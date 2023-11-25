import random

AGT_POS = (6, 6)
MAP_SIZE = 45
ATK_UTIL = 100  # 这个值必须要大于MAP_SIZE，否则智能体会认为攻击的效用不如移动的效用


def vcg_auction(observation):
    best_action = None
    min_vcg_payment = float('inf')  # 正无穷

    for action in range(21):  # 遍历所有动作
        vcg_payment = compute_vcg_payment(action, observation)

        if vcg_payment is None:
            return 7
            # 移动动作的随机值
            # return random.randint(0, 12)

        if vcg_payment < min_vcg_payment:
            min_vcg_payment = vcg_payment
            best_action = action

    return best_action


def compute_vcg_payment(action, current_obs):
    impact = compute_impact(action, current_obs)
    if impact is None:
        return None
    else:
        # 计算其他红方智能体选择该动作的估值，即VCG支付
        vcg_payment = -impact  # 注意这里取负值
        return vcg_payment


def compute_impact(action, current_obs):
    # 考虑移动带来的影响
    move_impact = compute_move_impact(action, current_obs)

    # 考虑攻击带来的影响
    attack_impact = compute_attack_impact(action, current_obs)

    if move_impact is None or attack_impact is None:
        return None

    # 总体影响为移动带来的影响加上攻击带来的影响
    total_impact = move_impact + attack_impact

    return total_impact


def compute_move_impact(action, current_obs):
    # 判断动作是否是移动
    if 0 <= action <= 5 or 7 <= action <= 12:
        # 获取当前智能体的坐标
        current_agent_position = AGT_POS

        # 获取智能体移动后的坐标
        new_agent_position = get_new_agent_position(action, current_agent_position)

        # 获取所有蓝方智能体的坐标
        blue_agent_positions = get_blue_agent_positions(current_obs)

        if len(blue_agent_positions) is 0:
            return None

        # 计算智能体移动后到最近蓝方智能体的距离
        min_distance = min(manhattan_distance(new_agent_position, blue_pos) for blue_pos in blue_agent_positions)

        if min_distance == 0:
            return 0

        # 影响的计算，可以根据实际情况进行调整
        impact = MAP_SIZE / min_distance  # 距离越近，影响越大

        return impact

    return 0


def compute_attack_impact(action, current_obs):
    # 判断动作是否是攻击
    if 13 <= action <= 20:
        agent_position = AGT_POS

        # 获取所有蓝方智能体的坐标
        blue_agent_positions = get_blue_agent_positions(current_obs)

        if len(blue_agent_positions) is 0:
            return None

        # 获取所有蓝方智能体的坐标和生命值
        # blue_agents_info = [(pos, current_obs[pos[0], pos[1], 4]) for pos in blue_agent_positions]

        # 获取攻击目标的坐标
        attack_target_position = get_attack_target_position(action, agent_position)

        # 判断攻击目标是否在观测范围内
        if attack_target_position in blue_agent_positions:
            # 攻击目标在观测范围内，计算对其的影响
            attack_power = ATK_UTIL
            attack_impact = attack_power  # 攻击的影响
            return attack_impact

    # 如果不是攻击动作或者攻击目标不在范围内，攻击影响为0
    return 0


def get_blue_agent_positions(current_obs):
    # 获取观测中所有蓝方智能体的坐标
    blue_agent_positions = [(i, j) for i in range(13) for j in range(13) if current_obs[i, j, 3] == 1]

    return blue_agent_positions


def get_new_agent_position(action, current_agent_position):
    # 定义动作对应的偏移量
    offsets = {
        0: (-2, 0),
        1: (-1, -1),
        2: (-1, 0),
        3: (-1, 1),
        4: (0, -2),
        5: (0, -1),
        6: (0, 0),
        7: (0, 1),
        8: (0, 2),
        9: (1, -1),
        10: (1, 0),
        11: (1, 1),
        12: (2, 0),
    }

    # 根据动作获取偏移量
    offset = offsets.get(action)

    # 计算新坐标
    new_agent_position = (current_agent_position[0] + offset[0], current_agent_position[1] + offset[1])

    return new_agent_position


def get_attack_target_position(action, agent_position):
    x, y = agent_position

    # 定义动作对应的偏移量
    offsets = {
        13: (-1, -1),
        14: (-1, 0),
        15: (-1, 1),
        16: (0, -1),
        17: (0, 1),
        18: (1, -1),
        19: (1, 0),
        20: (1, 1),
    }

    # 根据动作获取偏移量
    offset = offsets.get(action)

    # 计算攻击目标坐标
    target_position = (x + offset[0], y + offset[1])

    return target_position


def manhattan_distance(pos1, pos2):
    # 计算曼哈顿距离
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
