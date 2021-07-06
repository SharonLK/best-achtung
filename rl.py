from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy
import gym
from default_environment import DefaultEnvironment

if __name__ == '__main__':
    env = DefaultEnvironment()
    for i_episode in range(20):
        observation = env.reset()
        for t in range(100):
            env.render()
            print(observation)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
    env.close()
