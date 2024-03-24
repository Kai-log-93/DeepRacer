import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.linspace(0, 10000, 10)
reward_p = np.sin(x)
reward_s = np.cos(x)

# 创建图形和坐标轴
fig, ax = plt.subplots()

# 绘制曲线

# reward = ((params["progress"] / params["steps"]) * 100) + (params["speed"]**2)
ax.plot(x, y_sin, label='sin(x)')
ax.plot(x, y_cos, label='cos(x)')

# 添加标题和标签
ax.set_title('Sin and Cos Curves')
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')

# 显示图例
ax.legend()

# 展示图形
plt.show()
