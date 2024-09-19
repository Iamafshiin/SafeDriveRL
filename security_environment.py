import gymnasium as gym
import random

class SecurityEnvironment(gym.Env):
    def __init__(self):
        super(SecurityEnvironment, self).__init__()

        # Define action space (for Security Agent)
        self.action_space = gym.spaces.Discrete(3)

        # Define observation space (for input data to the Security Agent)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(3,), dtype=float)

        # Track whether the attack occurred
        self.attack_status = {'gps_spoofing': False, 'mitm_attack': False}
        self.steps = 0
        self.max_steps = 100

    def reset(self):
        # Reset the environment and attack status
        self.attack_status = {'gps_spoofing': False, 'mitm_attack': False}
        self.steps = 0
        obs = self._get_observation()
        return obs, {}

    def _get_observation(self):
        gps_spoofing_ind = float(self.attack_status['gps_spoofing'])
        mitm_ind = float(self.attack_status['mitm_attack'])
        normal_data = random.random()  # Random normal environment data
        return [gps_spoofing_ind, mitm_ind, normal_data]

    def step(self, action):
        # Simulate attack events randomly
        if random.random() < 0.05:  # 5% chance for GPS Spoofing
            self.attack_status['gps_spoofing'] = True
        if random.random() < 0.05:  # 5% chance for MitM attack
            self.attack_status['mitm_attack'] = True

        done = False
        reward = 0

        if action == 1:  # Detect GPS Spoofing
            if self.attack_status['gps_spoofing']:
                reward += 1  # Correct detection
            else:
                reward -= 0.5  # False positive
        
        if action == 2:  # Detect MitM attack
            if self.attack_status['mitm_attack']:
                reward += 1  # Correct detection
            else:
                reward -= 0.5  # False positive

        if self.attack_status['gps_spoofing'] and action != 1:
            reward -= 1  # Missed GPS Spoofing attack
        if self.attack_status['mitm_attack'] and action != 2:
            reward -= 1  # Missed MitM attack

        self.steps += 1
        if self.steps >= self.max_steps:
            done = True

        obs = self._get_observation()
        return obs, reward, done, False, {}

    def render(self, mode='human'):
        pass
