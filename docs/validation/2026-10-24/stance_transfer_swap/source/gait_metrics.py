"""Evaluation-only geometry/contact diagnostics. Never used in policy observations."""
import numpy as np


def progress_reward(displacement, dt):
    # Positive motion capped, backward motion fully charged: closed cycles cannot earn progress.
    return 10 * min(float(displacement), 0.06 * dt)


class GaitMetrics:
    """Credit translating alternating steps only, with a non-sliding supported stance.

    Foot centers and full-foot minimum heights are ground truth in simulation;
    physical trials must measure these externally using video. Contact alone does
    not prove load support: `supported` is the separate force diagnostic in SIM.
    """
    def __init__(self):
        self.previous = None
        self.airborne = np.zeros(2, dtype=bool)
        self.start = np.zeros((2, 2))
        self.stance_start = np.zeros((2, 2))
        self.clear_time = np.zeros(2)
        self.qualified = np.zeros(2, dtype=bool)
        self.valid_stance = np.ones(2, dtype=bool)
        self.steps = np.zeros(2, dtype=int)
        self.alternations = 0
        self.last = None
        self.distance = 0.0
        self.rejected = 0
        self.max_stance_slip = 0.0

    def update(self, centers, heights, contacts, supported, dt):
        centers = np.asarray(centers, dtype=float)[:, :2]
        contacts, supported = np.asarray(contacts, bool), np.asarray(supported, bool)
        if self.previous is None:
            self.previous = centers.copy()
        for i in range(2):
            j = 1-i
            if not contacts[i]:
                if not self.airborne[i]:
                    self.airborne[i] = True
                    self.start[i] = self.previous[i]
                    self.stance_start[i] = self.previous[j]
                    self.valid_stance[i] = True
                slip = float(np.linalg.norm(centers[j] - self.stance_start[i]))
                self.max_stance_slip = max(self.max_stance_slip, slip)
                self.valid_stance[i] &= bool(contacts[j] and supported[j] and slip <= .003)
                if heights[i] >= .003 and self.valid_stance[i]:
                    self.clear_time[i] += dt
                    self.qualified[i] |= self.clear_time[i] >= .04 - 1e-10
                else:
                    self.clear_time[i] = 0
            elif self.airborne[i]:
                advance = float(centers[i, 0]-self.start[i, 0])
                slip = float(np.linalg.norm(centers[j]-self.stance_start[i]))
                # No credit for hops, in-place lifts, toe pivots, or lifting then sliding.
                valid = (self.qualified[i] and self.valid_stance[i] and supported[i]
                         and supported[j] and slip <= .003 and advance >= .005
                         and abs(centers[i, 1]-self.start[i, 1]) <= .020)
                if valid and (self.last is None or self.last != i):
                    self.steps[i] += 1
                    self.alternations += int(self.last is not None)
                    self.last = i
                    # Two translating feet advance their midpoint by half the summed advance.
                    self.distance += advance/2
                else:
                    self.rejected += 1
                self.airborne[i] = False
                self.qualified[i] = False
                self.clear_time[i] = 0
        self.previous = centers.copy()
