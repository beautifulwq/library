import numpy as np
import cv2 as cv
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
            print('find file '+str(num+'.'+type)+' success in '+str(path))
        else:  # couldn't find the file
            print('Could not find file num:'+str(num)+' with type:'+str(type)+' at path:'+str(path))
            pass

    return file

# Function to return an array of R, G, B values
# from a raw video input
# Output is array of average R, G, B for length of video
def getRawRGB(patientNum,dataDir):
    rawFile = findFile(dataDir,patientNum,'.mp4')
    rawVid = cv.VideoCapture(rawFile.as_posix())
    vidLen = int(rawVid.get(cv.CAP_PROP_FRAME_COUNT))
    rgbArray = np.zeros([vidLen,3])
    print('processing ' +str(rawFile.name))
    count = 0
    success = 1
    while count<vidLen:
        success, image = rawVid.read()
        # process the image for R, G, B
        # the openCV package is using BGR protocol
        B2 = np.mean(image[:,:,0])
        G1 = np.mean(image[:,:,1])
        R0 = np.mean(image[:,:,2])
        rgbArray[count] = [R0,G1,B2]
        count += 1
    return rgbArray
#测试用例
get_video_and_save(4)
print(getRawRGB('4','E:\\C\\pythonexercise'))