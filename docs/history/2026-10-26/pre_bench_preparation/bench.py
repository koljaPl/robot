"""Read/log IMU by default. Explicit --channel enables one restricted pulse output."""
import argparse
import csv
import time
from pathlib import Path
from calibration import load_calibration
from serial_robot import SerialRobot


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',required=True);p.add_argument('--calibration',type=Path,default=Path('calibrations/example.invalid.json'))
    p.add_argument('--seconds',type=float,default=10);p.add_argument('--channel',type=int,choices=range(6));p.add_argument('--pulse-us',type=int,default=1500)
    p.add_argument('--output',type=Path,default=Path('runs/bench.csv'));a=p.parse_args()
    if not 0<a.seconds<=60 or not 1400<=a.pulse_us<=1600:p.error('Use 0..60 seconds and 1400..1600 us')
    c=load_calibration(a.calibration,require_valid=False)
    robot=SerialRobot(a.port,c);a.output.parent.mkdir(parents=True,exist_ok=True)
    try:
        robot.handshake();next_command=time.monotonic();end=next_command+a.seconds
        with a.output.open('x',newline='') as f:
            w=csv.writer(f);w.writerow(['host_ns','mcu_ms','ack','status',*[f'target_{i}' for i in range(6)],'ax','ay','az','gx','gy','gz'])
            while time.monotonic()<end:
                if a.channel is not None and time.monotonic()>=next_command:
                    robot.bench(a.channel,a.pulse_us);next_command+=.02
                kind,t=robot.read()
                if kind=='telemetry':w.writerow([time.monotonic_ns(),t.timestamp_ms,t.sequence,t.status,*t.applied_targets,*t.accelerometer,*t.gyroscope])
    finally:robot.close()

if __name__=='__main__':main()
