from stable_baselines3 import PPO
from security_environment import SecurityEnvironment

# Create the security environment
env = SecurityEnvironment()

# Define the PPO model for the Security Agent
model = PPO(
    "MlpPolicy", 
    env, 
    verbose=1, 
    n_steps=1024, 
    batch_size=64, 
    n_epochs=10, 
    learning_rate=0.0003, 
    gamma=0.99,
    tensorboard_log="./security_ppo/"
)

# Train the model
model.learn(total_timesteps=500000)

# Save the trained model for the Security Agent
model.save("security_ppo_model")
