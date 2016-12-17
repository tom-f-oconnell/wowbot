
import time
import pyxhook
import subprocess as sp
import pyscreenshot as sc
import re
import numpy as np
import matplotlib.pyplot as plt
import warnings
import pickle

# TODO why aren't these working?
# because GTK was really verbose, and they weren't relevant
#warnings.filterwarnings("ignore")
#warnings.simplefilter("ignore", Warning)
# just using '... 2> /dev/null' for now

started = time.time()
keyset = {'w',
          'F3',
          'P_Begin',
          'space',
          '4',
          'i',
          'F4',
          'minus',
          '9',
          'Pause',
          'BackSpace',
          'P_Delete',
          'period',
          'P_End',
          't',
          'F12',
          '0',
          'q',
          'Left',
          'Return',
          'F10',
          '7',
          'Control_L',
          'Alt_L',
          '5',
          'P_Down',
          'P_Insert',
          'Scroll_Lock',
          'Home',
          'semicolon',
          'equal',
          'Down',
          'P_Page_Up',
          'd',
          'y',
          'Up',
          'P_Right',
          'k',
          'slash',
          'Delete',
          'F9',
          'Insert',
          'F6',
          'Num_Lock',
          'o',
          'P_Left',
          'e',
          'c',
          'l',
          'comma',
          'Control_R',
          'bracketright',
          'F5',
          'P_Up',
          'j',
          'Shift_L',
          'x',
          'z',
          'g',
          'F2',
          'P_Home',
          'F7',
          '1',
          'F8',
          'grave',
          'p',
          'h',
          'b',
          'P_Next',
          's',
          'Menu',
          'r',
          'Escape',
          'F11',
          'Caps_Lock',
          'Shift_R',
          'v',
          'backslash',
          'Super_L',
          'P_Subtract',
          '3',
          '2',
          'Print',
          'Alt_R',
          'F1',
          'P_Add',
          'Right',
          'P_Divide',
          'Next',
          '8',
          'P_Enter',
          'n',
          'Page_Up',
          'a',
          'f',
          'End',
          'Tab',
          'apostrophe',
          '6',
          'bracketleft',
          'u',
          'P_Multiply',
          'm'}

mouseset = {'mouse wheel down',
            'mouse wheel up',
            'mouse 8',
            'mouse 9',
            'mouse left',
            'mouse right'}

cx_re = re.compile("Absolute upper-left X:  ([0-9]+)")
cy_re = re.compile("Absolute upper-left Y:  ([0-9]+)")
h_re = re.compile("Height: ([0-9]+)")
w_re = re.compile("Width: ([0-9]+)")

out = str(sp.check_output(["xwininfo", "-name", 'World of Warcraft']))
print(out)

cx = int(cx_re.search(out).groups()[0])
cy = int(cy_re.search(out).groups()[0])
h = int(h_re.search(out).groups()[0])
w = int(w_re.search(out).groups()[0])

num_keys = len(keyset)
num_mouse_buttons = len(mouseset)

both = keyset.union(mouseset)
actionmap = dict(zip(sorted(list(both)), range(0, len(both))))

# make the inverse map for decoding the numpy matrix entries
num2key = {actionmap[k]: k for k in actionmap.keys()}

# save it for decoding in other scripts
with open("num2key.p", "wb") as p:
    pickle.dump(num2key, p)

last_action = max(actionmap.values())

max_secs = 10
# this is out of our control
byzanz_framerate = 25 #fps
dt = (1 / byzanz_framerate) # seconds
max_timesteps = max_secs / dt

filename = 'video.flv'
duration = round(dt * max_timesteps)
delay = 0
byzanz_args = ['-d', str(duration), '--delay='+str(delay), filename]

# TODO why the left and the top?
args = ['byzanz-record', '-x', str(cx), '-y', str(cy),\
    '-w', str(w), '-h', str(h)] + byzanz_args

print(args)
sp.Popen(args)

# TODO make all but mouse coords single bits
actions = np.empty([num_keys + num_mouse_buttons + 2, max_timesteps], dtype=int) * np.nan
curr = 0

missing_keys = set()
# 2 for both mouse coordinates
# may try explicitly adding derivatives later (for at least 4 total dimensions)
# but i don't have the best intuition about what is needed now

########################################################################################

# TODO might need to protect against multithreading issues
def OnKeyPress(event):
    global actions
    global curr
    global missing_keys
    
    try:
        print('pressed key ' + str(actionmap[event.Key]))
        actions[actionmap[str(event.Key)], curr] = 1
    except KeyError:
        missing_keys.add(event.Key)

def OnKeyRelease(event):
    global actions
    global curr
    global missing_keys

    try:
        print('released key ' + str(actionmap[event.Key]))
        actions[actionmap[event.Key], curr] = 0
    except KeyError:
        missing_keys.add(event.Key)

def MouseButtonUp(event):
    global actions
    global curr
    global missing_keys

    # to get rid of " up"
    m = event.MessageName[:-3]
    try:
        print('pressed ' + m + "=" + str(actionmap[m]))
        actions[actionmap[m], curr] = 1
    except KeyError:
        missing_keys.add(m)

def MouseButtonDown(event):
    global actions
    global curr
    global missing_keys

    # to get rid of " down"
    m = event.MessageName[:-5]
    try:
        print('released ' + m + "=" + str(actionmap[m]))
        actions[actionmap[m], curr] = 0
    except KeyError:
        missing_keys.add(m)

########################################################################################

#instantiate HookManager class
new_hook = pyxhook.HookManager()
#listen to all keystrokes
new_hook.KeyDown = OnKeyPress
new_hook.KeyUp = OnKeyRelease
new_hook.MouseAllButtonsUp = MouseButtonUp
new_hook.MouseAllButtonsDown = MouseButtonDown 
#hook the keyboard
new_hook.HookKeyboard()
#start the session
new_hook.start()

while curr < actions.shape[1]:
    print(str(curr) + '/' + str(max_timesteps))

    # TODO it seems as though this sum sometimes gets over zero, but is strangely not monotonically increasing. must be overwriting stuff?
    # TODO remove

    if curr >= 1:
        actions[:, curr] = actions[:, curr - 1]
    else:
        # TODO check for keys currently pressed?
        actions[:, curr] = np.zeros(actions.shape[0], dtype=int)

    print(actions[:,curr])
    print(np.sum(actions[:-2,:]))
    print(np.nansum(actions[:-2,:]))

    actions[-1, curr] = new_hook.mouse_position_y
    actions[-2, curr] = new_hook.mouse_position_x

    if len(missing_keys) > 0:
        print("MISSING KEYS:")
        print(missing_keys)
        print()

    curr = curr + 1
    # TODO verify the delay in the above portion is negligible
    time.sleep(dt)

print('SAVING DATA...')
np.save('actions', actions)

print(byzanz_framerate * max_secs)
print(np.shape(actions))

new_hook.cancel()
