#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import imageio
import os.path

from scipy.interpolate import UnivariateSpline

from nnet import layers
from nnet import neuralnetwork
#import nn

actions = np.load('actions.npy')
# essentially (not actually 'one') hot encoding the keys
# cursor coordinates is a pair of integers
actions = np.concatenate((np.sign(actions[:-2,:]), actions[-2:]))

expanded_vid_filename = 'interpolated_vid'

if not os.path.isfile(expanded_vid_filename + '.npy'):
    vid = imageio.get_reader('video.flv', 'ffmpeg')
    frame_shape = np.shape(vid.get_data(0))
    vid_data = np.empty((frame_shape[0], frame_shape[1], frame_shape[2], vid.get_length())) * np.nan
    expanded = np.empty((frame_shape[0], frame_shape[1], frame_shape[2], actions.shape[1])) * np.nan

    curr = 0
    while curr < vid.get_length():
        vid_data[:,:,:,curr] = vid.get_data(curr)
        curr = curr + 1

    # adapted from AGML SO answer
    existing_length = vid.get_length()
    new_length = np.shape(actions)[1]
    old_indices = np.arange(0, existing_length)
    new_indices = np.linspace(0, existing_length - 1, new_length)

    # TODO parallelize
    # more pythonic way to do this? (looping over each index of a numpy tensor)
    for i in range(np.shape(vid_data)[0]):
        for j in range(np.shape(vid_data)[1]):
            for k in range(np.shape(vid_data)[2]):
                #print(i, j, k)
                spl = UnivariateSpline(old_indices, vid_data[i,j,k,:], k=3, s=0)
                expanded[i,j,k,:] = spl(new_indices)
        print(str(i) + '/' + str(np.shape(vid_data)[0]))

    np.save('interpolated_vid', expanded)
else:
    # TODO this correct?
    expanded = np.load(expanded_vid_filename + '.npy')

retrain_all = True
compare_performance = False

# TODO fix expand images to deal with arbitrary input dimensions

# simple feedforward net
# with single frames predicting single timestamps of keyboard / mouse data

ff_fname = 'W_ff'
# want to save any other information to make additional training on same model easier?
if retrain_all or os.path.isfile(ff_fname):
    '''
    # using my nn functions from the 187 assignment
    iterations = 4000
    # just for the hidden layers
    dims = [10, 10]
    # what if iterations > / < # examples?
    W_ff, _, _ =  nn.train_net(expanded, actions, dims, iterations)
    '''
    
    # using nnet functions adapted from andersbll's Github
    weight_scale = 2
    units1 = 200
    units2 = 30

    l1 = layers.Linear(units1, weight_scale)
    # TODO unclear how to specify dimensions for this subclass of Layer?
    l2 = layers.Activation('sigmoid')
    l3 = layers.Linear(units1, units2)
    l4 = layers.LogRegression()

    layers = [l1, l2, l3, l4]
    net_ff = neuralnetwork.NeuralNetwork(layers)

    print('Fitting neural network...')
    net_ff.fit(expanded, actions)

    np.save(ff_fname, net_ff)

if compare_performance:
    # TODO replay with correct dt (in a separate file that loads models)
    # could evaluate performance without trying to control anything
    # could make a hold out set and then train on everything after evaluating performance?
    #ff_action_est = nn.eval_net(W_ff, expanded)
    'nop'



# convolutional net still with only a single frame as input to one prediction


# recurrent simple FF net
# no attempt (as in GRU / LSTM) to resolve vanishing gradient problem (naive architecture)


# recurrent conv net


# GRU


# LSTM

