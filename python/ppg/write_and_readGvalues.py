import os
def writeGvalue(words,number):
#words是代写内容，number是编号，在当前工作文件夹下创建values文件夹
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
def readGvalue(number):
    number=str(number)
    filpath=findFile('values',number,'.txt')
    file=open(filpath,'r',encoding='utf-8')
    print('open %s '%number)
    array=file.readlines()
    print(array)
    file.close()
    return array
