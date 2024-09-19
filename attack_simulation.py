import random


class AttackSimulation:
    def __init__(self, gps_spoofing_prob=0.05, mitm_prob=0.05):
        self.gps_spoofing_prob = gps_spoofing_prob
        self.mitm_prob = mitm_prob

    def simulate_attacks(self):
        gps_spoofing = random.random() < self.gps_spoofing_prob
        mitm_attack = random.random() < self.mitm_prob
        return gps_spoofing, mitm_attack
