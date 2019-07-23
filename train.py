import tensorflow as tf, numpy, matplotlib.pyplot as plt


in_data = [[j for i in range(4)] for j in range(100)]
out_data = [[i] for i in range(100)]


x = tf.placeholder(tf.float32, shape=[None,4])
y = tf.placeholder(tf.float32, shape=[None,1])

w1 = tf.Variable(tf.truncated_normal([4,16],stddev=0.01))
b1 = tf.Variable(tf.constant(0.0, shape=[16]))
h1 = tf.matmul(x,w1)+b1


w2 = tf.Variable(tf.truncated_normal([16,16],stddev=0.01))
b2 = tf.Variable(tf.constant(0.0, shape=[16]))
y_ = tf.matmul(h1,w2)+b2

loss = tf.sqrt(tf.reduce_mean(tf.pow(y-y_,2)))

train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

print(in_data)
print(out_data)

l = []
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(10000):
        train_step.run(feed_dict={x:in_data,y:out_data})
        l.append(loss.eval( feed_dict={x:in_data,y:out_data}))      

x_axis = [i for i in range(len(l))]
plt.figure()
plt.plot(x_axis, l)
plt.show()
