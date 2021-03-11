import cv2
import sys
import PIL.ImageGrab
import numpy as np
import os
import asyncio
import websockets
import subprocess
import re

def np_array_to_hex2(array):
    array = np.asarray(array, dtype='uint32')
    array = (1 << 24) + ((array[:, :, 0]<<16) + (array[:, :, 1]<<8) + array[:, :, 2])
    return [hex(x)[-6:] for x in array.ravel()]

np.set_printoptions(threshold=sys.maxsize)
char_list = [" ", "\[", "\]", "'", "\""]

print("[Info] Websocket created on port 7000.")
print("")

# The meat and potatoes
async def desktop(websocket, path):
    async for message in websocket:
    
        xRes = 240
        yRes = 135
        newlineCounter = 0
        needsColor = True
        socketString = ""
    
        Frame = np.array(PIL.ImageGrab.grab())
        Frame = cv2.resize(Frame, (xRes , yRes), interpolation=cv2.INTER_AREA)
        Frame = np_array_to_hex2(Frame)

        for i, j in enumerate(Frame[:-1]):
            # If we haven't added the color already
            if (needsColor):
                socketString += "<color=#" + str(j)[::2] + ">"
                needsColor = False
        
            # If current pixel and next are equal
            if (str(j)[::2]  == str(Frame[i+1])[::2] or needsColor): 
                if (newlineCounter == xRes):
                    socketString += "\n"
                    newlineCounter = 0
                    
                socketString += "■"
                newlineCounter = newlineCounter + 1
                
            # If not equal, terminate and reset needsColor bool    
            else:
                if (newlineCounter == xRes):
                    socketString += "\n"
                    newlineCounter = 0
                    needsColor = True
                socketString += "■</color>"
                needsColor = True
                newlineCounter = newlineCounter + 1
            
        await websocket.send(socketString)

# Pushes string to port 7000
asyncio.get_event_loop().run_until_complete(
    websockets.serve(desktop, 'localhost', 7000))
asyncio.get_event_loop().run_forever()    

left.release()
right.release()
cv2.destroyAllWindows()