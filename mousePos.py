
import win32api #
import time

while 1:
    time.sleep(0.5)
    x,y = win32api.GetCursorPos()
    print(x,y)
