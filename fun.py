import numpy as np
from numpy import cos, sin, pi
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from matplotlib.widgets import Slider

# 将笛卡尔坐标转换为极坐标
def cart2pol(r):
    x,y,z = r
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi
    
# rho->theta
# 半径是一个决定theta的重要参数
def cal_Theta(radius, rho):
    Theta = rho * -(pi/radius) + pi
    Theta[rho>1] = 0
    return Theta

def cal_nr(r,m=1,eta=0,radius=1):
    rho,phi = cart2pol(r)
    
    # m 拓扑数
    # eta 螺旋度
    Phi = m*phi + eta
    Theta = cal_Theta(radius, rho)
    
    X = cos(Phi)*sin(Theta)
    Y = sin(Phi)*sin(Theta)
    Z = cos(Theta)
    
    return np.array([X,Y,Z])

# 计算颜色
def cal_color(nr):
    # 以方位角着色
    h = np.arctan2(nr[0], nr[1])
    # 展平并归一化
    h = (h.ravel() - (-pi)) / (2*pi)

    # 用于得出S和V
    tmp = nr[2].ravel() # nr[2]是z方向上的分量
    tmp = (tmp - (-1))/2

    # tmp<=0.5时，s = 1,v = 1-2*tmp
    # tmp>0.5时，v = 1,s = -2*(tmp-1)
    s = np.zeros_like(tmp)
    s[tmp<=0.5] = 1
    s[tmp>0.5] = -2*(tmp[tmp>0.5]-1)

    v = np.zeros_like(tmp)
    v[tmp<=0.5] = 2*tmp[tmp<=0.5]
    v[tmp>0.5] = 1

    hsv = np.column_stack((h, s, v))

    # Colormap
    c = hsv_to_rgb(hsv)
    # 给箭身和箭头分别上色
    c = np.concatenate((c,c.repeat(2,axis=0)),axis=0)
    return c

# 计算箭头的起点和终点
def cal_data(r,m=1,eta=0,radius=1):
    nr = cal_nr(r,m=m,eta=eta,radius=radius)
    nr = nr / np.linalg.norm(nr,axis=0).max()
    length = (r[0][0][1] - r[0][0][0])[0]
    start = r - nr * length / 2
    end   = r + nr * length / 2
    d = end - start

    start_X, start_Y, start_Z, dx, dy, dz = start[0], start[1], start[2], d[0], d[1], d[2]
    
    c = cal_color(nr) 
    
    return start_X, start_Y, start_Z, dx, dy, dz, c,length
