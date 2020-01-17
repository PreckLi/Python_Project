import os
import tensorflow as tf
#pycharm2019.3之前版本识别不了tensorflow.keras,只有这样写
try:
    import tensorflow.python.keras as keras
except:
    import tensorflow.keras as keras
from tensorflow.python.keras import layers,optimizers,datasets  #导入tf子库等
(x,y),(x_val,y_val)=datasets.mnist.load_data()  #加载mnist数据集，第一个为训练集，第二个为测试集
"""从 TensorFlow 中加载的 MNIST 数据图片，数值的范围为[0,255]。在机器学习中间，
一般希望数据的范围在 0 周围的小范围内分布。通过预处理步骤，我们把[0,255]像素范围
归一化(Normalize)到[0,1.]区间，再缩放到[−1,1]区间，从而有利于模型的训练。"""
x=2*tf.convert_to_tensor(x,dtype=tf.float32)/255.-1 #转换为浮点张量,并缩放到-1~1
y=tf.convert_to_tensor(y,dtype=tf.int32)    #转换为整型张量
"""可以将输出设置为𝑑out个输出节点的向量，𝑑out与类别数相
同，让第𝑖 ∈ [1, 𝑑out]个输出节点的值表示当前样本属于类别𝑖的概率𝑃(𝒙属于类别𝑖|𝒙)。我
们只考虑输入图片只输入一个类别的情况，此时输入图片的真实标签已经唯一确定：如果
物体属于第𝑖类的话，那么索引为𝑖的位置上设置为 1，其他位置设置为 0，我们把这种编码
方式叫作 one-hot 编码(独热编码)。"""
y=tf.one_hot(y,depth=10)    #one-hot编码
print(x.shape,y.shape)
print("x:",x)
train_dataset=tf.data.Dataset.from_tensor_slices((x,y)) #构建数据集对象
print('train_dataset:',train_dataset)
train_dataset=train_dataset.batch(512)  #批量训练
print(train_dataset)
