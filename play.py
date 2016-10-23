#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import time

imgs = np.load('video.dat.npy')
actions = np.load('actions.dat.npy')
print(np.nansum(np.nansum(actions)))
print(np.sum(np.sum(np.isnan(actions))))

dt = 0.2
curr = 0

while curr < imgs.shape[3]:
    plt.imshow(imgs[:,:,:,curr])
    plt.show()
    print(actions[:,curr])
    curr = curr + 1
    time.sleep(dt)
