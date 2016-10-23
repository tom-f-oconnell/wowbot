#!/usr/bin/env python3

import Xlib
from Xlib import XK, display, ext, X, protocol
import sys
import time

def stop_grab(display):
    display.ungrab_keyboard(X.CurrentTime)
    display.flush()

def send_key(d, root, win, keycode):
    #store current input focus
    currentfocus=d.get_input_focus()

    #set input focus to selected window
    d.set_input_focus(win, X.RevertToParent, X.CurrentTime)

    print('sending ' + str(keycode))

    #send keypress and keyrelease
    if type(keycode) == tuple:
        ext.xtest.fake_input(win, X.KeyPress, keycode[0])
        ext.xtest.fake_input(win, X.KeyRelease, keycode[1])
        ext.xtest.fake_input(win, X.KeyPress, keycode[0])
        ext.xtest.fake_input(win, X.KeyRelease, keycode[1])
    else:
        ext.xtest.fake_input(win, X.KeyPress, keycode)
        ext.xtest.fake_input(win, X.KeyRelease, keycode)

    #revert focus to original window
    d.set_input_focus(currentfocus.focus,X.RevertToParent,X.CurrentTime)

    d.sync()

# from http://shallowsky.com/software/crikey/pykey-0.1 
def send_press(window, keycode):
    shift_mask = 0 # or Xlib.X.ShiftMask
    #shift_mask = Xlib.X.ShiftMask

    #window = display.get_input_focus()._data["focus"]
    #keysym = Xlib.XK.string_to_keysym(emulated_key)
    #keycode = display.keysym_to_keycode(keysym)
    event = Xlib.protocol.event.KeyPress(
        time = int(time.time()),
        #time = X.CurrentTime,
        root = root,
        window = window,
        same_screen = 1, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        #mode = X.NotifyUngrab,
        detail = keycode
    )
    print(dir(event))
    print(event._data)
    print(event._fields)
    print('sending press')
    window.send_event(event, propagate = True)

def send_release(window, keycode):
    shift_mask = 0 # or Xlib.X.ShiftMask
    print('making release event')
    event = Xlib.protocol.event.KeyRelease(
        time = int(time.time()),
        #root = display.screen().root,
        root = root,
        window = window,
        same_screen = 1, child = Xlib.X.NONE,
        root_x = 0, root_y = 0, event_x = 0, event_y = 0,
        state = shift_mask,
        #mode = Xlib.X.NotifyUngrab,
        detail = keycode
    )
    print('sending release')
    window.send_event(event, propagate = True)

def get_window(display, name):
    root_win = display.screen().root 
    window_list = [root_win]

    while len(window_list) != 0:
        win = window_list.pop(0)
        if win.get_wm_name() == name:
            return win
        elif win.get_wm_name() == None:
            children = win.query_tree().children
            if children != None:
                window_list += children
        continue


    # not using this anymore, dont think
    if win.get_wm_name().find(name) != -1:
        return win
    children = win.query_tree().children
    if children != None:
        window_list += children

    print('Unable to find window matching - %s\n' % name)
    sys.exit(1)

"""
try:
    window_name_str = sys.argv[1]
except:
    print "<script> <window name string>"
    sys.exit(1)
"""

d = display.Display()
root = d.screen().root
win = get_window(d, "World of Warcraft")
print(win.get_wm_name())

root.change_attributes(event_mask = X.KeyPressMask | X.KeyReleaseMask)

currentfocus = None

print("Press <ESC> or Ctrl+C to quit")
while True:
    print(1)

    try:
        root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
        event = root.display.next_event()
    except KeyboardInterrupt:
        break

    print(2)

    if event.type == X.KeyRelease:
        currentfocus = d.get_input_focus()

    print(3)

    # If current focused window is the window to which you are sending keys, then don't do anything
    #if currentfocus != None and currentfocus.focus == win:
    #    continue

    print(4)

    try:
        if event.detail == 9:
            stop_grab(d)
            break
        else:
            print(5)
            keycode = event.detail
            print(6)

            # Ignore alt-tab, as that would be problematic to handle
            if (keycode == 64) or (keycode == 23):
                continue
            print(7)
            stop_grab(d)
            #send_key(d, root, win, keycode)
            print('SENDING KEYCODE: ' + str(keycode))
            send_press(win, keycode)
            send_release(win, keycode)
            
            # TODO why is this never reached?
            print('DONE SENDING')

    except AttributeError:
        print('no detail')
