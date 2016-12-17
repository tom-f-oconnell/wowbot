#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import imageio

from scipy.interpolate import UnivariateSpline

def update(*args):
    global curr

    # TODO deal with end boundary
    im.set_array(vid.get_data(curr))
    print(actions[:,curr])
    curr = curr + 1

    if curr == vid.get_length():
        quit()

    return im,

actions = np.load('actions.npy')
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

print(np.nansum(np.nansum(actions)))
print(np.sum(np.sum(np.isnan(actions))))
print(actions.shape)
print(vid.get_length())

dt = 1/25
curr = 0

fig = plt.figure()
fig.canvas.set_window_title('Training actions')

ax = plt.gca()
im = ax.imshow(vid.get_data(curr))
ax.axis('off')
'''
# this fucks things up before imshow and has no effect after... why?
ax.axis('tight')
'''

# TODO not sure interval is correct
ani = animation.FuncAnimation(fig, update, interval=(dt * 1000), blit=True)
plt.show()
