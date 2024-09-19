import gymnasium as gym
from mapek_loop import MAPEKLoop
from attack_simulation import AttackSimulation
import matplotlib.pyplot as plt
from stable_baselines3 import PPO


def plot_performance(history):
    episodes = range(1, len(history) + 1)
    
    collision_rates = [metrics['collision_rate'] for metrics in history]
    avg_safe_distances = [metrics['avg_safe_distance'] for metrics in history]
    avg_speeds = [metrics['avg_speed'] for metrics in history]
    lane_change_success_rates = [metrics['lane_change_success_rate'] for metrics in history]
    gps_spoofing_rates = [metrics['gps_spoofing_rate'] for metrics in history]
    mitm_detection_rates = [metrics['mitm_detection_rate'] for metrics in history]
    
    # Plot safety and security metrics over episodes
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(episodes, collision_rates, label='Collision Rate', marker='o')
    plt.xlabel('Episode')
    plt.ylabel('Collision Rate')
    plt.title('Collision Rate over Episodes')
    plt.grid()
    
    plt.subplot(2, 2, 2)
    plt.plot(episodes, avg_safe_distances, label='Average Safe Distance', marker='o')
    plt.xlabel('Episode')
    plt.ylabel('Avg Safe Distance')
    plt.title('Avg Safe Distance over Episodes')
    plt.grid()
    
    plt.subplot(2, 2, 3)
    plt.plot(episodes, avg_speeds, label='Avg Speed', marker='o')
    plt.xlabel('Episode')
    plt.ylabel('Avg Speed')
    plt.title('Avg Speed over Episodes')
    plt.grid()
    
    plt.subplot(2, 2, 4)
    plt.plot(episodes, lane_change_success_rates, label='Lane Change Success Rate', marker='o')
    plt.xlabel('Episode')
    plt.ylabel('Lane Change Success')
    plt.title('Lane Change Success Rate')
    plt.grid()
    
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(episodes, gps_spoofing_rates, label='GPS Spoofing Detection Rate', marker='o')
    plt.plot(episodes, mitm_detection_rates, label='MitM Detection Rate', marker='o')
    plt.xlabel('Episode')
    plt.ylabel('Detection Rate')
    plt.title('GPS Spoofing & MitM Detection Rates over Episodes')
    plt.legend()
    plt.grid()
    plt.show()


# Initialize agents and environment
env = gym.make("highway-v0")
safety_model = PPO.load("safety_ppo_model")
security_model = PPO.load("security_ppo_model")
attack_simulation = AttackSimulation()

# Initialize MAPE-K loop
mapek_loop = MAPEKLoop(safety_model, security_model, attack_simulation, env)

# Run simulation over multiple episodes
num_episodes = 5
for episode in range(num_episodes):
    print(f"Starting episode {episode + 1}")
    obs, info = env.reset()
    done = False
    
    while not done:
        action = safety_agent.act(obs)  # Get action from safety agent
        action = mapek_loop.loop(obs, info, action)  # MAPE-K loop adjusts action if necessary
        obs, reward, done, truncated, info = env.step(action)
        env.render()

        if done or truncated:
            break

    # Update model if the metrics are better than previous episodes
    mapek_loop.update_model_if_needed()

# After all episodes are done, visualize the results
plot_performance(mapek_loop.get_history())
