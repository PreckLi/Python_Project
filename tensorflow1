import tensorflow as tf
import timeit
# a=tf.constant(2.)
# b=tf.constant(4.)
# print('a+b=',a+b)
with tf.device('/cpu:0'):
    cpu_a=tf.random.normal([1,100])
    cpu_b=tf.random.normal([100,1])
    print(cpu_a.device,cpu_b.device)

with tf.device('/gpu:0'):
    gpu_a=tf.random.normal([1,100])
    gpu_b=tf.random.normal([100,1])
    print(gpu_a.device,gpu_b.device)

def cpu_run():
    with tf.device('/cpu:0'):
        c=tf.matmul(cpu_a,cpu_b)
    return c

def gpu_run():
    with tf.device('/gpu:0'):
        c=tf.matmul(gpu_a,gpu_b)
    return c


cpu_time=timeit.timeit(cpu_run,number=10)
gpu_time=timeit.timeit(gpu_run,number=10)
print('warmup:',cpu_time,gpu_time)

cpu_time=timeit.timeit(cpu_run,number=10)
gpu_time=timeit.timeit(gpu_run,number=10)
print('run_time:',cpu_time,gpu_time)
