import colorama
from pathlib import Path
import os
import scipy
from scipy.signal import savgol_filter
import cv2 as cv
import numpy as np
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
from pathlib import Path
import scipy.signal as signal
# print("\033[31m这是红色字体\033[0m")
# print("\033[32m这是绿色字体\033[0m")
# print("\033[33m这是黄色字体\033[0m")
# print("\033[34m这是蓝色字体\033[0m")
# print("\033[38m这是默认字体\033[0m")  # 大于37将显示默认字体
colorama.init(autoreset=True)

def check_dir_exist_sub(pathtocheck):
    if(Path.exists(pathtocheck)):
        pass
        
    else:
        print("\033[32mWELCOME TO    USE\n-----------------------------------\033[0m")
        print("\033[31minitialization...\033[0m")
        
        Path.mkdir(pathtocheck)

        print("\033[31mplease drag .mp4 file into videofile and restart\033[0m")
        input('\033[32mPress any key to quit program.\033[0m')
        os._exit(0)

pa2=Path('videofile')

check_dir_exist_sub(pa2)

print("\033[32mWELCOME TO    USE\n-----------------------------------\033[0m")
print("CONTINUE     \033[31mY\033[0m       QUIT    \033[31mN\033[0m\n")

select=input("select: ")
if select=='N':
    pass
else:
    def check_dir_exist(pathtocheck):
        if(Path.exists(pathtocheck)):
            print("\033[32mFOLDER:  videofile   exists\033[0m")
            
        else:
            print("\033[31mFOLDER:  videlfile   does not exist\033[0m")
            print("\033[31mMAKING FOLDER videofile\033[0m")
            print("\033[31mMAKE FOLDER videofile SUCCESS\033[0m")
            Path.mkdir(pathtocheck)

    pa2=Path('videofile')

    check_dir_exist(pa2)

    def findFile(path, num, type):
        fileList = list(Path(path).rglob('*' + type))
        #print(fileList)
        file = None
        for f in fileList:
            if str(num) in f.name:
                file = f
                #print(file)
                print('analizing:       '+(f.name)+"    in    "+str(path))
            else:  # couldn't find the file
                pass
        return file

    def getRawofRGB(patientNum,dataDir,sel):
        # sel=0,blue,sel=1;green,sel=2,red
        rawFile = findFile(dataDir,patientNum,'.mp4')
        rawVid = cv.VideoCapture(rawFile.as_posix())
        vidLen = int(rawVid.get(cv.CAP_PROP_FRAME_COUNT))
        print('videolength:    ',vidLen,'frame')
        rgbArray = np.zeros(vidLen)#vidLen行，1列
        print('processing:      ' +str(rawFile.name))
        print('please wait...')
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
                #y=signal.butter(2,0.8)
                plt.plot(y, 'red', label='savgol')
                plt.legend(loc='upper right')
                plt.gca().set(title=pltTitle,xlabel=pltXLabel,ylabel=pltYLabel)
                #选峰 用的是拟合后的y
                tx=y
                peaks,properties=find_peaks(tx,height=5,distance=100)
                peaksyval=y[peaks]
                print(peaks)
                print(peaksyval)
                #
                plt.plot(peaks[:],peaksyval,"x",color='black')
                plt.show()
                xtolen = len(tx)
                ytolen = len(peaksyval)
                print('xtolen', xtolen, 'xtol/30', xtolen / 30)
                print('ytollen', ytolen)
                print(30 * 60 * ytolen / xtolen)

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
                peaks, properties = find_peaks(tx, height=5, distance=20)
                #这个是关键find_reaks，可以选合适的峰值，如果不滤波可能通过调好参数来选出合适的峰值
                peaksyval = tx[peaks]
                # print('peaks:')
                # print(peaks)
                # print('peakyvals:')
                # print(peaksyval)

                plt.plot(peaks[:], peaksyval, "x", color='black')
                plt.show()
                xtolen = len(rgb)
                ytolen = len(peaksyval)
                # print('xtolen', xtolen, 'xtol/30', xtolen / 30)
                # print('ytollen', ytolen)
                print(30 * 60 * ytolen / xtolen)
                heart=30 * 60 * ytolen / xtolen
                plt.legend('heart rate= ')
                return plt
            else:
                print('plotGofRGB sel error only 0/1')
                pass

    def getvalueofheart(rgb):
        peaks, properties = find_peaks(rgb, height=5, distance=20)
        #这个是关键find_reaks，可以选合适的峰值，如果不滤波可能通过调好参数来选出合适的峰值
        peaksyval = rgb[peaks]
        xtolen = len(rgb)
        ytolen = len(peaksyval)
        #print(30 * 60 * ytolen / xtolen)       
        heart=30 * 60 * ytolen / xtolen
        return heart
    
    


    videofile_path=str(Path.cwd())+'/videofile'
    for i in os.listdir(videofile_path):
        
        rgbto_ana=getRawofRGB(i,videofile_path,1)
        print("\033[33m\n%s\033[0m"%(str(i)),"\033[33mheart rate is \033[0m","\033[33m%d\n\033[0m"%(getvalueofheart(rgbto_ana)))
    

    input('\033[32mPress any key to quit program.\033[0m')


print("\033[32m\nGOOD BYE\033[0m")
