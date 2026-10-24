"""Command delay and bounded position-target trajectory, shared with hardware tests."""
from collections import deque
import numpy as np
from robot_config import HOME, JOINT_LOW, JOINT_HIGH, TARGET_SPEED, SERVO_DEADBAND, PWM_RESOLUTION_US, ESTIMATED_US_PER_RAD


class ServoTargets:
    def __init__(self, delay=0.02, speed=TARGET_SPEED, deadband=SERVO_DEADBAND, calibration=None):
        self.calibration = calibration
        self.delay = float(delay)
        self.speed = float(speed)
        self.deadband = float(deadband)
        self.reset()

    def reset(self, home=HOME):
        self.applied = np.asarray(home, dtype=float).copy()
        self.goal = self.applied.copy()
        self.accepted = self.applied.copy()
        self.queue = deque()

    def enqueue(self, time, target):
        target = np.asarray(target, dtype=float)
        if target.shape != (6,) or not np.isfinite(target).all():
            raise ValueError("Invalid servo target")
        bounded = np.clip(target, JOINT_LOW, JOINT_HIGH)
        self.queue.append((float(time) + self.delay, bounded.copy()))

    def advance(self, time, dt):
        while self.queue and self.queue[0][0] <= time + 1e-10:
            _, incoming = self.queue.popleft()
            # Ignore sub-deadband reversals until accumulated change passes threshold.
            changed = np.abs(incoming - self.accepted) >= self.deadband
            self.accepted[changed] = incoming[changed]
            self.goal = self.accepted.copy()
        self.applied += np.clip(self.goal - self.applied, -self.speed * dt, self.speed * dt)
        self.applied = np.clip(self.applied, JOINT_LOW, JOINT_HIGH)
        return self.quantize(self.applied)

    def quantize(self, target):
        # Integer-us native PWM, per-channel measured mapping if supplied.
        if self.calibration is None:
            quantum = PWM_RESOLUTION_US / ESTIMATED_US_PER_RAD
            quantized = np.rint(np.asarray(target) / quantum)*quantum
            return np.clip(quantized, np.ceil(JOINT_LOW/quantum)*quantum,
                           np.floor(JOINT_HIGH/quantum)*quantum)
        c = self.calibration
        zero = np.array(c['zero_us']); gain = np.array(c['us_per_rad'])*c['sign']
        pulse_a = zero+gain*JOINT_LOW; pulse_b = zero+gain*JOINT_HIGH
        pulses = np.clip(np.rint(zero+gain*target),np.ceil(np.minimum(pulse_a,pulse_b)),np.floor(np.maximum(pulse_a,pulse_b)))
        return (pulses-zero)/gain
