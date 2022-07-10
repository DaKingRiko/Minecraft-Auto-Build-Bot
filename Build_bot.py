from asyncio.windows_events import NULL
import time
import sys
import keyboard # pip3 install keyboard 
import pyautogui  # pip3 install pyautogui 
import math
from colors import *
import PIL
from functools import partial
PIL.ImageGrab.grab = partial(PIL.ImageGrab.grab, all_screens=True)

'''
Goals for today:

x  get a second output image that shows what colors to get
+  have the bot give put the needed blocks into your inventory
_  stabilize building
_  get input picture from google
+  write algo that takes multiple colors and gets the 9 most used ones
+  use cli args for file and build size
'''

'''
check if a position is in a array
@position : an array with 2 items in it
@visited : an array
'''
def notinvisited(position, visited):
    for it in visited:
        if position[0] == it[0] and position[1] == it[1]:       
            return False
    return True

'''
checks if the rest of the array is full of zeroes. Used for clearing backgrounds
@arr : array we are checking
@start : position we are starting to check at
'''
def restIsZero(arr, start):
    for i in range(start, len(arr)):
        if arr[i] != 0:
            return False
    return True

'''
function that looks at the png and finds the 9 most common colors for you
@increments : size of your pixelized image in Minecraft blocks. has to be square
@imageName : name of image you are pixelizing
@availableColors : the Minecraft Block colors that are using
@clearBackGround : Boolean that makes your background to be ignored
@edge : The amount of pixels ignored when looking at the inside of the colors
'''
def findColorBlocks(increments, imageName, availableColors, clearBackGround, edge):
    image = PIL.Image.open(imageName)
    width, height = image.size
    increments = int(width / increments) 
    newWidth = width - (width % increments)
    newHeight = height - (height % increments)
    pixelizedImage = PIL.Image.new('RGB', (newWidth,newHeight))
    
    finalColors = {}
    finalBlocks = []
    blocksPos = [["" for x in range(int(width / increments))] for y in range(int(width / increments))] 
    colInstances = {}
    for colName in availableColors.keys():
        colInstances[colName] = 0
    
    for i in range(0, int(width / increments)):
        for j in range(0, int(height / increments)):
            average = [0,0,0]
            for pixX in range(i * increments + edge, i* increments + increments - edge):
                for pixY in range(j * increments + edge, j * increments + increments - edge):
                    pixel = image.getpixel((pixX , pixY ))
                    average[0] += pixel[0]
                    average[1] += pixel[1]
                    average[2] += pixel[2]
            newinc = increments - edge * 2
            average[0] /= (newinc * newinc)
            average[1] /= (newinc * newinc)
            average[2] /= (newinc * newinc)

            mindiff = 1000000
            use = ""
            #print(average) # find closest available color
            for colName, it in availableColors.items():
                newdiff = math.sqrt( abs(math.pow(it[0] - average[0],2) + math.pow(it[1] - average[1],2) + math.pow(it[2] - average[2],2) )) #  sqrt((r2-r1)^2 + (g2-g1)^2 + (b2-b1)^2)
                if newdiff < mindiff:
                    #print("u r dumbass")
                    mindiff = newdiff
                    use = colName
            #print(availableColors[use])
            average[0] = availableColors[use][0]
            average[1] = availableColors[use][1]
            average[2] = availableColors[use][2]
            blocksPos[i][j] = use
            colInstances[use] += 1

    # if you want a clear background, do a bfs to count how many background color pixels you have and subtract them from ther total count
    if clearBackGround:
        backGroundColor = blocksPos[0][0]
        queue = [[0,0],[len(blocksPos) - 1, len(blocksPos) - 1],[0,len(blocksPos) - 1],[len(blocksPos) - 1,0]]
        visited = []
        backamount = 0
        arrLen = len(blocksPos)
        while len(queue) > 0: # BFS algorithm to find the backbround and clear it
            if queue[0][0] + 1 < arrLen and blocksPos[queue[0][0] + 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                blocksPos[queue[0][0] + 1][queue[0][1]] = "background" 
                queue.append([queue[0][0] + 1, queue[0][1]])
            if queue[0][1] + 1 < arrLen and blocksPos[queue[0][0]][queue[0][1] + 1] == backGroundColor and notinvisited(queue[0],visited):
                blocksPos[queue[0][0]][queue[0][1] + 1] = "background" 
                queue.append([queue[0][0], queue[0][1] + 1])
            if queue[0][0] - 1 > 0 and blocksPos[queue[0][0] - 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                blocksPos[queue[0][0] - 1][queue[0][1]] = "background" 
                queue.append([queue[0][0] - 1, queue[0][1]])
            if queue[0][1] - 0 > 0 and blocksPos[queue[0][0]][queue[0][1] - 1] == backGroundColor and notinvisited(queue[0],visited):
                blocksPos[queue[0][0]][queue[0][1] - 1] = "background" 
                queue.append([queue[0][0], queue[0][1] - 1])
            visited.append(queue[0])
            queue.pop(0)
        
        for i in range(arrLen):
            for j in range(arrLen):
                if blocksPos[i][j] == backGroundColor:
                    backamount += 1
                elif blocksPos[i][j] == "background":
                    blocksPos[i][j] = backGroundColor

        print("background: " + str(colInstances[backGroundColor]))
        print("backgroundact: " + str(backamount))
        colInstances[backGroundColor] -= len(visited) # account for the background counting towards certain colors

    # make sure you to remove all entries with 0, to get the correct amount of colors being used
    newcols = {}
    for cool, numInstanceColor in colInstances.items():
        if numInstanceColor != 0:
            newcols[cool] = numInstanceColor
    
    # if you have less than 10 colors, you are done
    print(len(newcols))
    print(newcols)
    if (len(newcols) >= 10):
        # do work to find out what the rest of the top 9 colors approximate to
        newcols = dict(sorted(newcols.items(), key=lambda item: item[1])) # sort dict
        print(newcols)
        while(len(newcols) >= 10):
            # find a color that is used the least
            print(list(newcols)[0])
            leastUsed = list(newcols)[0]
            mindiff = 1000000
            newCol = ""
            for k,v in newcols.items():
                it = availableColors[k]
                average = availableColors[leastUsed]
                newdiff = math.sqrt( abs(math.pow(it[0] - average[0],2) + math.pow(it[1] - average[1],2) + math.pow(it[2] - average[2],2) )) #  sqrt((r2-r1)^2 + (g2-g1)^2 + (b2-b1)^2)
                if newdiff < mindiff and newdiff > 0:
                    mindiff = newdiff
                    newCol = k
            print(newCol)
            newcols[newCol] += newcols[leastUsed]
            newcols.pop(leastUsed)
            #return NULL,NULL
    count = 1
    for key, val in newcols.items():
        if val != 0:
            finalColors[count] = (availableColors[key][0],availableColors[key][1],availableColors[key][2])
            count += 1
            #print(finalColors)
            for k2,v2 in availableColors.items():
                if availableColors[key][0] == v2[0] and availableColors[key][1] == v2[1] and availableColors[key][2] == v2[2]:
                    finalBlocks.append(k2)
                    break
            

    # Make picture at the end
    for i in range(0, int(width / increments)):
        for j in range(0, int(height / increments)):
            for pixX in range(i* increments, i* increments + increments):
                for pixY in range(j* increments, j* increments + increments):
                    av = availableColors[blocksPos[i][j]]
                    pixelizedImage.putpixel((int(pixX ),int(pixY )),(int(av[0]),int(av[1]),int(av[2])))
    pixelizedImage.save('minecrafted.png')  
    # trigger earlier to remove a color
    print("+++ colors:")
    print(finalColors)
    print("+++ block:")
    print(finalBlocks)

    return finalColors, finalBlocks

'''
function that pixelizes a png
@increments : size of your pixelized image in Minecraft blocks. has to be square
@imageName : name of image you are pixelizing
@startColors : the Minecraft Block colors that are using
@clearBackGround : Boolean that makes your background to be ignored
@edge : The amount of pixels ignored when looking at the inside of the colors
'''
def changePictureToGrid(increments, imageName, startColors, clearBackGround, edge):
    #myScreenshot = pyautogui.screenshot()
    image = PIL.Image.open(imageName)
    width, height = image.size
    increments = int(width / increments) 
    newWidth = width - (width % increments)
    newHeight = height - (height % increments)
    pixelizedImage = PIL.Image.new('RGB', (newWidth,newHeight))
    
    backGroundColor = [255,255,255]
    finArr = [[0 for x in range(int(width / increments))] for y in range(int(width / increments))] 
    for i in range(0, int(width / increments)):
        for j in range(0, int(height / increments)):
            average = [0,0,0]
            for pixX in range(i * increments + edge, i* increments + increments - edge):
                for pixY in range(j * increments + edge, j * increments + increments - edge):
                    pixel = image.getpixel((pixX , pixY ))
                    average[0] += pixel[0]
                    average[1] += pixel[1]
                    average[2] += pixel[2]
            newinc = increments - edge * 2
            average[0] /= (newinc * newinc)
            average[1] /= (newinc * newinc)
            average[2] /= (newinc * newinc)

            mindiff = 1000000
            use = 0
            #print(average)
            for pos, it in startColors.items():
                newdiff = math.sqrt( abs(math.pow(it[0] - average[0],2) + math.pow(it[1] - average[1],2) + math.pow(it[2] - average[2],2) )) #  sqrt((r2-r1)^2 + (g2-g1)^2 + (b2-b1)^2)
                if newdiff < mindiff:
                    #print("u r dumbass")
                    mindiff = newdiff
                    use = pos
            #print(startColors[use])
            average[0] = startColors[use][0]
            average[1] = startColors[use][1]
            average[2] = startColors[use][2]
            finArr[i][j] = use


            for pixX in range(i* increments, i* increments + increments):
                for pixY in range(j* increments, j* increments + increments):
                    pixelizedImage.putpixel((int(pixX ),int(pixY )),(int(average[0]),int(average[1]),int(average[2])))
    pixelizedImage.save('pixelized.png')  
    if clearBackGround:
        backGroundColor = finArr[0][0]
        finArr[0][0] = 0
        queue = [[0,0],[len(finArr) - 1, len(finArr) - 1],[0,len(finArr) - 1],[len(finArr) - 1,0]]
        visited = []
        arrLen = len(finArr)
        while len(queue) > 0: # BFS algorithm to find the backbround and clear it
            if queue[0][0] + 1 < arrLen and finArr[queue[0][0] + 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0] + 1][queue[0][1]] = 0 
                queue.append([queue[0][0] + 1, queue[0][1]])
            if queue[0][1] + 1 < arrLen and finArr[queue[0][0]][queue[0][1] + 1] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0]][queue[0][1] + 1] = 0 
                queue.append([queue[0][0], queue[0][1] + 1])
            if queue[0][0] - 1 > 0 and finArr[queue[0][0] - 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0] - 1][queue[0][1]] = 0 
                queue.append([queue[0][0] - 1, queue[0][1]])
            if queue[0][1] - 0 > 0 and finArr[queue[0][0]][queue[0][1] - 1] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0]][queue[0][1] - 1] = 0 
                queue.append([queue[0][0], queue[0][1] - 1])
            visited.append(queue[0])
            queue.pop(0)

    #print(finArr)
    return finArr

'''
function that lets you use a existing png instead of computing it from scratch
@image : the file you want to reuse
'''
def usePreExisting(increments, imageName, startColors, clearBackGround):
    image = PIL.Image.open(imageName)
    width, height = image.size
    
    backGroundColor = [255,255,255]
    finArr = [[0 for x in range(increments)] for y in range(increments)] 
    for i in range(0, increments):
        for j in range(0, increments):
            average = [0,0,0]
            pixel = image.getpixel((i * increments + (increments / 2) , j * increments + (increments / 2) ))

            average[0] = pixel[0]
            average[1] = pixel[1]
            average[2] = pixel[2]

            mindiff = 1000000
            use = 0
            #print(average)
            for pos, it in startColors.items():
                newdiff = math.sqrt( abs(math.pow(it[0] - average[0],2) + math.pow(it[1] - average[1],2) + math.pow(it[2] - average[2],2) )) #  sqrt((r2-r1)^2 + (g2-g1)^2 + (b2-b1)^2)
                if newdiff < mindiff:
                    mindiff = newdiff
                    use = pos
            #print(startColors[use])
            average[0] = startColors[use][0]
            average[1] = startColors[use][1]
            average[2] = startColors[use][2]
            finArr[i][j] = use
 
    if clearBackGround:
        backGroundColor = finArr[0][0]
        finArr[0][0] = 0
        queue = [[0,0],[len(finArr) - 1, len(finArr) - 1],[0,len(finArr) - 1],[len(finArr) - 1,0]]
        visited = []
        arrLen = len(finArr)
        while len(queue) > 0: # BFS algorithm to find the backbround and clear it
            if queue[0][0] + 1 < arrLen and finArr[queue[0][0] + 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0] + 1][queue[0][1]] = 0 
                queue.append([queue[0][0] + 1, queue[0][1]])
            if queue[0][1] + 1 < arrLen and finArr[queue[0][0]][queue[0][1] + 1] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0]][queue[0][1] + 1] = 0 
                queue.append([queue[0][0], queue[0][1] + 1])
            if queue[0][0] - 1 > 0 and finArr[queue[0][0] - 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0] - 1][queue[0][1]] = 0 
                queue.append([queue[0][0] - 1, queue[0][1]])
            if queue[0][1] - 0 > 0 and finArr[queue[0][0]][queue[0][1] - 1] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0]][queue[0][1] - 1] = 0 
                queue.append([queue[0][0], queue[0][1] - 1])
            visited.append(queue[0])
            queue.pop(0)

    print(finArr)
    return finArr

'''
function that gets all of your blocks for you in Minecraft. Make sure you have an empty inventory to make this work.
'''
def GetBlocksFromInventory(colors):
    print("Press on ~ to get blocks")
    while(True):
        if (keyboard.is_pressed("~")):
            if (keyboard.is_pressed("1")):
                return 0
            time.sleep(.2)
            break
    # click on search
    pyautogui.keyDown('E')
    pyautogui.keyUp('E')
    pyautogui.moveTo(1291, 205, .01) 
    pyautogui.click() 
    pyautogui.moveTo(634, 361, .01)

    count = 1
    for color in colors:
        print(color)
        pyautogui.write(color) 
        if color.startswith("Blue"): # blue has weird case
            pyautogui.moveTo(654, 361, .01)
        pyautogui.press(str(count))
        count = count + 1
        if color.startswith("Blue"):
            pyautogui.moveTo(634, 361, .01)
        for i in range(len(color)):
            pyautogui.press('backspace')
    
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')


print("=== Start with an empty inventory ===")

size = 0
image = ""
background = False
getblocks = False

if len(sys.argv) == 5:
    size = int(sys.argv[1])
    image = "assets/" + sys.argv[2] + ".png"
    if sys.argv[3] == '1':
        background = True
    if sys.argv[4] == '1':
        getblocks = True
else:
    print("You need to pass 4 arguments, size of build in minecraft, image name, background clearing (1 to enable) and getting new blocks (1 to enable)")
    exit()

bestColors, BlockNames = findColorBlocks(size, image, AVAILABLE_COLORS, background, 8)
if getblocks:
    GetBlocksFromInventory(BlockNames)
itemArray = changePictureToGrid(size, image, bestColors, background, 8)
#itemArray = usePreExisting( size, "pixelized.png", mercy, True)

print("Click on '~' to start the building once you are inside Minecraft")
print("Make sure you are flying, pointing downwards, have a 0 degree view angle on the x and z axis, and that you have a wall to prevent you from flying off")

while(True):
    if (keyboard.is_pressed("~")):
        print("Let's get this bot started")
        time.sleep(.5)
        break

# Code for building the image in Minecraft
'''
t = .5
for i in range(0,len(itemArray)):
    for j in range(0,len(itemArray)):
        if (keyboard.is_pressed("~")):
            print("STOP")
            exit()
        if restIsZero(itemArray[i],j):
            continue
        if itemArray[i][j] != 0:
            pyautogui.press(str(itemArray[i][j]))
            pyautogui.click(button='right') 
        else:
            time.sleep(0.2)
        pyautogui.keyDown('D')
        pyautogui.keyUp('D')
        time.sleep(t)
        
        if j == 10 or j == 22:
            pyautogui.keyDown('A')
            pyautogui.keyUp('A')

    pyautogui.keyDown('S')
    pyautogui.keyUp('S')  

    pyautogui.keyDown('A')
    time.sleep(.12 * j)
    pyautogui.keyUp('A')
    if i == 13:
        pyautogui.keyDown('W')
        pyautogui.keyUp('W')
'''

for i in range(0,len(itemArray)):
    pyautogui.press(str(itemArray[i][0]))
    pyautogui.click(button='right')
    pyautogui.keyDown('S')
    time.sleep(0.13)  
    for j in range(1,len(itemArray)):
        if (keyboard.is_pressed("~")):
            print("STOP")
            exit()
        if restIsZero(itemArray[i],j):
            continue
        pyautogui.press(str(itemArray[i][j]))
        pyautogui.click(button='right')
        time.sleep(0.02)
        if j == 19:
            time.sleep(0.025)
        
         
    pyautogui.keyUp('S')   
    #pyautogui.mouseUp(button='right')
         
    break

print("=== Done ===")
