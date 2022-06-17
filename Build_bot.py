import time
import keyboard # pip3 install keyboard 
import pyautogui
import math
import PIL
import atexit
from functools import partial
PIL.ImageGrab.grab = partial(PIL.ImageGrab.grab, all_screens=True)

def changePictureToGrid(increments, imageName, startColors):
    #myScreenshot = pyautogui.screenshot()
    image = PIL.Image.open(imageName)
    width, height = image.size
    pixelizedImage = PIL.Image.new('RGB', (width,height))
    increments = int(width / increments) + 1
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
    return finArr

print("=== Start ===")
#startColors = {1:(79,79,79),2:(127,127,127),3:(195,195,195),
#            4:(255,255,255),5:(0,0,0),6:(63,72,204), 
#            7:(255,141,66),8:(50,175,243),9:(255,127,39)}
startColors = {1:(253,241,1),2:(84,185,72),3:(54,111,47),
             4:(255,255,255),5:(80,165,220),6:(159,113,54), 
             7:(171,26,31),8:(67,123,160),9:(121,124,127)}
itemArray = changePictureToGrid(20, "sample.jpg", startColors)

time.sleep(4)
print("gonna click")
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
timeout = .131
for i in range(0,len(itemArray)):
    for j in range(0,len(itemArray)):
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

print("=== Done ===")