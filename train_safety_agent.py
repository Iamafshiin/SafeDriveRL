import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Create the environment (using highway-env for safety training)
env = make_vec_env("highway-v0", n_envs=4)

# Define and configure the PPO model
model = PPO(
    "MlpPolicy", 
    env, 
    verbose=1, 
    n_steps=1024, 
    batch_size=64, 
    n_epochs=10, 
    learning_rate=0.0003, 
    gamma=0.99,
    tensorboard_log="./highway_ppo/"
)

# Train the model for a specific number of timesteps
model.learn(total_timesteps=500000)

# Save the trained model for use in the Safety Agent
model.save("highway_ppo_safety_model")
