#!/usr/bin/env python3

import Xlib
from Xlib import XK, display, ext, X, protocol
import sys
import time
import subprocess as sp
import re

def stop_grab(display):
    display.ungrab_keyboard(X.CurrentTime)
    display.flush()

"""
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
"""

def send_key(window, keycode, delay=0):
    send_press(window, keycode)
    time.sleep(delay)
    send_release(window, keycode)

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
    """
    print(dir(event))
    print(event._data)
    print(event._fields)
    print('sending press')
    """
    window.send_event(event, propagate = True)

def send_release(window, keycode):
    shift_mask = 0 # or Xlib.X.ShiftMask
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
    #print('sending release')
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

def get_windows(display, name):
    root_win = display.screen().root 
    window_list = [root_win]
    windows = []

    while len(window_list) != 0:
        win = window_list.pop(0)
        if win.get_wm_name() == name:
            windows.append(win)
        elif win.get_wm_name() == None:
            children = win.query_tree().children
            if children != None:
                window_list += children
        continue

    return windows

    # TODO why is this still here?
    # not using this anymore, dont think
    if win.get_wm_name().find(name) != -1:
        return win
    children = win.query_tree().children
    if children != None:
        window_list += children

    print('Unable to find window matching - %s\n' % name)
    sys.exit(1)

def get_window_ids():
    out = str(sp.check_output(('wmctrl', '-l')))
    r = re.compile("(0x........)\ \ 0\ blackbox\ World\ of\ Warcraft")
    return r.findall(out)

def change_focus_to_id(ID):
    sp.Popen(("wmctrl", "-i", "-a", ID))

def clear_focus():
    sp.Popen(("wmctrl", "-a", "Desktop"))

"""
try:
    window_name_str = sys.argv[1]
except:
    print "<script> <window name string>"
    sys.exit(1)
"""

d = display.Display()
root = d.screen().root
#win = get_window(d, "World of Warcraft")
windows = get_windows(d, "World of Warcraft")
#wids = get_window_ids()
#quit()

print("FOUND " + str(len(windows)) + " WINDOWS")

root.change_attributes(event_mask = X.KeyPressMask | X.KeyReleaseMask)
currentfocus = None
switching_period = 0.15

print("Press <ESC> or Ctrl+C to quit")
while True:
    try:
        root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
        event = root.display.next_event()
    except KeyboardInterrupt:
        break

    if event.type == X.KeyRelease:
        currentfocus = d.get_input_focus()

    # If current focused window is the window to which you are sending keys, then don't do anything
    #if currentfocus != None and currentfocus.focus == win:
    #    continue

    try:
        if event.detail == 9:
            stop_grab(d)
            break
        else:
            keycode = event.detail

            # Ignore alt-tab, as that would be problematic to handle
            if (keycode == 64) or (keycode == 23):
                continue

            stop_grab(d)
            #send_key(d, root, win, keycode)

            print("KEYCODE=" + str(keycode))

            #if keycode == 49 or keycode == 10 or keycode == 21:
            if event.type == X.KeyPress:
                #print('SENDING KEYCODE: ' + str(keycode))
                for win in windows:
                    ID = '0x0' + format(win.__window__(), '02x')
                    change_focus_to_id(ID)

                    # didn't seem to work
                    #d.set_input_focus(win, X.RevertToNone, X.CurrentTime)
                    #d.set_input_focus(win, X.RevertToParent, int(time.time()))

                    #send_press(win, keycode)
                    send_key(win, keycode)

                    time.sleep(switching_period)
                clear_focus()
            elif event.type == X.KeyRelease:
                for win in windows:
                    ID = '0x0' + format(win.__window__(), '02x')
                    change_focus_to_id(ID)

                    # didn't seem to work
                    #d.set_input_focus(win, X.RevertToNone, X.CurrentTime)
                    #d.set_input_focus(win, X.RevertToParent, int(time.time()))

                    #send_release(win, keycode)
                    time.sleep(switching_period)
                # TODO just return to same focus
                clear_focus()

    except AttributeError:
        print('no detail')

