# 每个智能体的动作空间都是一个整数值，范围是0-20，由于环境是二维有边界网格世界，智能体的动作也是离散的。
# 具体来说，0-20的动作对应如下：
# 0-向上两格（也就是智能体的坐标从(x,y)变成(x-2,y)）
# 1-向左上一格（也就是智能体的坐标从(x,y)变成(x-1,y-1)）
# 2-向上一格（也就是智能体的坐标从(x,y)变成(x-1,y)）
# 3-向右上一格（也就是智能体的坐标从(x,y)变成(x-1,y+1)）
# 4-向左两格
# 5-向左一格
# 6-不动
# 7-向右一格
# 8-向右两格
# 9-向左下一格
# 10-向下一格
# 11-向右下一格
# 12-向下两格
# 13-向左上攻击（也就是说，假设某个红方智能体当前坐标为(x,y)，它会去攻击坐标为(x-1,y-1)的蓝方智能体）
# 14-向上攻击（也就是说，假设智能体当前坐标为(x,y)，它会去攻击坐标为(x-1,y)的智能体）
# 15-向右上攻击
# 16-向左攻击
# 17-向右攻击
# 18-向左下攻击
# 19-向下攻击
# 20-向右下攻击