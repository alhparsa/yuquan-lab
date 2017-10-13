
import timeit

import tensorflow as tf

node1 = tf.constant(3.0, dtype=tf.float32)
node2 = tf.constant(4.0)

# print(node1, node2)

sess = tf.Session()
# print(sess.run([node1, node2]))

node3 = tf.add(node1, node2)
# print("node3:", node3)
# print("sess.run(node3):", sess.run(node3))

a = tf.placeholder(dtype=tf.float32)
b = tf.placeholder(dtype=tf.float32)

adder_node = a + b  # + provides a shortcut for tf.add(a, b)

# print (a,b, adder_node)


W = tf.Variable([.3], dtype=tf.float32)
b = tf.Variable([-.3], dtype=tf.float32)
x = tf.placeholder(tf.float32)
linear_model = W * x + b

init = tf.global_variables_initializer()
sess.run(init)
# print(sess.run(linear_model, {x: [1,2,3,4]}))

y = tf.placeholder(tf.float32)
squared_deltas = tf.square(linear_model - y)  # squares the difference between expected value and the results
# [ 0.          0.30000001  0.60000002  0.90000004] vs [0, -1, -2, -3]
loss = tf.reduce_sum(squared_deltas)  # sum of squared_deltas (1.3^2+2.6^2+3.9^2)
print("before the changes")
print(sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))

# to fix the problem manually tf.assing can be used to change the values of W and b
fix_1 = tf.assign(W, [-1])
fix_2 = tf.assign(b, [1])
sess.run([fix_1, fix_2])

print ("after modifying the value of W and b")
print(sess.run(loss, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]}))


# using training function to minimize the loss
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)
sess.run(init)
start = timeit.default_timer()
for i in range(100):
  sess.run(train, {x: [1, 2, 3, 4], y: [0, -1, -2, -3]})
stop = timeit.default_timer()
time = round((stop - start),4)

print ( "time taken = ", time, "s")
print(sess.run([W, b]))



