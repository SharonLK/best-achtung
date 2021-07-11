from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy

from default_environment import DefaultEnvironment

if __name__ == '__main__':
    env = DefaultEnvironment()

    model = PPO(ActorCriticPolicy, env, verbose=2)#, n_steps=512)
    model.learn(total_timesteps=20000000)

    model.save('sharon')

    # obs = env.reset()
    # for i in range(1000):
    #     action, _states = model.predict(obs, deterministic=True)
    #     obs, reward, done, info = env.step(action)
    #     print(reward)
    #     if done:
    #         obs = env.reset()

    env.close()
