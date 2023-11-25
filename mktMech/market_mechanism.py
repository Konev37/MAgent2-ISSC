import random
import time

import numpy as np
from pettingzoo.utils.env import AECEnv
from pettingzoo.utils import random_demo

from magent2.environments import battle_v4

env = battle_v4.env(render_mode='human')


def red_policy(obs, agent):
    if obs[5][5][3] == 1:
        action = 13
    elif obs[5][6][3] == 1:
        action = 14
    elif obs[5][7][3] == 1:
        action = 15
    elif obs[6][5][3] == 1:
        action = 16
    elif obs[6][7][3] == 1:
        action = 17
    elif obs[7][5][3] == 1:
        action = 18
    elif obs[7][6][3] == 1:
        action = 19
    elif obs[7][7][3] == 1:
        action = 20
    else:
        action = 7
    return action
    # return env.action_space(agent).sample()


def blue_policy(obs, agent):
    return env.action_space(agent).sample()


def mkt_mech(env: AECEnv, render: bool = True, episodes: int = 1) -> float:
    completed_episodes = 0
    while completed_episodes < episodes:
        env.reset()
        for agent in env.agent_iter():
            if render:
                env.render()

            obs, reward, termination, truncation, _ = env.last()
            if termination or truncation:
                action = None
            elif isinstance(obs, dict) and "action_mask" in obs:
                action = random.choice(np.flatnonzero(obs["action_mask"]).tolist())
            else:
                # action = env.action_space(agent).sample()
                if 'red' in agent:
                    action = red_policy(obs, agent)
                else:
                    action = blue_policy(obs, agent)
            env.step(action)
        completed_episodes += 1

    time.sleep(60)  # 阻塞进程
    if render:
        env.close()


if __name__ == '__main__':
    mkt_mech(env, render=False, episodes=1)
