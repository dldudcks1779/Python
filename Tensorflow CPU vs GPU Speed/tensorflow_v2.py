import tensorflow as tf
import time

def cpu_time_matmul(x):
    start = time.time()
    for loop in range(10):
        tf.matmul(x, x)

    result = time.time()-start
    print()
    print("CPU 속도 : {:0.3f} 초".format(result))
    print()

def gpu_time_matmul(x):
    start = time.time()
    for loop in range(10):
        tf.matmul(x, x)

    result = time.time()-start
    print()
    print("GPU 속도 : {:0.3f} 초".format(result))
    print()


# CPU에서 강제 실행
with tf.device("CPU:0"):
    x = tf.random.uniform([20000, 20000])
    assert x.device.endswith("CPU:0")
    cpu_time_matmul(x)

# GPU 이용 가능시 GPU에서 강제 실행
if tf.test.is_gpu_available():
    with tf.device("GPU:0"):
        x = tf.random.uniform([10000, 10000])
        assert x.device.endswith("GPU:0")
        gpu_time_matmul(x)      
