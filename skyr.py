import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import fun

# 生成网格数据
x = np.linspace(-1., 1., 30)
y = np.linspace(-1., 1., 30)
X, Y, Z = np.meshgrid(x, y, 0)
# 将网格数据转换为向量
r = np.array((X, Y, Z))



# 创建三维图形
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

*data,c,length = fun.cal_data(r)
quiver = ax.quiver(*data,color=c,length=length, normalize=True)


ax.axis('equal')
ax.set_facecolor([0.4]*3)
ax.set_axis_off()
ax.set_position([0,0.15,1,1])

m_slider_ax = fig.add_axes([0.1, 0.05, 0.8, 0.03])
m_slider = Slider(m_slider_ax, 'm', -2, 2, valinit=1)

eta_slider_ax = fig.add_axes([0.1, 0.08, 0.8, 0.05])
eta_slider = Slider(eta_slider_ax, 'eta', -3.14, 3.14, valinit=0)

def update(val):
    global quiver
    quiver.remove()
    *data,c,length = fun.cal_data(r,m=m_slider.val,eta=eta_slider.val)
    quiver = ax.quiver(*data,color=c,length=length, normalize=True)
    fig.canvas.draw_idle()
    
m_slider.on_changed(update)
eta_slider.on_changed(update)

# 显示图形
plt.show()