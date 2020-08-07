import sys
import numpy as np
import tensorflow as tf
from datetime import datetime
 
shape=(int(30000),int(30000))
 
with tf.device("/cpu:0"):
    random_matrix = tf.random_uniform(shape=shape, minval=0, maxval=1)
    dot_operation = tf.matmul(random_matrix, tf.transpose(random_matrix))
    sum_operation = tf.reduce_sum(dot_operation)
 
startTime = datetime.now()
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as session:
    result = session.run(sum_operation)
    print(result)
 
print()
print("CPU 계산 속도(시간) : ", datetime.now() - startTime, "초")
print()
 
with tf.device("/gpu:0"):
    random_matrix = tf.random_uniform(shape=shape, minval=0, maxval=1)
    dot_operation = tf.matmul(random_matrix, tf.transpose(random_matrix))
    sum_operation = tf.reduce_sum(dot_operation)
 
startTime = datetime.now()
with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as session:
    result = session.run(sum_operation)
    print(result)
 
print()
print("GPU 계산 속도(시간) : ", datetime.now() - startTime, "초")
print()
