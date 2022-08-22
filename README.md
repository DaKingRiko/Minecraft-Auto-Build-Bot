# Minecraft Bot 

## Prerequisites

You need to install the following packages in order to make the program work:

```
pip install keyboard
pip install pyautogui
pip install pillow
pip install pytesseract
```

## How to Use

If you are using this on windows, running any of this code on WSL will NOT work. Use powershell instead.

0. Before you start, you might need to go and change some variables in the code.
The bot is hard coded to take position coordinates of the block the player is looking at, so in certain versions of Minecraft, those coordinates are in other parts of the screen.
To make sure this works without any changes, use the bot with Minecraft 1.19.
The coordinates are located on line 178 in variable im1. Take a screenshot and find those numbers on your screen using paint or some other image editing software.

1. Open a powershell in the folder that has all the code

2. run 

   ```bash
   python .\Build_Bot <MINECRAFT BUILD SIZE> <IMAGE NAME> <BACKGROUND REMOVAL>
   # Example:
   python .\Build_Bot 18 totodile -back
   python .\Build_Bot 35 kyogre
   ```

3. Background removal is optional and make sure that the images you use are squares, otherwise the program won't work.
Also, make sure that the image width and height is perfectly divisible by the build size, or the program won't work

4. Once you run the program, the bot will do all the work and create a image called 'pixelized.png' which will show you how the image will look like in minecraft.

5. At this point go into Minecraft, make sure you have all the blocks needed to proceed.
If you don't, run:
  ```bash
   python .\Build_Bot getblocks
   ```
Then go into Minecraft, press on '~', and wait until you get all 32 blocks.
It is possible to customize the blocks you use, and you can add even more if you want to.
Edit the colors.py file to add any building blocks you want.

6. Once you have all the blocks needed to proceed, Make sure your character is pointing at a distance of 2 blocks in front of you, and make sure your viewing angle is about -180 or 180.
You need to be facing in the negative Z direction, since the bot will move right (positive X direction) and backwards (positive Z), and it will assume that for the coordinates it is trying to read.
You can start anywhere in the world at any elevation, but if pytesseract is failing, you might need to expand or shrink the box it is trying to read, similarly like you did in step 5.
press on '~' to start the building

7. The bot will start building (slowly), and it may take some time depending on the size of the image.
Very rarely, The bot might randomly miss a block or stop working all-together due to pytesseract not being able to process text from a screenshot.

8. The bot should be done, and the program will end

If you have any questions come into my twitch chat and ask me directly, I am happy to answer any questions:
https://www.twitch.tv/King_Riko