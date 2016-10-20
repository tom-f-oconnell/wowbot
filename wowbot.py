
import time
import pyxhook
import subprocess
import pyscreenshot as sc
import re
import numpy as np
import matplotlib.pyplot as plt

started = time.time()
keyset = {'F3',
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
          'w',
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

keymap = dict(zip(sorted(list(keyset)), range(0,len(keyset))))

mouseset = {'mouse wheel down',
            'mouse wheel up',
            'mouse 8',
            'mouse 9',
            'mouse left',
            'mouse right'}

mousemap = dict(zip(sorted(list(mouseset)), range(0,len(mouseset))))

dt = 0.2 # seconds
num_keys = len(keyset)
#num_mouse_buttons = 

keys = None
actions = None

def init_keys():
    global keys
    keys = np.zeros(num_keys, 1)

def OnKeyPress(event):
    global keys
    
    if keys is None:
        init_keys()

    print('pressed key ' + str(keymap[event.key]))

# TODO hopefully this works?
def OnKeyRelease(event):
    global keys

    if keys is None:
        init_keys()

    print('released key ' + str(keymap[event.key]))

def MouseButtonUp(event):
    global mouse

    event.MessageName[:-3]

def MouseButtonDown(event):
    global mouse

    event.MessageName[:-5]

cx_re = re.compile("Absolute upper-left X:  ([0-9]+)")
cy_re = re.compile("Absolute upper-left Y:  ([0-9]+)")
h_re = re.compile("Height: ([0-9]+)")
w_re = re.compile("Width: ([0-9]+)")

out = str(subprocess.check_output(["xwininfo", "-name", 'World of Warcraft']))
print(out)

cx = int(cx_re.search(out).groups()[0])
cy = int(cy_re.search(out).groups()[0])
h = int(h_re.search(out).groups()[0])
w = int(w_re.search(out).groups()[0])

# 1 Gbyte
max_array_size_bytes = 1e9
# uint8 should be 1 byte per point
max_timesteps = max_array_size_bytes / (h * w)

#instantiate HookManager class
new_hook = pyxhook.HookManager()
#listen to all keystrokes
new_hook.KeyDown = OnKeyPress
new_hook.KeyUp = OnKeyRelease
#hook the keyboard
new_hook.HookKeyboard()
#start the session
new_hook.start()


print("after starting hook manager")

raw = sc.grab(bbox=(cx, cy, cx+w, cy+h))

img = np.asarray(raw)
#plt.imshow(img)
#plt.show()
#raw.save('sc.png')


