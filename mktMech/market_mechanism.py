import random
import time

import numpy as np
from pettingzoo.utils.env import AECEnv
from pettingzoo.utils import random_demo

from magent2.environments import battle_v4

from vcg import vcg_auction


def default_policy(obs, agent):
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
        if 'red' in agent:
            action = 7
        else:
            action = 5
    return action


def random_policy(obs, agent):
    return env.action_space(agent).sample()


def mkt_mech(env: AECEnv, render: bool = True, episodes: int = 1, red_policy='random', blue_policy='random') -> float:
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
                if 'red' in agent:
                    if red_policy == 'random':
                        action = random_policy(obs, agent)
                    elif red_policy == 'vcg':
                        action = vcg_auction(obs)
                    else:
                        action = default_policy(obs, agent)
                else:
                    if blue_policy == 'random':
                        action = random_policy(obs, agent)
                    else:
                        action = default_policy(obs, agent)
            env.step(action)
        completed_episodes += 1

    time.sleep(60)  # 阻塞进程
    if render:
        env.close()


if __name__ == '__main__':
    env = battle_v4.env(render_mode='human')
    mkt_mech(env, render=False, episodes=1, red_policy='vcg', blue_policy='random')
