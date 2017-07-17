import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import pandas as pd
from sklearn.cluster import KMeans

def Getdir(dirname):
    files=os.listdir(dirname)
    file_new=[]
    for i in files:
        i=dirname+'\\'+i
        file_new.append(i)
    return file_new


def Imagedata(filemane):
    datas=[]
    for i in filemane:
        im = Image.open(i)
        (width,height) = im.size
        im = im.convert("L")
        data = im.getdata()
        data = np.array(data,dtype=float)/255.0
        new_data = np.reshape(data,(height,width))
        datas.append(new_data)
        im.close()
    return datas
    
def Dictation(x):
    dic=[]
    for i,j in enumerate(x):
        a={'id':i,'pic':j}
        dic.append(a)
    return dic
    
    
a=Getdir(r'C:\Users\Administrator\Desktop\C碎纸片\附件1')
b=Imagedata(a)
b_dic=Dictation(b)
#2lie

def Uper(b,length=1):
    up=[]
    for i in b:
        a=['pic'][:length]
        a=a.reshape(-1)
        aa={'id':i['id'],'pic':a}
        up.append(aa)
    return up
        
def Downer(b,length=1):
    down=[]
    for i in b:
        a=i['pic'][-length:]
        a=a.reshape(-1)
        aa={'id':i['id'],'pic':a}
        down.append(aa)
    return down
    
def Lefter(b,length=1):
    left=[]
    for i in b:
        a=i['pic'][:,:length]
        a=a.reshape(-1)
        aa={'id':i['id'],'pic':a}
        left.append(aa)
    return left

def Righter(b,length=1):
    right=[]
    for i in b:
        a=i['pic'][:,-length:]
        a=a.reshape(-1)
        aa={'id':i['id'],'pic':a}
        right.append(aa)
    return right
#计算左右距离

def Compute(one, another):#只适合左右的
    diff=[]
    for i in one:
        cha00=[]
        for j in another:
            if i['id']==j['id']:
                pass
            else:
                cha=sum(abs(i['pic']-j['pic']))
                cha1={'sum':cha,'right':i['id'],'left':j['id']}
                cha00.append(cha1)
#        print(len(cha00))
        mini=1e10
        minione=0
        minianother=0
        for i,j in enumerate(cha00):
            if j['sum']<mini:
                mini=j['sum']
                minione=j['right']
                minianother=j['left']
        cha02={'sum':mini,'right':minione,'left':minianother}
        diff.append(cha02)
    return diff


def Bianyuan(data):#侧边缘
    sums=[]
    for i in data:
        y=i['pic'].mean()
        cha=abs(y-1)
        cha1={'cha':cha,'id':i['id']}
        sums.append(cha1)
    idc=[]
    for j in sums:
        if j['cha']==0:
            idc.append(j['id'])
    return idc

def Paixu_left(px,numlist):
    nextt=numlist[0]
    pai=[]
    for i in px:
        if i['left']==nextt:
            pai.append(nextt)
            nextt=i['right']
            break
    while len(set(pai))==len(pai):
        for i in px:
            if i['left']==nextt:
                pai.append(nextt)
                nextt=i['right']
                break
    pai.pop()
    return pai
    
def Paixu_right(px,numlist):
    nextt=numlist[0]
    pai=[]
    for i in px:
        if i['right']==nextt:
            pai.append(nextt)
            nextt=i['left']
            break
    while len(set(pai))==len(pai):
        for i in px:
            if i['right']==nextt:
                pai.append(nextt)
                nextt=i['left']
                break
    pai.pop()
    pai.reverse()
    return pai

    
def Be_in(sth,num):#选出是选中的数据
    aa=[]
    for i in sth:
        flag=0
        for j in num:
            if i['id']==j:
                flag=1
                break
        if flag==1:
            aa.append({'pic':i['pic'],'id':i['id']})
    return aa
def Be_not(sth,num):#选出不是选中的数据
    aa=[]
    for i in sth:
       flag=1
       for j in num:
           if i['id']==j:
               flag=0
               break
       if flag==1:
           aa.append({'pic':i['pic'],'id':i['id']})
    return aa
    

    
    
def Separate_to_list(x):
    idc=[]
    data=[]
    for i in x:
        idc.append(i['id'])
        data.append(i['pic'])
        
    return idc,data
    
    
def Merge_to_dict(bian,idc):
    aa=[]
    for i,j in zip(bian,idc):
        aa.append({'id':j,'lei':i})
    return aa
    
def One_dimension(x):
    aa=[]
    for i in x:
        a=np.mean(i,axis=1)
        a[a!=1]=0
        aa.append(a)
    return aa
#k means
def K_mean_list(x):
    km=KMeans(n_clusters=11,max_iter=500,tol=0.0002)
    km.fit(x)
    aa=km.predict(x)
    return aa
    
    
def Visual(data,num):
    aa=[]
    for i in num:
        for j in data:
            if j['id']==i:
                aa.append(j['pic'])
                break
    bb=np.concatenate(aa,axis=1)
    bb=bb*255
    new_im = Image.fromarray(bb.astype(np.uint8))
    new_im.show()
    return bb
    
def Save_picture(data,num):
    new_im = Image.fromarray(data.astype(np.uint8))
    new_im.show()
    new_im.save('C:\Users\Administrator\Desktop\C碎纸片\碎1题解\0000.bmp')
    ccc=pd.Series(num)
    ccc.to_csv('C:\Users\Administrator\Desktop\C碎纸片\碎1题解\0000.csv')
    
    
    
    
    
    
    
    

