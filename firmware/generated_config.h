#pragma once
// Generated. Calibration persists in firmware flash; reboot always disarmed.
constexpr const char* CONFIG_HASH="4d3b0dcbad59774b12f9c908c74446f6bf7452d5bdf34a08f07cf4271cc15019";
constexpr const char* CAL_HASH="04e1dd29253c457169b2ce286f728e44321864da91d80e072578953ecdc54479";
constexpr bool CAL_VALID=false;
constexpr float SIGN[6]={1.0f,1.0f,1.0f,-1.0f,-1.0f,-1.0f};
constexpr float ZERO[6]={1500.0f,1500.0f,1500.0f,1500.0f,1500.0f,1500.0f};
constexpr float GAIN[6]={500.0f,500.0f,500.0f,500.0f,500.0f,500.0f};
constexpr float PMIN[6]={900.0f,900.0f,900.0f,900.0f,900.0f,900.0f};
constexpr float PMAX[6]={2100.0f,2100.0f,2100.0f,2100.0f,2100.0f,2100.0f};
constexpr float QMIN[6]={-0.6108652382f,-0.1745329252f,-0.3490658504f,-0.6108652382f,-0.1745329252f,-0.3490658504f};
constexpr float QMAX[6]={0.6108652382f,1.047197551f,0.3490658504f,0.6108652382f,1.047197551f,0.3490658504f};
constexpr float HOME_Q[6]={-0.1745329252f,0.1745329252f,0.0f,-0.1745329252f,0.1745329252f,0.0f};
constexpr float MAX_SPEED=3.141592654f;
