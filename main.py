"""mousemacro.py defines the following functions:

click() -- calls left mouse click
hold() -- presses and holds left mouse button
release() -- releases left mouse button

rightclick() -- calls right mouse click
righthold() -- calls right mouse hold
rightrelease() -- calls right mouse release

middleclick() -- calls middle mouse click
middlehold() -- calls middle mouse hold
middlerelease() -- calls middle mouse release

move(x,y) -- moves mouse to x/y coordinates (in pixels)
getpos() -- returns mouse x/y coordinates (in pixels)
slide(x,y) -- slides mouse to x/y coodinates (in pixels)
              also supports optional speed='slow', speed='fast'
"""

from ctypes import*
from ctypes.wintypes import *
import time
from time import sleep
import win32.win32api as win32api
import win32.lib.win32con as win32con

__all__ = ['click', 'hold', 'release', 'rightclick', 'righthold', 'rightrelease', 'middleclick', 'middlehold', 'middlerelease', 'move', 'slide', 'getpos']

# START SENDINPUT TYPE DECLARATIONS
PUL = POINTER(c_ulong)

class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
             ("wScan", c_ushort),
             ("dwFlags", c_ulong),
             ("time", c_ulong),
             ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
             ("wParamL", c_short),
             ("wParamH", c_ushort)]

class MouseInput(Structure):
    _fields_ = [("dx", c_long),
             ("dy", c_long),
             ("mouseData", c_ulong),
             ("dwFlags", c_ulong),
             ("time",c_ulong),
             ("dwExtraInfo", PUL)]

class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
              ("mi", MouseInput),
              ("hi", HardwareInput)]

class Input(Structure):
    _fields_ = [("type", c_ulong),
             ("ii", Input_I)]

class POINT(Structure):
    _fields_ = [("x", c_ulong),
             ("y", c_ulong)]
# END SENDINPUT TYPE DECLARATIONS

  #  LEFTDOWN   = 0x00000002,
  #  LEFTUP     = 0x00000004,
  #  MIDDLEDOWN = 0x00000020,
  #  MIDDLEUP   = 0x00000040,
  #  MOVE       = 0x00000001,
  #  ABSOLUTE   = 0x00008000,
  #  RIGHTDOWN  = 0x00000008,
  #  RIGHTUP    = 0x00000010

MIDDLEDOWN = 0x00000020
MIDDLEUP   = 0x00000040
MOVE       = 0x00000001
ABSOLUTE   = 0x00008000
RIGHTDOWN  = 0x00000008
RIGHTUP    = 0x00000010


FInputs = Input * 2
extra = c_ulong(0)

click = Input_I()
click.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
release = Input_I()
release.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))

x = FInputs( (0, click), (0, release) )
#user32.SendInput(2, pointer(x), sizeof(x[0])) CLICK & RELEASE

x2 = FInputs( (0, click) )
#user32.SendInput(2, pointer(x2), sizeof(x2[0])) CLICK & HOLD

x3 = FInputs( (0, release) )
#user32.SendInput(2, pointer(x3), sizeof(x3[0])) RELEASE HOLD


def move(x,y):
    windll.user32.SetCursorPos(x,y)

def getpos():
    global pt
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y
'''
def slide(a,b,speed=0):
    while True:
        if speed == 'slow':
            sleep(0.005)
            Tspeed = 2
        if speed == 'fast':
            sleep(0.001)
            Tspeed = 5
        if speed == 0:
            sleep(0.001)
            Tspeed = 3

        x = getpos()[0]
        y = getpos()[1]
        if abs(x-a) < 5:
            if abs(y-b) < 5:
                break

        if a < x:
            x -= Tspeed
        if a > x:
            x += Tspeed
        if b < y:
            y -= Tspeed
        if b > y:
            y += Tspeed
        move(x,y)
'''

def click(x,y):
    print('click event')
    #windll.user32.SendInput(2,pointer(x),sizeof(x[0]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.005)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

'''
def hold():
    windll.user32.SendInput(2, pointer(x2), sizeof(x2[0]))

def release():
    windll.user32.SendInput(2, pointer(x3), sizeof(x3[0]))


def rightclick():
    windll.user32.mouse_event(RIGHTDOWN,0,0,0,0)
    windll.user32.mouse_event(RIGHTUP,0,0,0,0)

def righthold():
    windll.user32.mouse_event(RIGHTDOWN,0,0,0,0)

def rightrelease():
    windll.user32.mouse_event(RIGHTUP,0,0,0,0)


def middleclick():
    windll.user32.mouse_event(MIDDLEDOWN,0,0,0,0)
    windll.user32.mouse_event(MIDDLEUP,0,0,0,0)

def middlehold():
    windll.user32.mouse_event(MIDDLEDOWN,0,0,0,0)

def middlerelease():
    windll.user32.mouse_event(MIDDLEUP,0,0,0,0)
'''


operating_window = []

def convert_to_pixels(percentageX, percentageY):
    xDiff = operating_window[2] - operating_window[0]
    yDiff = operating_window[3] - operating_window[1]
    pixel_value_x = round(operating_window[0] + xDiff * percentageX)
    pixel_value_y = round(operating_window[1] + yDiff * percentageY)
    return {pixel_value_x, pixel_value_y}

def start_game_loop():
    '''This function handles the logic of the game'''

    # first we have to click the start game button
    x, y = convert_to_pixels(0.75, 0.8) 
    print(x,y)
    move(x, y)
    time.sleep(1)
    click(x, y)

    # then click skip button
    time.sleep(3)
    x, y = convert_to_pixels(0.95, 0.95) 
    print(x,y)
    move(x, y)
    click(x, y)

    # then mouse click to begin
    time.sleep(1)
    click(x, y)

    # then wait till turn
    time.sleep(6)

    #click skip at bottom left
    x, y = convert_to_pixels(0.05, 0.95) 
    print(x,y)
    move(x, y)
    click(x, y)

    # now the shots can be fired
    time.sleep(2)
    x, y = convert_to_pixels(0.65, 0.62)
    print(x,y)
    move(x, y)
    click(x, y)

    # now the shots can be fired
    time.sleep(15)
    x, y = convert_to_pixels(0.65, 0.62)
    print(x,y)
    move(x, y)
    click(x, y)

    # now the shots can be fired
    time.sleep(15)
    click(x, y)


if __name__ == '__main__':

    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    clickCount = 2
    while clickCount > 0:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            if a < 0:
                x,y = getpos()
                operating_window.append(x)
                operating_window.append(y)
                clickCount = clickCount - 1
                print('clicked')
                
        time.sleep(0.001)

    print(operating_window)
    start_game_loop()
