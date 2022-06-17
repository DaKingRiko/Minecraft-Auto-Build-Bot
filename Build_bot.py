import time
import keyboard # pip3 install keyboard 
import pyautogui
import math
import random
import PIL
import atexit
from functools import partial
PIL.ImageGrab.grab = partial(PIL.ImageGrab.grab, all_screens=True)

'''
Goals for today:

+  Make it work while flying
_  clean up output image
_  get a second output image that shows what colors to get
_  make background clear
'''

def notinvisited(position, visited):
    for it in visited:
        if position[0] == it[0] and position[1] == it[1]:       
            return False
    return True

def restIsZero(arr, start):
    for i in range(start, len(arr)):
        if arr[i] != 0:
            return False
    return True

def changePictureToGrid(increments, imageName, startColors, clearBackGround):
    #myScreenshot = pyautogui.screenshot()
    image = PIL.Image.open(imageName)
    width, height = image.size
    pixelizedImage = PIL.Image.new('RGB', (width,height))
    increments = int(width / increments) + 1
    backGroundColor = [255,255,255]
    finArr = [[0 for x in range(int(width / increments))] for y in range(int(width / increments))] 
    for i in range(0, int(width / increments)):
        for j in range(0, int(height / increments)):
            average = [0,0,0]
            for pixX in range(i * increments, i* increments + increments):
                for pixY in range(j * increments, j * increments + increments):
                    pixel = image.getpixel((pixX  ,pixY ))
                    average[0] += pixel[0]
                    average[1] += pixel[1]
                    average[2] += pixel[2]
            average[0] /= (increments * increments)
            average[1] /= (increments * increments)
            average[2] /= (increments * increments)

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
        queue = [[0,0]]
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

print("=== Start ===")
#startColors = {1:(79,79,79),2:(127,127,127),3:(195,195,195),
#            4:(255,255,255),5:(0,0,0),6:(63,72,204), 
#            7:(255,141,66),8:(50,175,243),9:(255,127,39)}
startColors = {1:(253,241,1),2:(84,185,72),3:(54,111,47),
             4:(255,255,255),5:(80,165,220),6:(159,113,54), 
             7:(171,26,31),8:(67,123,160),9:(121,124,127)}
charmander = {
    1:(253,241,1), # yellow
    2:(243,119,53), # orange
    3:(244,67,54), # red
    4:(0,0,0),
    5:(255,255,255)
}
size = 24
itemArray = changePictureToGrid(size, "sample.png", charmander, True)

time.sleep(4)
print("Click on '~' to start the building once you are inside Minecraft")
'''pyautogui.press('D', presses=10)
for i in range(0,30):
    pyautogui.click(button='right') 
    pyautogui.keyDown('D')
    time.sleep(timeout)
    pyautogui.keyUp('D')
    if i % 2 == 0:
        pyautogui.press('3')
    else:
        pyautogui.press('6')
'''

while(True):
    if (keyboard.is_pressed("~")):
        print("Let's get this bot started")
        time.sleep(.5)
        break
'''
#test
t = .4
for cc in range(2):
    for i in range(25):
        pyautogui.press(str(random.randint(1,9)))
        pyautogui.click(button='right') 
        pyautogui.keyDown('D')
        pyautogui.keyUp('D')
        time.sleep(t)
        
        if i == 10 or i == 22:
            pyautogui.keyDown('A')
            pyautogui.keyUp('A')

    pyautogui.keyDown('S')
    pyautogui.keyUp('S')  

    pyautogui.keyDown('A')
    time.sleep(5)
    pyautogui.keyUp('A')
''' 

'''
# Old way of doing movement and block placement
timeout = .132
for i in range(0,len(itemArray)):
    for j in range(0,len(itemArray)):
        if (keyboard.is_pressed("~")):
            exit()
        if i % 2 == 0: 
            pyautogui.press(str(itemArray[i][j]))
        else:
            pyautogui.press(str(itemArray[i][len(itemArray) - j - 1]))
        pyautogui.click(button='right') 
        if i % 2 == 0:
            pyautogui.keyDown('D')
            time.sleep(timeout)
            pyautogui.keyUp('D')
        else:
            pyautogui.keyDown('A')
            time.sleep(timeout)
            pyautogui.keyUp('A')
    pyautogui.keyDown('S')
    time.sleep(timeout)
    pyautogui.keyUp('S')
    if i % 2 == 1:
        pyautogui.keyDown('D')
        time.sleep(timeout)
        pyautogui.keyUp('D')
    else:
        pyautogui.keyDown('A')
        time.sleep(timeout)
        pyautogui.keyUp('A')
'''

t = .4
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
            pyautogui.press('=')
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
    '''if i == 10 or i == 22:
        pyautogui.keyDown('W')
        pyautogui.keyUp('W')'''

print("=== Done ===")