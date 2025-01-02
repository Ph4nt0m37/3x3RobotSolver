from rubik_solver import utils
from flask import Flask, render_template
import serial, json, random
from serial import SerialException
#from cubescrambler import scrambler333
import os, time,colorsys
from io import StringIO, BytesIO
import numpy as np
from itertools import product
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
cube = 'bygrybbwwogrobrwogyggbrwyogryyogrowbrgywobrybogwywborw'

solution = (str(utils.solve(cube, method='Kociemba'))+'\r').replace('[',"").replace(']',"").replace(',',"")
print(solution)

buffer = bytearray()

byteList = []

def printC(c):
     print(c)

arduinoData = serial.Serial('com5',115200)
time.sleep(3)

arduinoData.write(solution.encode())

'''cv2.imshow("Color Detection", side1)
cv2.waitKey(0)
cv2.destroyAllWindows()'''
cameraNum = 1

def getImages():
     global cameraNum
     global buffer
     global byteList
     buffer = bytearray()
     imgSuccess = False
     msg = str(cameraNum)
     msg = msg + '\r'
     arduinoData.write(msg.encode())
     print(f"sent request: {msg}")
     while not imgSuccess:
          try:
               data = arduinoData.readline().strip()
               #print(data)
               if not 'done' in str(data):
                    #print(data.decode("utf-8"))
                    #byteList.append(int(data.decode("utf-8")))
                    try:
                         byteList.append(int(data.decode("utf-8")))
                    except ValueError:
                         byteList.append(0)
                    '''bytearray2 = bytearray(data)
                    buffer = buffer+bytearray2'''
               else:
                    img2 = Image.open(BytesIO(bytearray(byteList)))
                    #img2 = img2.convert('RGB')
                    img2.save(f"side{cameraNum}.jpg")
                    imgSuccess = True
                    print("Image save success!")

               '''print(str(solution))
               arduinoData.write(solution.encode())'''
          except SerialException:
               print("COM3 Not found, skipping this process...")
     if cameraNum < 2:
          byteList = []
          cameraNum+=1
          getImages()
     else:
          getSolution()

def getSolution():
     getColors()
def getColors():
     '''checkColors("side2.jpg",[[50,93],[84,83],[102,76],[80,104],[148,87],[119,121],[152,106],[175,97]])
     checkColors("side2.jpg",[[31,111],[60,122],[98,143],[33,148],[104,196],[42,203],[62,213],[93,236]])
     checkColors("side2.jpg",[[130,144],[165,126],[192,114],[117,200],[193,154],[138,226],[163,214],[170,212]])
     checkColors("side1.jpg",[[38,9],[54,5],[87,3],[18,67],[120,28],[6,126],[58,99],[83,81]])'''
     checkColors("side2.jpg",[[82,136],[144,120],[180,114],[128,157],[277,128],[211,177],[282,160],[340,152]])
     checkColors("side2.jpg",[[45,175],[106,198],[172,231],[53,237],[168,310],[61,301],[123,318],[169,348]])
     checkColors("side2.jpg",[[243,227],[312,204],[366,192],[249,297],[354,230],[250,349],[286,328],[324,301]])
     '''checkColors("side1.jpg",[[26,77],[110,9],[170,2],[15,111],[211,23],[12,176],[73,171],[222,119]])
     checkColors("side1.jpg",[[309,5],[350,32],[400,63],[277,16],[417,137],[306,128],[385,183],[435,202]])
     #getColors("side1.jpg",[[36,12],[57,7],[88,3],[18,70],[94,29],[9,124],[47,112],[103,90]])'''
     #checkColors("side1.jpg",[[,],[,],[,],[,],[,],[,],[,],[,]])
     #openCV color detection
     '''side1 = cv2.imread("side1.jpg")
     side1 = cv2.cvtColor(side1,cv2.COLOR_BGR2RGB)'''

def checkColors(image,pointsToCheck):
     #fixImage(image)
     image = image.replace(".jpg","")
     img = Image.open(f"{image}Fixed.jpg")
     #img = Image.open(f"side2Fixed.jpg")
     side1 = img.load()
     '''side1 = cv2.cvtColor(side1,cv2.COLOR_BGR2HSV)
     cv2.imwrite("side1HSV.jpg",side1)
     side1img = Image.open("side1HSV.jpg")'''
     '''lower_range = np.array([0, 0, 143]) # lower range of yellow color in RGB
     upper_range = np.array([162,162,255]) # upper range of yellow color in RGB
     side1_mask = cv2.inRange(side1,lower_range,upper_range)
     side1_masked = cv2.bitwise_and(side1, side1, mask = side1_mask)'''
     for point in pointsToCheck:
          sd1p = side1[point[0],point[1]]
          #print(f"pixel: {sd1p[0]}")
          side1px1color = colorsys.rgb_to_hsv(sd1p[0]/float(255),sd1p[1]/float(255),sd1p[2]/float(255))
          side1px1coloradj = [side1px1color[0]*360,side1px1color[1]*100,side1px1color[2]*100]
          print(side1px1coloradj)
          side1px1 = (side1px1coloradj[0])
          side1px2 = (side1px1coloradj[1])
          side1px3 = (side1px1coloradj[2])
          #image = cv2.circle(side1, (point[0],point[1]), radius=1, color=(255,0,0), thickness=-1)
          #cv2.imwrite("side1point.jpg",image)
          #print(side1px2)
          #print(side1px1)
          if (side1px1 >= 56 and side1px1 <= 95) and side1px3 > 50 and side1px2 > 70:
               print("yellow")

          if (side1px1 >= 30 and side1px1 < 56):
               if (side1px1 >= 30 and side1px1 < 45) and (side1px2 >= 65 and side1px2 <= 100) and side1px3 > 60:
                    print("orange")
               elif (side1px1 >= 45 and side1px1 < 56) and side1px2 > 70:
                    print("orange")

          if (side1px1 >= 85 and side1px1 <= 155) and side1px2>=80:
               print("green")

          if ((side1px1 >= 0.1 and side1px1 <= 45) or (side1px1 >= 340 and side1px1 <= 359)) and side1px2>=85 and side1px3 <= 60:
               print("red")
          if ((side1px1 >= 45 and side1px1 <= 130) or (side1px1 >= 295 and side1px1 <= 310) or (side1px1==0)) and (side1px2 <= 45):
               if (side1px1 >= 45 and side1px1 <= 130):
                    print("white")
               elif (side1px1 >= 295 and side1px1 <= 310):
                    print("white")
               elif (side1px1 ==0):
                    print("white")

          if (side1px1>=180 and side1px1<=230):
               print("blue")
          '''if (side1px1 >=90 and side1px1 <=140):
               if (side1px3 >=70 and side1px3 <= 95) and (side1px2 >= 20 and side1px2 <= 40):
                    print("white")
               elif (side1px3 >=35 and side1px3 <= 65) and (side1px2 >= 45 and side1px2 <= 65):
                    print("white")
               elif (side1px2 >= 80 and side1px2 <= 100):
                    print("green")
               elif (side1px2 >= 40 and side1px2 <= 65) and (side1px2<side1px3):
                    if (side1px1 >=90 and side1px1 <=105):
                         print("white")
                    else:
                         print("green")
          if (side1px1 >45 and side1px1 <=75):
               if (side1px2 >= 75) and (side1px2>side1px3):
                    print("red")
               elif (side1px3>=50 and side1px3 <=100):
                    print("orange")
               elif (side1px3 < 45):
                    print("orange")
          if (side1px1 >=20 and side1px1 <=45):
               if (side1px2 >85 and side1px2 <=100):
                    if (side1px1 >=35 and side1px1 <=45) and (side1px2 >= 90 and side1px2 <= 100) and (side1px3 >= 50 and side1px3 <= 70):
                         print("orange")
                    else:
                         print("red")
               elif (side1px2 >=45 and side1px2 <=85):
                    print("orange")
          if (side1px1 >=100 and side1px1 <=190) and (side1px2 > side1px3):
               print("blue")
          if (side1px1 >=76 and side1px1 <=105):
               if (side1px1 >= 87 and side1px1 <=105) and (side1px2 >= 70 and side1px2 <=85):
                    print("yellow")
               elif (side1px1 >=76 and side1px1 <=86):
                    print("yellow")'''

'''def fixImage(image):
     img = Image.open(image)
     image = image.replace(".jpg","")
     arr = np.asarray(img, dtype=np.int16)

     # Optional step to reduce the size of the image
     arr = arr[::2, ::2, :]
     # arr = arr[::4, ::4, :]

     target_colors = np.array([
     [i, j, k]
     for i, j, k in product(range(0, 256, 48), range(0, 256, 48), range(0, 256, 48))
     ], dtype=np.int16)

     # colors = {
     #     "White": 0x97d393,
     #     "Red": 0x782e02,
     #     "Yellow": 0x639405,
     #     "Orange": 0xb6820e,
     #     "Green": 0x7c2900,
     #     "Blue": 0x032225,
     # }
     # _color_map = {i: key for i, key in colors}
     # def decompose(color):
     #     red, rest = divmod(color, 2**16)
     #     green, blue = divmod(rest, 2**8)
     #     return [red, green, blue]

     # target_colors = np.array([
     #     decompose(color)
     #     for color in colors.values()
     # ], dtype=np.int16)

     diffs = (arr[None, ...] - target_colors[:, None, None, :])
     colors = np.argmin(np.abs(diffs).mean(axis=-1), axis=0)

     painted = Image.fromarray(target_colors[colors].astype(np.uint8))

     painted.save(f"{image}Fixed.jpg")'''

#getImages()
#getSolution()

'''def getScramble():
     global scramble
     global solution
     scramble = scrambler333.get_WCA_scramble()
     print (scramble)
     solution = (str(utils.solve(cube, 'Kociemba'))+'\r').replace('[',"").replace(']',"").replace(',',"")'''
     

'''app = Flask(__name__)

@app.route("/")
def index():
     getScramble()
     getSolution()
     return render_template('index.html',scramble = scramble, getSolution = getSolution(), test = test())

if __name__ == '__main__':
     app.run(debug=True)'''
