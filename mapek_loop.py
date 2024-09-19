from safety_agent import SafetyAgent
from security_agent import SecurityAgent
from attack_simulation import AttackSimulation


class MAPEKLoop:
    def __init__(self, safety_agent: SafetyAgent, security_agent: SecurityAgent, attack_simulation: AttackSimulation, env):
        self.safety_agent = safety_agent
        self.security_agent = security_agent
        self.attack_simulation = attack_simulation
        self.env = env
        self.best_metrics = None  # Track the best metrics
        self.history = []  # History of performance across episodes
    
    def monitor(self, obs):
        return obs
    
    def analyze(self, info):
        gps_spoofing, mitm_attack = self.attack_simulation.simulate_attacks()
        gps_spoofing_detected, mitm_detected = self.security_agent.detect_attacks(gps_spoofing, mitm_attack)
        
        # Update safety metrics using the SafetyAgent
        speed = info.get('speed', 0)
        distance_to_nearest_car = info.get('distance_to_nearest_car', 0)
        self.safety_agent.update_metrics(info, speed, distance_to_nearest_car)
        
        return gps_spoofing_detected, mitm_detected
    
    def plan(self, gps_spoofing_detected, mitm_detected):
        return self.security_agent.analyze_security(gps_spoofing_detected, mitm_detected)
    
    def execute(self, safety_issue, action):
        return self.safety_agent.adjust_for_attacks(safety_issue, action)
    
    def loop(self, obs, info, action):
        obs = self.monitor(obs)
        gps_spoofing_detected, mitm_detected = self.analyze(info)
        safety_issue = self.plan(gps_spoofing_detected, mitm_detected)
        action = self.execute(safety_issue, action)
        return action
    
    def update_model_if_needed(self):
        current_safety_metrics = self.safety_agent.get_safety_metrics()
        current_security_metrics = self.security_agent.get_security_metrics()
        current_metrics = {**current_safety_metrics, **current_security_metrics}
        
        if self.best_metrics is None or self.is_better_metrics(current_metrics, self.best_metrics):
            print("Updating model: new metrics are better")
            self.best_metrics = current_metrics  # Save the new best metrics
        
        self.history.append(current_metrics)
    
    def is_better_metrics(self, current, best):
        # Define criteria to determine if the current metrics are better than the best
        return (current['collision_rate'] < best['collision_rate']) and \
               (current['avg_safe_distance'] > best['avg_safe_distance']) and \
               (current['avg_speed'] >= best['avg_speed']) and \
               (current['lane_change_success_rate'] >= best['lane_change_success_rate'])
    
    def get_history(self):
        return self.history
