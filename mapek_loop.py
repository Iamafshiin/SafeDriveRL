
from attack_simulation import AttackSimulation

class MAPEKLoop:
    def __init__(self, safety_model, security_model, attack_simulation, env):
        self.safety_model = safety_model
        self.security_model = security_model
        self.attack_simulation = attack_simulation
        self.env = env
        self.best_metrics = None  # Track the best metrics
        self.history = []  # History of performance across episodes
    
    def monitor(self, obs):
        return obs
    
    def analyze(self, info):
        # Simulate security attacks and detect them
        gps_spoofing, mitm_attack = self.attack_simulation.simulate_attacks()
        gps_spoofing_detected, mitm_detected = self.detect_attacks(gps_spoofing, mitm_attack)
        
        # Get safety metrics directly from the environment info
        speed = info.get('speed', 0)
        distance_to_nearest_car = info.get('distance_to_nearest_car', 0)
        safety_metrics = self.get_safety_metrics(info, speed, distance_to_nearest_car)
        
        return gps_spoofing_detected, mitm_detected, safety_metrics
    
    def detect_attacks(self, gps_spoofing, mitm_attack):
        # Use the security model to predict if attacks are detected based on observations
        obs = [gps_spoofing, mitm_attack]
        gps_spoofing_detected, _ = self.security_model.predict(obs)
        mitm_detected, _ = self.security_model.predict(obs)
        return gps_spoofing_detected, mitm_detected
    
    def plan(self, gps_spoofing_detected, mitm_detected):
        # Plan action based on detected security threats
        if gps_spoofing_detected or mitm_detected:
            return True  # Indicate that there is a security issue
        return False
    
    def execute(self, safety_issue, action):
        # Adjust safety actions based on security threats
        if safety_issue:
            print("Adjusting action due to detected security issue")
            action = 0  # Example: Stop the vehicle or take safer action
        return action
    
    def loop(self, obs, info, action):
        obs = self.monitor(obs)
        gps_spoofing_detected, mitm_detected, safety_metrics = self.analyze(info)
        safety_issue = self.plan(gps_spoofing_detected, mitm_detected)
        action = self.execute(safety_issue, action)
        return action
    
    def get_safety_metrics(self, info, speed, distance_to_nearest_car):
        # Collect safety-related metrics
        safety_metrics = {
            'collision_rate': info.get('collision_rate', 0),
            'avg_safe_distance': distance_to_nearest_car,
            'avg_speed': speed,
            'lane_change_success_rate': info.get('lane_change_success_rate', 0),
        }
        return safety_metrics
    
    def update_model_if_needed(self):
        # Get safety metrics directly from the environment
        current_metrics = {
            'collision_rate': self.env.get('collision_rate', 0),
            'avg_safe_distance': self.env.get('avg_safe_distance', 0),
            'avg_speed': self.env.get('speed', 0),
            'lane_change_success_rate': self.env.get('lane_change_success_rate', 0),
        }

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
