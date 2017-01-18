import pyscreenshot
import os
from win32api import GetSystemMetrics

def getTop(image):
    xOffset = int(GetSystemMetrics(0)/2)
    currentY = 100
    while(currentY < GetSystemMetrics(1)):
        color = image.getpixel((xOffset,currentY))
        if(color == (255,255,255)):
            break
        currentY+=1
    return currentY

def getRightside(image):
    currentX = int(GetSystemMetrics(0)-GetSystemMetrics(0)/5)
    yOffset = int(GetSystemMetrics(1)/3)
    while(currentX > 0):
        color = image.getpixel((currentX,yOffset))
        if(color == (255,255,255)):
            break
        currentX-=1
    return currentX

def getBottom(image):
    xOffset = int(GetSystemMetrics(0)/2)
    currentY = GetSystemMetrics(1)-75
    while(currentY > 0):
        color = image.getpixel((xOffset,currentY))
        if(color == (255,255,255)):
            break
        currentY-=1
    return currentY

def getLeftside(image):
    currentX = int(GetSystemMetrics(0)/5)
    yOffset = int(GetSystemMetrics(1)/3)
    while(currentX < GetSystemMetrics(0)):
        color = image.getpixel((currentX,yOffset))
        if(color == (255,255,255)):
            break
        currentX+=1
    return currentX
