import random
import time

import numpy as np
from pettingzoo.utils.env import AECEnv
from pettingzoo.utils import random_demo

from magent2.environments import battle_v4
env = battle_v4.env(render_mode='human')


random_demo(env, render=False, episodes=9)

def policy(observation, agent):
    return env.action_space(agent).sample()


env.reset()
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    action = policy(observation, agent)
    env.step(action)

