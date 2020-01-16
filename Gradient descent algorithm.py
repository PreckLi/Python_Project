"""梯度下降算法"""

import numpy as np
from matplotlib import pyplot as plt
#1.采样数据
#真实模型 y=1.477x+0.089
#模拟真实样本的观测误差,添加误差自变量E,采样自均值为0,标准差为0.01的高斯分布 y=1.477x+0.089+E,E~N(0,0.01^2)
#随机采样n=100次,获得n个样本的训练数据集Dtrain


#2.计算误差
#循环计算每个点(x(i),y(i))预测值与真实值之间差的平方并累加
def mse(b,w,points):
    #根据当前w,b参数计算均方差损失
    totalError=0
    for i in range(0,len(points)):  #迭代所有的点
        x=points[i,0]   #i点输入x
        y=points[i,1]   #i点输出y
        #计算差的平方,并累加
        totalError+=(y-(w*x+b))**2
    #将累加的误差求平均，得均方差
    return totalError/float(len(points))

#3.梯度计算
#计算l对w偏导数,和l对b的偏导数
def step_gradient(b_current,w_current,points,lr):
    #误差在所有点上的导数,并更新w,b,lr为学习率
    b_gradient=0
    w_gradient=0
    M=float(len(points))    #样本总数
    for i in range(0,len(points)):
        x=points[i,0]
        y=points[i,1]
        # 求误差函数对b的导数：grad_b=2(wx+b-y)
        b_gradient+=(2/M)*((w_current*x+b_current)-y)
        # 求误差函数对w的导数：grad_w=2(wx+b-y)*x
        w_gradient+=(2/M)*x*((w_current*x+b_current)-y)
    #根据梯度下降算法更新w',b',lr为学习率
    new_b=b_current-(lr*b_gradient)
    new_w=w_current-(lr*w_gradient)
    return [new_b,new_w]

#4。梯度更新
#在计算出误差函数在𝑤和𝑏处的梯度后，我们可以更新𝑤和𝑏的值。我们把
# 对数据集的所有样本训练一次称为一个 Epoch，共循环迭代 num_iterations 个 Epoch。
def gradient_descent(points,starting_b,starting_w,lr,num_iterations):
    #循环更新w,b多次
    b=starting_b    #b的初始值
    w=starting_w    #w的初始值
    #根据梯度下降算法更新多次
    for step in range(num_iterations):
        b,w=step_gradient(b,w,np.array(points),lr)
        loss=mse(b,w,points)    #计算当前均方差,监控训练进度
        if step%50==0:  #打印误差和实时w,b值
            print(f"iteration:{step},loss:{loss},w:{w},b:{b}")
        wlist.append(w)
        blist.append(b)
        losslist.append(loss)

    return [b,w]    #返回最后一次w,b

#主函数
def main():
    #加载训练集数据
    lr=0.01
    initial_b=0 #初始化b
    initial_w=0 #初始化w
    num_iterations=1000
    #训练1000次，返回最优w*,b*和训练Loss的下降过程
    [b,w]=gradient_descent(data,initial_b,initial_w,lr,num_iterations)
    loss=mse(b,w,data)  #计算最优数值解w,b上的均方差
    print(f'Final loss:{loss},w:{w},b:{b}')

    plt.plot(losslist)
    plt.show()

if __name__ == '__main__':
    data = []
    wlist=[]
    blist=[]
    losslist=[]
    for i in range(100):
        x = np.random.uniform(-10, 10.)  # 随机采样输入x
        # 采样高斯噪声
        eps = np.random.normal(0., 0.01)  # 生成正态分布的概率密度
        # 得到模型输出
        y = 1.477 * x + 0.089 + eps
        data.append([x, y])  # 保存样本点
    data = np.array(data)  # 转换为2D numpu数组constant

    main()






