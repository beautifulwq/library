import numpy as np
import cv2 as cv
import  os
from scipy.signal import savgol_filter
import numpy as np
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
from pathlib import Path

def get_video_and_save(numb):

    cap = cv.VideoCapture(0)
    # 声明编码器和创建 VideoWrite 对象,
    fourcc = cv.VideoWriter_fourcc(*'mp4v')  # mp4
#    fourcc = cv.VideoWriter_fourcc(*'GPJM')
#上边这个出现OpenCV: FFMPEG: tag 0x4d4a5047/'GPJM' is not found
#(format 'mp4 / MP4 (MPEG-4 Part 14)')'
    out = cv.VideoWriter('%d.mp4'%(numb),fourcc, 30.0, (640,480))
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
        #frame = cv.flip(frame,0)
            # 写入已经翻转好的帧
            out.write(frame)
            cv.imshow('frame',frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # 释放已经完成的工作
    cap.release()
    out.release()
    cv.destroyAllWindows()
# Function to return the path of a file
# given a directory, patient number and file type
def findFile(path, num, type):
    fileList = list(Path(path).rglob('*' + type))
    #print(fileList)
    file = None
    for f in fileList:
        if str(num) in f.name:
            file = f
            print(file)
            print('find file '+str(num+type)+' success in '+str(path))
        else:  # couldn't find the file
            pass

    return file

# Function to return an array of  G values
# from a raw video input
# Output is array of average  G  for length of video
def getRawofG(patientNum,dataDir):
    rawFile = findFile(dataDir,patientNum,'.mp4')
    rawVid = cv.VideoCapture(rawFile.as_posix())
    vidLen = int(rawVid.get(cv.CAP_PROP_FRAME_COUNT))
    rgbArray = np.zeros(vidLen)#vidLen行，1列
    print('processing ' +str(rawFile.name))
    count = 0
    success = 1
    while count<vidLen:
        success, image = rawVid.read()
        # process the image for R, G, B
        # the openCV package is using BGR protocol
        G1 = np.mean(image[:,:,1])
        rgbArray[count] = G1
        count += 1
    return rgbArray

def plotGofRGB(rgb,num):
    color ='green'
    pltTitle = 'G Plot for ' + str(num)
    pltXLabel = 'Frame'
    pltYLabel = 'Received Lumen Value'
    plt.plot(rgb[:],color=color,label=str(color))
    y = savgol_filter(rgb, 5, 3, mode='nearest')
    plt.plot(y, 'red', label='savgol')
    plt.legend(loc='upper right')
    plt.gca().set(title=pltTitle,xlabel=pltXLabel,ylabel=pltYLabel)
    plt.show()
    return plt

#测试用例
#get_video_and_save(2)
listi=[x for x in range(2,3)]
print(listi)
for i in listi:
    rgba=getRawofG('%d'%(i),'E:\\C\\pythonexercise')
    plotGofRGB(rgba,i)
    print(rgba)
