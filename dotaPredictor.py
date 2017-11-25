from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
import random

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def multilayer_perceptron(x, weights, biases):
	# Hidden layer with RELU activation
	layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
	layer_1 = tf.nn.relu(layer_1)

	# Hidden layer with RELU activation
	layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
	layer_2 = tf.nn.relu(layer_2)

	# Output layer with linear activation
	out_layer = tf.matmul(layer_2, weights['out'] + biases['out'])
	return out_layer

def learnToPredictWinner(learningHeroes, learningVictories, testHeroes, testVictories):
	learning_rate = 0.001
	training_epochs = 100
	batch_size = 100
	display_step = 1

	# Network parameters
	n_hidden_1 = 10
	n_hidden_2 = 10
	n_input = 10
	n_classes = 2

	# Tensor flow graph inputs
	x = tf.placeholder(dtype = tf.float32, shape = [None, n_input])
	y = tf.placeholder(dtype = tf.float32, shape = [None, n_classes])

	# Create model
	weights = {
		'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
		'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
		'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
	}

	biases = {
		'b1': tf.Variable(tf.random_normal([n_hidden_1])),
		'b2': tf.Variable(tf.random_normal([n_hidden_2])),
		'out': tf.Variable(tf.random_normal([n_classes])),
	}

	# construct model
	pred = multilayer_perceptron(x, weights, biases)

	# cost and optimizer
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = pred, labels = y))
	optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

	init = tf.global_variables_initializer()

	print(testVictories)
	with tf.Session() as sess:
		sess.run(init)
		for epoch in range(training_epochs):			
			avg_cost = 0.
			total_batches = int(len(learningHeroes)/batch_size)
			game_batches = np.array_split(learningHeroes, total_batches)			
			victory_batches = np.array_split(learningVictories, total_batches)			
			for i in range(total_batches):				
				game_batch, batch_victories = game_batches[i], victory_batches[i]				
				_, c = sess.run([optimizer, cost], feed_dict={x: game_batch, y: batch_victories})
				avg_cost += c /total_batches
			if epoch % display_step == 0:
				print("Learning in progress")
		print("learning done finished")

		# Test model
		correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y,1))

		# Calculate accuracy
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

		print("Accuracy", accuracy.eval({x: testHeroes, y:testVictories}))