
import pyscreenshot # grab()
import math # infinity

from enums import Color, Direction, MapObject
from mouse import mouseDrag, setMouseCoords
import screenshot

# Board width/height in number of blocks
_BOARD_WIDTH_BLOCK = 6
_BOARD_HEIGHT_BLOCK = 6

# RGB
_COLOR_RED = (221, 34, 0)
_COLOR_GREEN = (34, 204, 0)
_COLOR_DARKBLUE = (34, 34, 221)
_COLOR_LIGHTBLUE = (0, 221, 221)
_COLOR_YELLOW = (238, 238, 0)
_COLOR_PURPLE = (170, 0, 170)

class Game():

    def __init__(self):
        self.gameboard = []
        self.unconnectedColors = [Color.red, Color.green, Color.darkblue, Color.lightblue, Color.yellow, Color.purple]
        self.xPadding = 0
        self.yPadding = 0
        self.width = 0
        self.height = 0
        self.blocksize = 0
        # self.unconnectedColors = [Color.green]

    # Assumes game window is in the foreground
    # A gameboard position consist of a dictionary with information about
    # object on that position such as color, type, parent x and ycoords and distance
    # where the last three are used in findPath (Dijkstras)
    def createGameboard(self):

        fullscreenImage=pyscreenshot.grab()
        x1 = screenshot.getLeftside(fullscreenImage)
        y1 = screenshot.getTop(fullscreenImage)
        x2 = screenshot.getRightside(fullscreenImage)
        y2 = screenshot.getBottom(fullscreenImage)
        gameboardImage=pyscreenshot.grab(bbox=(x1,y1,x2,y2))
        self.xPadding = x1
        self.yPadding = y1
        self.width = x2-x1
        self.height = y2-y1
        self.blocksize = self.width/_BOARD_WIDTH_BLOCK
        self.gameboard = [[0 for x in range(_BOARD_WIDTH_BLOCK)] for y in range(_BOARD_HEIGHT_BLOCK)]
        for y in range(_BOARD_HEIGHT_BLOCK):
            for x in range(_BOARD_WIDTH_BLOCK):
                # Magic number five is offset to ensure a blob is sampled correctly, remove it and in some cases a blob is missed
                magicNum = 10
                color = gameboardImage.getpixel((self.blocksize/2+x*self.blocksize, self.blocksize/2+y*self.blocksize+magicNum))
                if(color == _COLOR_RED):
                    self.gameboard[y][x] = {'color': Color.red, 'objectType': MapObject.blob, 'coords': (x,y) ,'parentX': None, 'parentY': None, 'distance':-1}
                elif(color == _COLOR_GREEN):
                    self.gameboard[y][x] = {'color': Color.green, 'objectType': MapObject.blob, 'coords': (x,y) ,'parentX': None, 'parentY': None, 'distance':-1}
                elif(color == _COLOR_DARKBLUE):
                    self.gameboard[y][x] = {'color': Color.darkblue, 'objectType': MapObject.blob, 'coords': (x,y) ,'parentX': None, 'parentY': None, 'distance':-1}
                elif(color == _COLOR_LIGHTBLUE):
                    self.gameboard[y][x] = {'color': Color.lightblue, 'objectType': MapObject.blob, 'coords': (x,y) ,'parentX': None, 'parentY': None, 'distance':-1}
                elif(color == _COLOR_YELLOW):
                    self.gameboard[y][x] = {'color': Color.yellow, 'objectType': MapObject.blob, 'coords': (x,y) ,'parentX': None, 'parentY': None, 'distance':-1}
                elif(color == _COLOR_PURPLE):
                    self.gameboard[y][x] = {'color': Color.purple, 'objectType': MapObject.blob, 'coords': (x,y) ,'parentX': None, 'parentY': None, 'distance':-1}
                else:
                    self.gameboard[y][x] = {'color': Color.colorless, 'objectType': MapObject.empty, 'coords': (x,y) ,'parentX': None, 'parentY': None, 'distance':-1}

    def printBoard(self):
        for y in range(_BOARD_HEIGHT_BLOCK):
            for x in range(_BOARD_WIDTH_BLOCK):
                print(self.gameboard[y][x]['color'].name, end=" ")
            print()

    # Resets all path of a certain color
    def clearColor(self, color):
        for y in range(_BOARD_HEIGHT_BLOCK):
            for x in range(_BOARD_WIDTH_BLOCK):
                if self.gameboard[y][x]['color'] == color and self.gameboard[y][x]['objectType'] == MapObject.path:
                    self.gameboard[y][x]['color'] = Color.colorless
                    self.gameboard[y][x]['objectType'] = MapObject.empty

    # Dijkstras bredsida
    # Finds shortest path from (startX,startY) to the nearest blob of the same color
    # Returns stack where the start pos is at the top and the goal at the bottom
    # OBS a reference to gameboard is sent! or atleast a reference to its mutable parts???
    def findPath(self,startX,startY,ignorePaths):
        # Reset all node in the gameboard
        for y in range(_BOARD_HEIGHT_BLOCK):
            for x in range(_BOARD_WIDTH_BLOCK):
                self.gameboard[y][x]['parentX'] = None
                self.gameboard[y][x]['parentY'] = None
                self.gameboard[y][x]['distance'] = math.inf

        # Init startnode
        color = self.gameboard[startY][startX]['color']
        self.gameboard[startY][startX]['distance'] = 0
        # List of node that have not been visited
        unvisited = [self.gameboard[startY][startX]]

        while unvisited:
            unvisited.sort(key= lambda dictEntry: dictEntry['distance']) # Sort after distance which is index 2 in tuple
            current = unvisited.pop(0)
            x = current['coords'][0]
            y = current['coords'][1]
            dist = current['distance']

            # If found goal stop looking
            if (not(x == startX) or not(y == startY)) and current['color'] == color and current['objectType'] == MapObject.blob:
                break

            # Update up
            tmpX = x
            tmpY = y-1
            if tmpY>=0 and self.gameboard[tmpY][tmpX]['distance'] > dist+1:
                if self.gameboard[tmpY][tmpX]['objectType'] == MapObject.empty or self.gameboard[tmpY][tmpX]['color'] == color or (ignorePaths and self.gameboard[tmpY][tmpX]['objectType'] == MapObject.path):
                    self.gameboard[tmpY][tmpX]['parentX'] = x
                    self.gameboard[tmpY][tmpX]['parentY'] = y
                    self.gameboard[tmpY][tmpX]['distance'] = dist+1
                    unvisited.append(self.gameboard[tmpY][tmpX])

            # right
            tmpX = x+1
            tmpY = y
            if tmpX<_BOARD_WIDTH_BLOCK and self.gameboard[tmpY][tmpX]['distance'] > dist+1:
                if self.gameboard[tmpY][tmpX]['objectType'] == MapObject.empty or self.gameboard[tmpY][tmpX]['color'] == color or (ignorePaths and self.gameboard[tmpY][tmpX]['objectType'] == MapObject.path):
                    self.gameboard[tmpY][tmpX]['parentX'] = x
                    self.gameboard[tmpY][tmpX]['parentY'] = y
                    self.gameboard[tmpY][tmpX]['distance'] = dist+1
                    unvisited.append(self.gameboard[tmpY][tmpX])

            # down
            tmpX = x
            tmpY = y+1
            if tmpY<_BOARD_HEIGHT_BLOCK and self.gameboard[tmpY][tmpX]['distance'] > dist+1:
                if self.gameboard[tmpY][tmpX]['objectType'] == MapObject.empty or self.gameboard[tmpY][tmpX]['color'] == color or (ignorePaths and self.gameboard[tmpY][tmpX]['objectType'] == MapObject.path):
                    self.gameboard[tmpY][tmpX]['parentX'] = x
                    self.gameboard[tmpY][tmpX]['parentY'] = y
                    self.gameboard[tmpY][tmpX]['distance'] = dist+1
                    unvisited.append(self.gameboard[tmpY][tmpX])

            # left
            tmpX = x-1
            tmpY = y
            if tmpX>=0 and self.gameboard[tmpY][tmpX]['distance'] > dist+1:
                if self.gameboard[tmpY][tmpX]['objectType'] == MapObject.empty or self.gameboard[tmpY][tmpX]['color'] == color or (ignorePaths and self.gameboard[tmpY][tmpX]['objectType'] == MapObject.path):
                    self.gameboard[tmpY][tmpX]['parentX'] = x
                    self.gameboard[tmpY][tmpX]['parentY'] = y
                    self.gameboard[tmpY][tmpX]['distance'] = dist+1
                    unvisited.append(self.gameboard[tmpY][tmpX])

        # When goal has been reached unravel path by adding current positions coords to the stack
        # then set current pos to parent and repeat until start positions is reached
        pathStack = []
        coordTuple = current['coords']
        pathStack.append(coordTuple)
        while not(coordTuple==self.gameboard[startY][startX]['coords']):
            current = self.gameboard[current['parentY']][current['parentX']]
            coordTuple = current['coords']
            pathStack.append(coordTuple)
            # If cross over another colors then add that color to unconnectedColors
            if not(current['color'] == Color.colorless) and current['color'] not in self.unconnectedColors:
                self.unconnectedColors.append(current['color'])
                self.clearColor(current['color'])

        # print(pathStack)
        return pathStack

    # Takes a stack of coordinates and drags the cursor from the coords at the top of the stack to the bottom
    def connectPath(self, pathStack):

        # debug
        import time
        time.sleep(0.1)

        currPos = pathStack.pop()
        currColor = self.gameboard[currPos[1]][currPos[0]]['color']
        setMouseCoords(self.xPadding+int(self.blocksize/2)+currPos[0]*self.blocksize, self.yPadding+int(self.blocksize/2)+currPos[1]*self.blocksize)
        prevPos = currPos
        while pathStack:
            currPos = pathStack.pop()
            # Mark new positions as a path
            self.gameboard[currPos[1]][currPos[0]]['color'] = currColor
            # Dont change to path if goal position since it is and must remain a blob
            if pathStack:
                self.gameboard[currPos[1]][currPos[0]]['objectType'] = MapObject.path

            if currPos[1]==prevPos[1]-1:#up
                mouseDrag(Direction.up,self.blocksize)
            elif currPos[0]==prevPos[0]+1: #right
                mouseDrag(Direction.right,self.blocksize)
            elif currPos[1]==prevPos[1]+1:#down
                mouseDrag(Direction.down,self.blocksize)
            elif currPos[0]==prevPos[0]-1:#left
                mouseDrag(Direction.left,self.blocksize)
            prevPos = currPos

    # Goes through the gameboard and finds one path between every pair of blobs
    def connectGameboard(self):
        # List of already finished colors
        # uncompletedColors = [Color.red, Color.green, Color.darkblue, Color.lightblue, Color.yellow, Color.purple]
        tries = 3
        prevUnconnectedColors = []
        while not(self.unconnectedColors==prevUnconnectedColors) and tries>0:
            prevUnconnectedColors = list(self.unconnectedColors)
            tries-=1
            for y in range(_BOARD_HEIGHT_BLOCK):
                for x in range(_BOARD_WIDTH_BLOCK):
                    if self.gameboard[y][x]['objectType'] == MapObject.blob and self.gameboard[y][x]['color'] in self.unconnectedColors:
                        path = self.findPath(x,y,False)
                        # If the path is only the start pos (len 1) or if the goal pos is not a blob
                        if(len(path) <= 1 or not(self.gameboard[path[0][1]][path[0][0]]['objectType'] == MapObject.blob)):
                            # print("disregarding: ",self.gameboard[y][x]['color']," goal: ",self.gameboard[path[0][1]][path[0][0]])
                            path = self.findPath(x,y,True)
                            # print("connecting: ",self.gameboard[y][x]['color']," goal: ",self.gameboard[path[0][1]][path[0][0]])
                        self.connectPath(path)
                        self.unconnectedColors.remove(self.gameboard[y][x]['color'])
            # print(self.unconnectedColors, prevUnconnectedColors)
