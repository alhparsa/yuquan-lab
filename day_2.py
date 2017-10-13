import tensorflow as tf
import timeit

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)  # retrieving the data for the example from internet

x = tf.placeholder(tf.float32, [None, 784])  # input layer
W = tf.Variable(tf.zeros([784, 10]))  # weight layer
b = tf.Variable(tf.zeros([10]))  # bias layer

y = tf.nn.softmax(tf.matmul(x, W) + b)  # calculates the softmax

y_ = tf.placeholder(tf.float32, [None, 10])  # placeholder for the actual results

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))  # finds the loss

train_speed = 0.05

train = tf.train.GradientDescentOptimizer(train_speed).minimize(cross_entropy)  # model for training

sess = tf.InteractiveSession()

tf.global_variables_initializer().run()  # sets the variables

start = timeit.default_timer()  # starts the timer

for _ in range(1000):
    # training process
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train, feed_dict={x: batch_xs, y_: batch_ys})

stop = timeit.default_timer() # track the time again

time = stop - start # training time
print "time taken = ", round(time, 4), "s"
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))  # truth value of (x == y) element-wise
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) # mean of elements across dimensions of a tensor
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
