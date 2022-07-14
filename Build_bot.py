from asyncio.windows_events import NULL
import time
import sys
import keyboard # pip3 install keyboard 
import pyautogui  # pip3 install pyautogui 
import math
from colors import *
import PIL
from functools import partial
from pytesseract import pytesseract
PIL.ImageGrab.grab = partial(PIL.ImageGrab.grab, all_screens=True)

'''
Goals for today:

+  stabilize building
_  get input picture from google
_  get walking to work as an option
_  make setup script that gets you all blocks 
_  add self adjusting angle at the beggining of the build
_  add more colors as options
_  try correcting pytesseract errors when reading weird text
_  when backGroundClear is enabled make sure to skip initial clear blocks too
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
        if len(arr[i]) > 0:
            return False
    return True

'''
function that pixelizes a png
@increments : size of your pixelized image in Minecraft blocks. has to be square
@imageName : name of image you are pixelizing
@startColors : the Minecraft Block colors that are using
@edge : The amount of pixels ignored when looking at the inside of the colors
'''
def changePictureToGrid(increments, imageName, startColors, clearBackground,  edge):
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
    if clearBackground:
        backGroundColor = finArr[0][0]
        finArr[0][0] = ""
        queue = [[0,0],[len(finArr) - 1, len(finArr) - 1],[0,len(finArr) - 1],[len(finArr) - 1,0]]
        visited = []
        arrLen = len(finArr)
        while len(queue) > 0: # BFS algorithm to find the backbround and clear it
            if queue[0][0] + 1 < arrLen and finArr[queue[0][0] + 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0] + 1][queue[0][1]] = "" 
                queue.append([queue[0][0] + 1, queue[0][1]])
            if queue[0][1] + 1 < arrLen and finArr[queue[0][0]][queue[0][1] + 1] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0]][queue[0][1] + 1] = "" 
                queue.append([queue[0][0], queue[0][1] + 1])
            if queue[0][0] - 1 > 0 and finArr[queue[0][0] - 1][queue[0][1]] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0] - 1][queue[0][1]] = "" 
                queue.append([queue[0][0] - 1, queue[0][1]])
            if queue[0][1] - 0 > 0 and finArr[queue[0][0]][queue[0][1] - 1] == backGroundColor and notinvisited(queue[0],visited):
                finArr[queue[0][0]][queue[0][1] - 1] = "" 
                queue.append([queue[0][0], queue[0][1] - 1])
            visited.append(queue[0])
            queue.pop(0)
    
    #print(finArr)
    return finArr

'''
function that lets you use a existing png instead of computing it from scratch
@image : the file you want to reuse
'''
def usePreExisting(increments, imageName, startColors):
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
            pyautogui.moveTo(684, 361, .01)
        pyautogui.press(str(count))
        count = count + 1
        if color.startswith("Blue"):
            pyautogui.moveTo(634, 361, .01)
        for i in range(len(color)):
            pyautogui.press('backspace')
    
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')

'''
function that takes a screenshot and looks at player coordinates, and returns the x and z coordinates
'''
def readCoordinates(mult):
    myScreenshot = pyautogui.screenshot()
    #myScreenshot.save('screen.png') 
    #im = PIL.Image.open("screen2.png")
    im1 = myScreenshot.crop((3575, 424, 3835 ,457)) #1926 388 | 2618 420 | 2712 NEW 3575 424 | 3835 457 | 3478 . old: (2006, 385, 2712, 425) 
    width, height = im1.size
    im1 = im1.resize((width*2,height*2))
    #im1.save("crop.png")

    path_to_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract
    #Open image with PIL
    #Extract text from image
    text = pytesseract.image_to_string(im1, lang='mc', config='--psm 13 -c tessedit_char_whitelist=0123456789.-/')
    print(text)
    coords = text.split(" ")
    if len(coords) >= 3:
        if len(mult) == 0:
            if coords[0].split(' ')[0].startswith('-'):
                mult.append(-1)
            else:
                mult.append(1)
            if coords[2].split(' ')[0].startswith('-'):
                mult.append(-1)
            else:
                mult.append(1)
        return [mult[0] * int(coords[0].split(' ')[0].replace("-", "").replace(" ", "")),mult[1] * int(coords[2].split(' ')[0].replace("-", "").replace(" ", "")),mult[0],mult[1]]
    else:
        return []

print("=== Start with an empty inventory ===")

size = 0
image = ""
background = False

if len(sys.argv) == 4:
    size = int(sys.argv[1])
    image = "assets/" + sys.argv[2] + ".png"
    background = (sys.argv[3] == '1')
else:
    print("You need to pass 3 arguments, size of build in minecraft, image name, and clearBackground (1 to enable)")
    exit()

itemArray = changePictureToGrid(size, image, AVAILABLE_COLORS, background, 8)
#itemArray = usePreExisting( size, "pixelized.png", mercy, True)

print("Click on '~' to start the building once you are inside Minecraft")
print("Make sure you are on the ground, pointing in front of you, have a 0 degree view angle on the x and z axis, and that you have a wall to prevent you from walking off")

while(True):
        if (keyboard.is_pressed("~")):
            print("Let's get this bot started")
            time.sleep(.5)
            break

starting = readCoordinates([])
current = [starting[0],starting[1],starting[2],starting[3]]
print(starting)
# Code for building the image in Minecraft
t = 0.1
currhand = ""
for i in range(0,len(itemArray)):
    #print(itemArray[i][0])
    #print(len(itemArray[i][0]))
    if len(itemArray[i][0]) > 0:
        #print("here")
        next = AVAILABLE_COLORS_LOCATION[itemArray[i][0]]
        with pyautogui.hold('X'):
            pyautogui.press([next[0]])
        pyautogui.press(next[1])
        pyautogui.click(button='right')
    pyautogui.keyDown('D')
    time.sleep(t)
    pyautogui.keyUp('D')
    for j in range(1,len(itemArray)):
        if (keyboard.is_pressed("~")): 
            print("STOP")
            exit()
        if restIsZero(itemArray[i],j):
            continue
        newPos = readCoordinates([current[2],current[3]])
        print(newPos)
        while newPos[0] != current[0] + 1:
            print("adjust")
            if newPos[0] <= current[0]: # check for z tooand newPos[1] == current[1]:
                pyautogui.keyDown('D')
                time.sleep(t)
                pyautogui.keyUp('D')
            elif newPos[0] >= current[0] + 2: # check for z tooand newPos[1] == current[1]:
                pyautogui.keyDown('A')
                time.sleep(t)
                pyautogui.keyUp('A')
            
            newPos = readCoordinates([current[2],current[3]])
            print(newPos)
        if len(itemArray[i][j]) > 0:
            next = AVAILABLE_COLORS_LOCATION[itemArray[i][j]]
            with pyautogui.hold('X'):
                pyautogui.press([next[0]])
            pyautogui.press(next[1])
            pyautogui.click(button='right')
        pyautogui.keyDown('D')
        time.sleep(t)
        pyautogui.keyUp('D')
        current = newPos

    pyautogui.keyDown('S') 
    time.sleep(t)
    pyautogui.keyUp('S') 
    newPos = readCoordinates([current[2],current[3]])
    while newPos[1] != current[1] + 1:
        print("adjust y")
        if newPos[1] <= current[1]: # check for z too and newPos[1] == current[1]:
            pyautogui.keyDown('S')
            time.sleep(t)
            pyautogui.keyUp('S')
        elif newPos[1] >= current[1] + 2: # check for z too and newPos[1] == current[1]:
            pyautogui.keyDown('W')
            time.sleep(t)
            pyautogui.keyUp('W')
        
        newPos = readCoordinates([current[2],current[3]])
        print(newPos)
    pyautogui.keyDown('A') 
    time.sleep(0.1 * j)
    pyautogui.keyUp('A') 
    newPos = readCoordinates([current[2],current[3]])
    
    while newPos[0] != starting[0]:
        print("adjust end")
        if newPos[0] < starting[0]: 
            pyautogui.keyDown('D')
            time.sleep(t)
            pyautogui.keyUp('D')
        elif newPos[0] > starting[0]: 
            pyautogui.keyDown('A')
            time.sleep(t)
            pyautogui.keyUp('A')
        newPos = readCoordinates([current[2],current[3]])
        print(newPos)
    if background: # if the back ground is clear, skip the rows that are transparent
        print(itemArray[i])
        for extra in itemArray[i]:
            if extra == "":
                print("skipped ")
                newPos[1] += 1 
            else:
                break
    current[0] = newPos[0]
    current[1] = newPos[1]
    print(current)
    
   

print("=== Done ===")
