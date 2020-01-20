import tensorflow as tf
a=tf.constant([[1.,2.],[3.,4.]])
print('before:',a.dtype)
if a.dtype!=tf.float16:
    a=tf.cast(a,tf.float16) #tf.cast函数可以完成精度转换
    print('after:',a.dtype)
