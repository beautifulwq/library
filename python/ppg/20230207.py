import scipy
from scipy.signal import savgol_filter
import cv2 as cv
import numpy as np
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
from pathlib import Path
import  os
#录制视频，numb为要保存的编号，电脑是默认摄像头，手机不知道能不能成功
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

# Function to return an array of  RGB values 可以三选一或者都用
# from a raw video input
# Output is array of average  G  for length of video
def getRawofRGB(patientNum,dataDir,sel):
    # sel=0,blue,sel=1;green,sel=2,red
    rawFile = findFile(dataDir,patientNum,'.mp4')
    rawVid = cv.VideoCapture(rawFile.as_posix())
    vidLen = int(rawVid.get(cv.CAP_PROP_FRAME_COUNT))
    print('vidlen:',vidLen)
    rgbArray = np.zeros(vidLen)#vidLen行，1列
    print('processing ' +str(rawFile.name))
    count = 0
    success = 1
    while count<vidLen-1:
        success, image = rawVid.read()
        # process the image for R, G, B
        # the openCV package is using BGR protocol
        G1 = np.mean(image[:,:,sel])
        G1=format(G1,'.8f')#控制小数位数
        rgbArray[count] = G1
        count += 1
    #print(rgbArray)
    return rgbArray

def plotGofRGB(rgb,num,col,sel):
#sel=1,滤波（未完成），sel=0，不滤波
        if sel==1:
            color =col
            pltTitle = '%s'%(col)+' Plot for ' + str(num)+'滤峰'
            pltXLabel = 'Frame'
            pltYLabel = 'Received Lumen Value'
            plt.plot(rgb[:-1],color=color,label=str(color))
            y = savgol_filter(rgb, 5, 3, mode='nearest')
            plt.plot(y, 'red', label='savgol')
            plt.legend(loc='upper right')
            plt.gca().set(title=pltTitle,xlabel=pltXLabel,ylabel=pltYLabel)
            #选峰 用的是拟合后的y
            tx=y
            peaks,properties=find_peaks(tx,height=5,distance=20)
            peaksyval=y[peaks]
            print(peaks)
            print(peaksyval)
            #
            plt.plot(peaks[:],peaksyval,"x",color='black')
            plt.show()

            return plt
        elif sel==0:
            color = col
            pltTitle = '%s'%(col)+' Plot for ' + str(num)
            pltXLabel = 'Frame'
            pltYLabel = 'Received Lumen Value'
            plt.plot(rgb[:-1], color=color, label=str(color))
            plt.legend(loc='upper right')
            plt.gca().set(title=pltTitle, xlabel=pltXLabel, ylabel=pltYLabel)
            # 选峰 用的是tx
            tx = rgb
            peaks, properties = find_peaks(tx, height=5, distance=15)
            #这个是关键find_reaks，可以选合适的峰值，如果不滤波可能通过调好参数来选出合适的峰值
            peaksyval = tx[peaks]
            print('peaks:')
            print(peaks)
            print('peakyvals:')
            print(peaksyval)

            plt.plot(peaks[:], peaksyval, "x", color='black')
            plt.show()
            xtolen = len(rgb)
            ytolen = len(peaksyval)
            print('xtolen', xtolen, 'xtol/30', xtolen / 30)
            print('ytollen', ytolen)
            print(30 * 60 * ytolen / xtolen)
            return plt
        else:
            print('plotGofRGB sel error only 0/1')
            pass

#这个不知道手机上行不行，保存rgb
def writeGvalue(words,number):
    try:
        dir=os.makedirs('values',)
        file=open('values\\%d'%(number)+'.txt','a+',encoding='utf-8')
        file.write(str(words))
        print('write %d success'%number)
        file.close()
    except:
        file=open('values\\%d'%(number)+'.txt','a+',encoding='utf-8')
        file.write(str(words))
        print('write %d success'%number)

        file.close()

#从txt文件读取rgb值
def readGvalue(number):
    try:
        number=str(number)
        filpath=findFile('values',number,'.txt')
        thisfile=open(filpath,'r',encoding='utf-8')
        print('open %s '%number)
        array=''
        while True:
            temparray=thisfile.readline()
            temparray=temparray.strip("\n")
            if temparray=="":
                break
            array+=temparray
        array=array.strip('[')
        array=array.strip(']')

        #print(array)
        array=array.split(' ')
        #list类型的array（已经过滤空串）
        array=list(filter(lambda cx:cx!='',array))
        thisfile.close()
        return array
    except Exception as err:
        print('读取文件失败,错误原因如下')
        print(err)

#个人测试
#get_video_and_save(3)
# listi=[x for x in range(3,4)]
# listi=[x for x in range(5,6)]
# print(listi)
# for i in listi:
#     rgba=getRawofRGB('%d'%(i),'E:\\C\\pythonexercise',0)
#     plotGofRGB(rgba,'%d'%i,'pink',0)

#从csv文件读取rgb，与文件路径有关
def loadleftcsv(pnum):
    data=np.loadtxt('left\\%d.csv'%pnum,delimiter=',',skiprows=1,usecols=1)
    return data
def loadrightcsv(pnum):
    data=np.loadtxt('right\\%d.csv'%pnum,delimiter=',',skiprows=1,usecols=1)
    return data
#rgb值保存成csv文件
def saveRGB(rgb,fname,path):
    if path.exists(): # check if folders exist
        pass
    else: # create them if not
        path.mkdir()
    csvExt = fname+'.csv'
    csvName = Path.home().joinpath(path,csvExt)
    if csvName.exists(): # check if files already exist
        return 1
    else: # save the files if they don't
        np.savetxt(csvName,rgb)
        plotTitle = fname
        # plt = plotRGB(rgb,plotTitle)
        # pngExt = fname+'.png'
        # pngName = Path.home().joinpath(path,pngExt)
        # plt.savefig(pngName)
        # plt.clf()
    return 0

#个人测试
#     print(rgba)
# #writeGvalue(rgba,3)



# lili=[100001]
# for tt in lili:
#     d1=loadleftcsv(tt)
#     plotGofRGB(d1,tt,'green',0)
#     #d2=loadrightcsv(tt)
#     print(Path.home())
#     print(Path.cwd())
#     pa=Path('E:\\C\\pythonexercise\\csv')
#     saveRGB(d1,'sss',pa)
