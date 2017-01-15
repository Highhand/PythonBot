
import time
import win32api #
import win32con # datatypes for the windows api

from enums import Direction

# Returns x and y pos of cursor
def getMouseCoords():
    x,y = win32api.GetCursorPos()
    return x,y

def setMouseCoords(x,y):
    win32api.SetCursorPos((x,y))

def mouseLeftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)

def mouseLeftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def mouseLeftClick():
    time.sleep(0.1)
    mouseLeftDown()
    time.sleep(0.1)
    mouseLeftUp()

def mouseDrag(direction, distance):
    time.sleep(0.1)
    mouseLeftDown()
    counter = distance
    while (counter > 0):
        x,y = getMouseCoords()
        if (direction == Direction.up):
            y-=1
        elif (direction == Direction.right):
            x+=1
        elif (direction == Direction.down):
            y+=1
        elif (direction == Direction.left):
            x-=1
        setMouseCoords(x,y)
        counter-=1
    mouseLeftUp()
