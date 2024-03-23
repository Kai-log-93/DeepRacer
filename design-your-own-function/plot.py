import matplotlib.pyplot as plt
import numpy as np

# 准备数据
x = np.linspace(0, 10, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

# 创建图形和坐标轴
fig, ax = plt.subplots()

# 绘制曲线
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
