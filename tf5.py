import tensorflow as tf
import numpy as np
a=tf.constant([-1,0,1,2])
aa=tf.Variable(a)   #通过 tf.Variable()函数可以将普通张量转换为待优化张量
print(aa.name,aa.trainable)
b=tf.Variable([[1,2],[3,4]])    #直接创建Variable张量

#从列表创建张量
c=tf.convert_to_tensor([1,2.])

#从数组中创建张量
d=tf.convert_to_tensor(np.array([[1,2.],[3,4]]))

#创建全0和全1的标量
e,f=tf.zeros([]),tf.ones([])

#创建全0和全1的向量
e,f=tf.zeros([1]),tf.ones([1])

#创建全0和全1的矩阵
e,f=tf.zeros([2,2]),tf.ones([3,4])  #2行2列，3行3列

a = tf.zeros([3,2]) # 创建一个矩阵
tf.ones_like(a) # 创建一个与 a 形状相同，但是全 1 的新矩阵
