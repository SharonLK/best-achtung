from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy

from default_environment import DefaultEnvironment

if __name__ == '__main__':
    env = DefaultEnvironment()

    model = PPO(ActorCriticPolicy, env, verbose=1)
    model.learn(total_timesteps=1000)

    env.close()
