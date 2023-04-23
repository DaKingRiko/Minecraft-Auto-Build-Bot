from asyncio.windows_events import NULL
import time
import sys
import keyboard # pip3 install keyboard 
import pyautogui  # pip3 install pyautogui 
import math
from colors import *
import PIL
from functools import partial
from pytesseract import pytesseract # pip install pytesseract
PIL.ImageGrab.grab = partial(PIL.ImageGrab.grab, all_screens=True)
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import numpy

'''
Goals for today:

_  get input picture from google
_  get walking to work as an option
_  make setup script that gets you all blocks 
_  add more colors as options
?  try correcting pytesseract errors when reading weird text
_  MAKE IT FASTER. make it work backwards on odd rows
_  add a fast option where it inputs setblock commands
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
def restIsZero(arr, start, order):
    if order == 1:
        for i in range(start, len(arr)):
            if len(arr[i]) > 0:
                return False
    else:
        for i in range(0, start + 1):
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
                    #print(pixX)
                    #print(pixY)
                    if isinstance(pixel,int):
                        temp = pixel
                        pixel = [temp,temp,temp]
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
    
    size = 18
    width, height = img.size
    ccc = 0
    for i in range(size):
        for j in range(size): #99, 42, 9
            for inc in range(int(width / size)):
                pixelizedImage.putpixel((int(i*(width / size )),int(j*(width / size )+ inc)),(99, 42, 9))
                pixelizedImage.putpixel((int(j*(width / size )+ inc),int(i*(width / size ))),(99, 42, 9))
            #img.save(("gridgif/trygrid" + str(ccc) + ".png"))
            ccc += 1
    #pixelizedImage.save(("griddy" + str(ccc) + ".png"))
    
    if clearBackground:
        backGroundColor = finArr[0][0]
        finArr[0][0] = ""
        finArr[len(finArr) - 1][ len(finArr) - 1] = ""
        finArr[0][len(finArr) - 1] = ""
        finArr[len(finArr) - 1][0] = ""
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
        #print(color)
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
def readCoordinates(mult,prev):
    myScreenshot = pyautogui.screenshot()
    #myScreenshot.save('screen.png') 
    #im = PIL.Image.open("screen2.png")
    im1 = myScreenshot.crop((2146, 532, 2382, 565)) #1926 388 | 2618 420 | 2712 NEW 3575 424 | 3835 457 | 3478 . old: (2006, 385, 2712, 425) 1.12: 2146 532 2382 565
    width, height = im1.size
    im1 = im1.resize((width*2,height*2))
    im1.save("crops.png")

    path_to_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract
    #Open image with PIL
    #Extract text from image
    try:
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
            print(text[0:4])
            print(text[5:8])
            return [mult[0] * int(text[0:4]),mult[1] * int(text[5:8]),mult[0],mult[1]]
            prev[0] += 1
            print("COORDINATE READING FAILED")
            return prev # to prevent it from crashing, pretend it worked properly for now TODO make this better
    except:
        prev[0] += 1
        print("COORDINATE READING FAILED")
        return prev

# used to end program if '~' key is detected
def listenEnd(mytime):
    if (keyboard.is_pressed("~")): 
        print("=== This took " + str(time.time() - mytime) + " seconds ===")
        exit()

'''
function that adjusts your current Minecraft player position to be the same as current
@newPos : your position
@current : goal position
@t : time to sleep in between walks
'''
def adjustMCXPosition(newPos, current, t):
    while newPos[0] != current[0]:
        if (keyboard.is_pressed("~")): 
            print("STOP")
            exit()
        #print("adjust x")
        if newPos[0] < current[0]: # check for z tooand newPos[1] == current[1]:
            pyautogui.keyDown('D')
            time.sleep(t)
            pyautogui.keyUp('D')
        elif newPos[0] > current[0]: # check for z tooand newPos[1] == current[1]:
            pyautogui.keyDown('A')
            time.sleep(t)
            pyautogui.keyUp('A')
        
        newPos = readCoordinates([current[2],current[3]],current)
        #print(newPos)
    return newPos

'''
function that adjusts your current Minecraft player position to be the same as current
@newPos : your position
@current : goal position
@t : time to sleep in between walks
'''
def adjustMCZPosition(newPos, current, t):
    while newPos[1] != current[1]:
        if (keyboard.is_pressed("~")): 
            print("STOP")
            exit()
        #print("adjust z")
        if newPos[1] < current[1]: # check for z too and newPos[1] == current[1]:
            pyautogui.keyDown('S')
            time.sleep(t)
            pyautogui.keyUp('S')
        elif newPos[1] > current[1]: # check for z too and newPos[1] == current[1]:
            pyautogui.keyDown('W')
            time.sleep(t)
            pyautogui.keyUp('W')
        
        newPos = readCoordinates([current[2],current[3]],current)
        #print(newPos)
    return newPos

'''
helper function to make the program less lines of code
@key : key to press
@t: time to wait until press is done
'''
def moveMC(key, t):
    pyautogui.keyDown(key)
    time.sleep(t)
    pyautogui.keyUp(key)

'''
function to place block in MC
@item: string that represents the color that should be placed
'''
def rightClick(item):
    if len(item) > 0:
        next = AVAILABLE_COLORS_LOCATION[item]
        with pyautogui.hold('X'):
            pyautogui.press([next[0]])
        pyautogui.press(next[1])
        pyautogui.click(button='right')

def getWrittenCommand(block,i,j,k=4,useDict=True):
    mycommand = "setblock ~" + str(i + 2) + " " + str(k) +" ~" + str(j + 2) + " minecraft:"
    if useDict:
        if "Wool" in block:
            mycommand += "wool "
        elif "Terracotta" in block:
            mycommand += "stained_hardened_clay "
        # pick color
        if "Light" in block:
            if "Blue" in block:
                mycommand += "3"
            elif "Gray" in block:
                mycommand += "8"
        else:
            mycommand += str(PLAIN_COLOR[ block.split(" ")[0]])
    else:
        mycommand += block
    #print(mycommand)
    pyautogui.press('/') 
    pyautogui.write(mycommand)
    pyautogui.press('enter') 

############################################################ NEW STL CODE ####################################################################################

def bounding_box(points):
    '''
    Calculate the bounding box edge lengths of an stl using the design coordinate system (not an object oriented bounding box),
    expect that input coordinates are in mm.
    '''
    v = points
    x = v[..., 0].flatten()
    y = v[..., 1].flatten()
    z = v[..., 2].flatten()
    return (x.max()-x.min(), y.max()-y.min(), z.max()-z.min())

def get_min(points):
    '''
    Calculate the minimum coordinates of your stl,
    expect that input coordinates are in mm.
    '''
    v = points
    x = v[..., 0].flatten()
    y = v[..., 1].flatten()
    z = v[..., 2].flatten()
    return (x.min(), y.min(), z.min())

def getSTLarray(filename,STLX,STLY,STLZ):
    # Create a new plot
    figure = pyplot.figure()
    axes = figure.add_subplot(projection='3d')

    # Load the STL files and add the vectors to the plot
    your_mesh = mesh.Mesh.from_file(filename)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    minVals = get_min(your_mesh.points)
    #print(minVals)
    LENGTHS = bounding_box(your_mesh.points)
    #print(LENGTHS)

    v = your_mesh.points
    x = v[..., 0].flatten()
    y = v[..., 1].flatten()
    z = v[..., 2].flatten()
    try:
        myw,myl,myh = STLX,STLY,STLZ
        scx,scy,scz = LENGTHS[0]/myw,LENGTHS[1]/myl,LENGTHS[2]/myh
        pamounts = numpy.zeros([myw,myl,myh])
        err = 0
        #print(pamounts)
        #print("x {} y {} z {}".format(len(x),len(y),len(z)))
        for i in range(0,len(x)): # 10):#
            #print("x {} min {} scale {}".format(x[i],minVals[0],scx))
            corx = int( (x[i] - minVals[0]) / scx)
            cory = int( (y[i] - minVals[1]) / scy)
            corz = int( (z[i] - minVals[2]) / scz)
            #print("nx {} ny {} nz {}".format(corx,cory,corz))
            if corx >= myw or cory >= myl or corz >= myh :
                err += 1
            else:
                pamounts[corx,cory,corz] += 1

        #print("Errs {}".format(err))
        #print(pamounts)
        limit = int(len(x) / (3*myw*myl*myh ))
        #print(limit)
        fin = numpy.zeros([myw,myl,myh])
        for i in range(0,myw):
            for j in range(0,myl):
                for k in range(0,myh):
                    if pamounts[i,j,k] >= limit:
                        fin[i,j,k] += 1
        #print(fin)
        return fin
    except Exception as e:
        print(e)
        exit()

############################################################ MAIN PROGRAM START ####################################################################################

mytime = time.time()
print("=== Start with an empty inventory ===")

size = 0
image = ""
background = False
fast = False

if len(sys.argv) >= 3:
    stl = ('-stl' in sys.argv)
    if not stl:
        size = int(sys.argv[1])
        image = "assets/" + sys.argv[2] + ".png"
        background = ('-back' in sys.argv)
        fast = ('-fast' in sys.argv)
else:
    print("You need to pass at least 2 arguments: size of build in minecraft, and source image name.")
    print("Optional Arguments: to have a clear Background (-back), and option to make the building fast (-fast)")
    print("\n    Example: python ./Build_Bot.py 20 image.png -back -fast\n")
    print("If You want to build in 3D, use the -stl option, then give a file name, 3 dimensions, and a block name (without the minecraft part)")
    print("\n    Example: python ./Build_Bot.py -stl object.stl 10 10 10 stone\n")
    exit()

####################################
# STL Handler for 3D
####################################

if stl:
    if len(sys.argv) >= 7:
        #print(sys.argv)
        file = "assets/" + sys.argv[2] + ".stl"
        STLX = int(sys.argv[3])
        STLY = int(sys.argv[4])
        STLZ = int(sys.argv[5])
        STL_BLOCK = sys.argv[6]
    else:
        print("You need to pass at least 5 arguments: source file name, desired Minecraft block Width, Depth, Height, and Block to use.")
        print("\n    Example: python ./Build_Bot.py -stl object.stl 10 10 10 stone\n")
        exit()

    stlArr = getSTLarray(file,STLX,STLY,STLZ)
    #print(stlArr)

    print("Click on '~' to start the building once you are inside Minecraft")
    print("=== This first computation took " + str(time.time() - mytime) + " seconds ===")
    while(True):
            if (keyboard.is_pressed("~")):
                print("Let's get this bot started")
                time.sleep(.5)
                break
    #print("x {} y {} z {} block {}".format(STLX,STLY,STLZ,STL_BLOCK))
    mytime = time.time()
    for i in range(0,STLX):
        for j in range(0,STLY):
            for k in range(0,STLZ):
                if (keyboard.is_pressed("*")): 
                    print("STOP")
                    exit()
                #print("i {} j {} k {} val {}".format(i,j,k,stlArr[i,j,k] ))
                if stlArr[i,j,k] == 1:
                    getWrittenCommand(STL_BLOCK,i,k,j + 7,useDict=False) # i j k to i k j

    print("=== This took " + str(time.time() - mytime) + " seconds ===")
    exit()

    


####################################
# Grid code
####################################
img = PIL.Image.open(image)
width, height = img.size
ccc = 0
for i in range(size):
    for j in range(size): #99, 42, 9
        for inc in range(int(width / size)):
            img.putpixel((int(i*(width / size )),int(j*(width / size )+ inc)),(99, 42, 9))
            img.putpixel((int(j*(width / size )+ inc),int(i*(width / size ))),(99, 42, 9))
        #img.save(("gridgif/trygrid" + str(ccc) + ".png"))
        ccc += 1
#img.save(("griddy" + str(ccc) + ".png"))
####################################     



itemArray = changePictureToGrid(size, image, AVAILABLE_COLORS, background, 0)
#itemArray = usePreExisting( size, "pixelized.png", mercy, True)
#myScreenshot = pyautogui.screenshot()
#myScreenshot.save('sshot112.png') # 2146 532 2382 565

print("Click on '~' to start the building once you are inside Minecraft")
print("Make sure you are on the ground, pointing in front of you, have a 0 degree view angle on the x and z axis, and that you have a wall to prevent you from walking off")
print("=== This first computation took " + str(time.time() - mytime) + " seconds ===")
while(True):
        if (keyboard.is_pressed("~")):
            print("Let's get this bot started")
            time.sleep(.5)
            break

mytime = time.time()
if fast:
    print("The bot will instead type in commands to build the image for you") 
    for i in range(0,len(itemArray)):
        for j in range(0,len(itemArray)):
            if (keyboard.is_pressed("*")): 
                print("STOP")
                exit()
            if len(itemArray[i][j]) > 0:
                #print(itemArray[i][j])
                getWrittenCommand(itemArray[i][j],i,j)

    print("=== This took " + str(time.time() - mytime) + " seconds ===")
    exit()

starting = readCoordinates([1,1],[])
current = [starting[0],starting[1],starting[2],starting[3]]
#print(starting)
# Code for building the image in Minecraft
t = 0.07
currhand = ""
skip = 0
newPos = []

for i in range(0,len(itemArray)):
    if i % 2 == 0:
        for j in range(skip,len(itemArray)):
            if restIsZero(itemArray[i],j,1):
                newPos = readCoordinates([current[2],current[3]],current)
                break
            rightClick(itemArray[i][j])
            if j >= len(itemArray) - 1:
                newPos = readCoordinates([current[2],current[3]],current)
                break
            moveMC('D', t)
            newPos = readCoordinates([current[2],current[3]],current)
            newPos = adjustMCXPosition(newPos, [current[0] + 1,current[1],current[2],current[3]], t)
            current = newPos
        newPos = adjustMCZPosition(newPos, [current[0],current[1] + 1,current[2],current[3]], t)
        skip = 0
        if i + 1 < len(itemArray):
            for nextit in reversed(itemArray[i+1]):
                if nextit == '':
                    skip += 1
                else:
                    break
        newPos = adjustMCXPosition(newPos, [starting[0] + len(itemArray) - 1 - skip,current[1],current[2],current[3]], t)
        current = newPos
    else:
        for j in reversed(range(0,len(itemArray) - skip)):
            if restIsZero(itemArray[i],j,0):
                newPos = readCoordinates([current[2],current[3]],current)
                break
            rightClick(itemArray[i][j])
            if j <= 0:
                newPos = readCoordinates([current[2],current[3]],current)
                break
            moveMC('A', t)
            newPos = readCoordinates([current[2],current[3]],current)
            newPos = adjustMCXPosition(newPos, [current[0] - 1,current[1],current[2],current[3]], t)
            current = newPos
        newPos = adjustMCZPosition(newPos, [current[0],current[1] + 1,current[2],current[3]], t)
        skip = 0
        if i + 1 < len(itemArray):
            for nextit in itemArray[i+1]:
                if nextit == '':
                    skip += 1
                else:
                    break
        newPos = adjustMCXPosition(newPos, [starting[0] + skip,current[1],current[2],current[3]], t)
        current = newPos   

tottime = time.time() - mytime
print("=== This took " + str((tottime - tottime % 60) / 60) + " minutes " + str(tottime % 60) + " seconds ===")
print("=== Done ===")
