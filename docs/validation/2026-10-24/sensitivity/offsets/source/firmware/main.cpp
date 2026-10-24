#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"
#include "hardware/i2c.h"
#include "control.h"
#include <cstdio>
#include <cstdarg>

constexpr uint PINS[6]={0,1,2,3,6,7};
Control ctrl;
float accel[3]{},gyro[3]{};
void send(const char* format,...){
    char body[180];va_list args;va_start(args,format);vsnprintf(body,sizeof(body),format,args);va_end(args);
    printf("%s*%04X\n",body,crc16(body));
}
bool reg(uint8_t r,uint8_t v){uint8_t b[2]={r,v};return i2c_write_timeout_us(i2c0,0x68,b,2,false,1500)==2;}
bool whoami(){
    uint8_t r=0x75,id=0;
    return i2c_write_timeout_us(i2c0,0x68,&r,1,true,1500)==1 && i2c_read_timeout_us(i2c0,0x68,&id,1,false,1500)==1 && id==0x68;
}
bool sample(){
    uint8_t r=0x3b,b[14];
    if(i2c_write_timeout_us(i2c0,0x68,&r,1,true,1500)!=1 || i2c_read_timeout_us(i2c0,0x68,b,14,false,1500)!=14)return false;
    auto raw=[&](int i){return int16_t((uint16_t(b[i])<<8)|b[i+1]);};
    for(int i=0;i<3;++i){accel[i]=raw(i*2)*9.80665f/16384;gyro[i]=raw(8+i*2)*.01745329252f/131;}
    return true;
}
void output(){
    for(int i=0;i<6;++i){int pulse=ctrl.armed?ctrl.pulse(i):(ctrl.bench&&ctrl.channel==i?ctrl.bench_us:0);pwm_set_gpio_level(PINS[i],pulse);}
}
int main(){
    stdio_init_all();
    for(auto pin:PINS){gpio_init(pin);gpio_put(pin,0);gpio_set_dir(pin,GPIO_OUT);}
    for(auto pin:PINS){
        gpio_set_function(pin,GPIO_FUNC_PWM);auto slice=pwm_gpio_to_slice_num(pin);
        pwm_config cfg=pwm_get_default_config();pwm_config_set_clkdiv(&cfg,float(clock_get_hz(clk_sys))/1000000.f);pwm_config_set_wrap(&cfg,19999);
        pwm_init(slice,&cfg,true);pwm_set_gpio_level(pin,0);
    }
    i2c_init(i2c0,400000);gpio_set_function(4,GPIO_FUNC_I2C);gpio_set_function(5,GPIO_FUNC_I2C);gpio_pull_up(4);gpio_pull_up(5);
    sleep_ms(100);
    // MPU6050: wake, DLPF=3 (~44Hz accel/42Hz gyro), sample divider4 ->200Hz, +/-2g,+/-250deg/s.
    bool configured=whoami()&&reg(0x6b,1)&&reg(0x1a,3)&&reg(0x19,4)&&reg(0x1b,0)&&reg(0x1c,0);
    char line[192];unsigned used=0;bool overflow=false;uint32_t next_imu=0,next_control=0;
    while(true){
        uint32_t now=to_ms_since_boot(get_absolute_time());ctrl.watchdog(now);
        if(int32_t(now-next_imu)>=0){
            next_imu=now+5;ctrl.imu=configured&&sample();
            if(!ctrl.imu && ctrl.armed)ctrl.fail();
            send("T,1,%u,%lu,%u,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d",ctrl.ack_seq,(unsigned long)now,ctrl.status(),
                 int(std::lround((ctrl.pulse(0)-ZERO[0])/(SIGN[0]*GAIN[0])*1000)),int(std::lround((ctrl.pulse(1)-ZERO[1])/(SIGN[1]*GAIN[1])*1000)),int(std::lround((ctrl.pulse(2)-ZERO[2])/(SIGN[2]*GAIN[2])*1000)),int(std::lround((ctrl.pulse(3)-ZERO[3])/(SIGN[3]*GAIN[3])*1000)),int(std::lround((ctrl.pulse(4)-ZERO[4])/(SIGN[4]*GAIN[4])*1000)),int(std::lround((ctrl.pulse(5)-ZERO[5])/(SIGN[5]*GAIN[5])*1000)),
                 int(accel[0]*1000),int(accel[1]*1000),int(accel[2]*1000),int(gyro[0]*1000),int(gyro[1]*1000),int(gyro[2]*1000));
        }
        if(int32_t(now-next_control)>=0){next_control=now+20;ctrl.tick(now);}
        int ch=getchar_timeout_us(0);
        if(ch>=0){
            if(ch=='\n'){
                if(overflow){ctrl.fail();}else{line[used]=0;bool ok=ctrl.packet(line,now);if(ok)send("I,1,%s,%s,%u",CONFIG_HASH,CAL_HASH,ctrl.status());}
                used=0;overflow=false;
            }else if(ch<32||ch>126||used>=sizeof(line)-1){overflow=true;ctrl.fail();}
            else if(!overflow)line[used++]=char(ch);
        }
        output(); // immediate PWM disable on fault; servo electronics may still retain position
        tight_loop_contents();
    }
}
