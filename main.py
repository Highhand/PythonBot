"""
screen res: 1650x1050
game box    463,109      1213,109
            463,859     1213,859
spelhemsida: http://connection.ivank.net/
"""

import time # sleep
import win32gui # windowshandling (not the OS windows)

from game import Game
from mouse import mouseLeftClick, setMouseCoords

# import constants# Name of window to open and play in
_WINDOW_NAME = 'Connection - Mozilla Firefox'

def windowToForeground(winName):
    handle = win32gui.FindWindow(None, winName)
    try:
        win32gui.SetForegroundWindow(handle)
        return True
    except:
        print("There is no window with name: " + winName)
        return False

def startGame():
    # 850. 440 red level
    setMouseCoords(850,440)
    mouseLeftClick()
    time.sleep(0.5)
    # 505 290 level 1
    setMouseCoords(505,290)
    mouseLeftClick()
    time.sleep(1)

def nextLevel():
    time.sleep(0.1)
    setMouseCoords(940,680)
    time.sleep(5)
    mouseLeftClick()
    time.sleep(5)

def main():
    game = Game()
    foundWindow = windowToForeground(_WINDOW_NAME)
    if foundWindow:
        startGame()
        game.createGameboard()
        game.connectGameboard()
        # nextLevel()
        # game.createGameboard()
        # game.connectGameboard()



if __name__ == "__main__":
    main();
