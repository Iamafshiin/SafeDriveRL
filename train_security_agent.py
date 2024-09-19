import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
import highway_env

if __name__ == "__main__":
    train = True
    n_cpu = 6
    batch_size = 64
    learning_rate = 5e-4
    gamma = 0.85
    n_steps = batch_size * 12 // n_cpu
    n_epochs = 10

    env = make_vec_env(SecurityEnvironment, n_envs=n_cpu, vec_env_cls=SubprocVecEnv)

    if train:
        model = PPO(
            "MlpPolicy",
            env,
            policy_kwargs=dict(net_arch=[dict(pi=[256, 256], vf=[256, 256])]),
            n_steps=n_steps,
            batch_size=batch_size,
            n_epochs=n_epochs,
            learning_rate=learning_rate,
            gamma=gamma,
            verbose=2,
            tensorboard_log="security_ppo/",
        )
        model.learn(total_timesteps=50000)
        model.save("security_ppo/security_model")

    model = PPO.load("security_ppo_model")