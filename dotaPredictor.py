from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import random

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

amount_of_heroes = 100 #100 Should be the amount of heroes

def get_data(amount):
	numbers = []
	labels = []
	for x in range(0,amount):
		numbers.append(random.sample(range(amount_of_heroes), 10)) 
		labels.append(random.randint(0,1))
	return numbers, labels		

testHeroes, victories = get_data(10000)
testTestHeroes, _ = get_data(10)

x = tf.placeholder(dtype = tf.float32, shape = [None, 10])
y = tf.placeholder(dtype = tf.int32, shape = [None])

logits = tf.contrib.layers.fully_connected(x, amount_of_heroes, tf.nn.relu)

loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = y, logits = logits))

train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

correct_pred = tf.argmax(logits, 1)

accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for i in range(201):
	_, loss_value = sess.run([train_op, loss], feed_dict={x: testHeroes, y:victories})
	if i % 10 == 0:
		print("Loss: ", loss_value)
	print("Done with EPOCH")

predicted = sess.run([correct_pred], feed_dict={x: testTestHeroes})[0]
print(predicted)

sess.close()