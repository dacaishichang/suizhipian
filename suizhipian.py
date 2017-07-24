import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GMM
import random
import re
import cv2

def Getdir(dirname):
    files=os.listdir(dirname)
    file_new=[]
    for i in files:
        i=dirname+'\\'+i
        file_new.append(i)
    return file_new


    
    

def ReGetdir(dirname):
    files=os.listdir(dirname)
    file_new=[]
    dic=[]
    for i in files:
        i=dirname+'\\'+i
        file_new.append(i)
        dic.append(eval(re.findall('[0-9]{1,3}',i)[-1]))
    return file_new,dic
def ReDictation(x,di):
    dic=[]
    for i,j in zip(di,x):
        a={'id':i,'pic':j}
        dic.append(a)
    return dic
    
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


def Uper(b,length=1):
    up=[]
    for i in b:
        a=i['pic'][:length]
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
    one0=[i['id'] for i in one]
    another0=[i['id'] for i in another]
    num=0
    for i in one and num<=19:
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
        minione=1e10
        minianother=1e10
        for i,j in enumerate(cha00):
            if j['sum']<mini and j['left'] in another0 and j['right'] in one0:
                mini=j['sum']
                minione=j['right']
                minianother=j['left']
        if minione!=1e10 and minianother!=1e10:
            one0.remove(minione)
            another0.remove(minianother)
            cha02={'sum':mini,'right':minione,'left':minianother}
            diff.append(cha02)
            num=num+1
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
    number=0
    while len(set(pai))==len(pai) and number<200:
        number=number+1
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
    number=0
    while len(set(pai))==len(pai):
        number=number+1
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
    
def One_dimension(data):
    aa=[]
    for i in data:
        a=np.mean(i['pic'],axis=1)
        aa.append({'id':i['id'],'pic':a})
    return aa
#k means
def K_mean(data):
    dat=[]
    idc=[]
    for i in data:
        dat.append(i['pic'])
        idc.append(i['id'])
    km=KMeans(n_clusters=11,max_iter=6000,tol=0.001,n_init=3)
    km.fit(dat)
    aa=km.predict(dat)
    bb=pd.DataFrame()
    bb['id']=idc
    bb['lei']=aa
    print(bb['lei'].value_counts())
    return bb,km
    

    
def Gausian(data):
    dat=[]
    idc=[]
    for i in data:
        dat.append(i['pic'])
        idc.append(i['id'])
    km=GMM(n_components=11)
    km.fit(dat)
    aa=km.predict(dat)
    bb=pd.DataFrame()
    bb['id']=idc
    bb['lei']=aa
    print(bb['lei'].value_counts())
    return bb,km
    
    
    
def Visual_shu(data,num):
    aa=[]
    for i in num:
        for j in data:
            if j['id']==i:
                aa.append(j['pic'])
                break
    bb=np.concatenate(aa,axis=0)
    bb=bb*255
    new_im = Image.fromarray(bb.astype(np.uint8))
    new_im.show()
    return bb
    
def Visual_heng(data,num):
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
    
def Select_heng(data,num):
    aa=[]
    for i in num:
        for j in data:
            if j['id']==i:
                aa.append(j['pic'])
                break
    bb=np.concatenate(aa,axis=1)
    bb=bb*255
    return bb
def Select_zong(data,num):
    aa=[]
    for i in num:
        for j in data:
            if j['id']==i:
                aa.append(j['pic'])
                break
    bb=np.concatenate(aa,axis=0)
    bb=bb*255
    return bb
def Save_picture_pai(data,num,path):
    new_im = Image.fromarray(data.astype(np.uint8))
#    new_im.show()
    new_im.save(path+'\\'+'result.bmp')
    ccc=pd.Series(num)
    ccc.to_csv(path+'\\result.csv')
    
def Blur(data,dim):
    pic0=data['pic']
    pic1=cv2.blur(pic0,(dim,dim))
#    cv2.imshow('001',pic1)
#    cv2.waitKey(0)
    pic2={'pic':pic1,'id':data['id']}
    return pic2
    
def Fenlei(data,idc,path,num):
    dat=[]
    for i in idc:
        for j in data:
            if i==j['id']:
                dat.append(j)
                break
    for i in dat:
        new_im = Image.fromarray((i['pic']*255).astype(np.uint8))
        new_im.save(path+'\\'+str(num)+'\\'+str(i['id'])+'.bmp')
    print('OK')




save_path=r'C:\Users\Administrator\Desktop\C碎纸片\碎5题解'
read_path=r'C:\Users\Administrator\Desktop\C碎纸片\附件5'
a=Getdir(read_path)

b=Imagedata(a)
b_dic=Dictation(b)
#
#ri=Righter(b_dic,10)
#le=Lefter(b_dic,10)
#
#bian_le=Bianyuan(le)
#bian_ri=Bianyuan(ri)
##
#ri=Righter(b_dic,1)
#le=Lefter(b_dic,1)
##
#b_in=Be_in(b_dic,np.concatenate((bian_le,bian_ri),axis=0))
#b_not=Be_not(b_dic,np.concatenate((bian_le,bian_ri),axis=0))
##
#b_flatten=One_dimension(b_not)


#b_km,kmodel=K_mean(b_flatten)
##
#while True:
#    b_km,kmodel=K_mean(b_flatten)
#    print(b_km.ix[:,1].value_counts().max())
#    if b_km.ix[:,1].value_counts().max()<=34:
#        break
##        
#b_bian_flatten=One_dimension(b_in)
#dat=[]
#idc=[]
#for i in b_bian_flatten:
#    dat.append(i['pic'])
#    idc.append(i['id'])
#aa=kmodel.predict(dat)
#bb=pd.DataFrame()
#bb['id']=idc
#bb['lei']=aa
#print(bb['lei'].value_counts())
####
#for nu in range(11):
#    one_lei=b_km['id'][b_km['lei']==nu].tolist()
#    two_lei=bb['id'][bb['lei']==nu].tolist()
#    one_lei.extend(two_lei)
#    print(len(one_lei))
#    Fenlei(b_dic,one_lei,save_path,nu)
####
#bb.to_csv(r'C:\Users\Administrator\Desktop\C碎纸片\碎5题解 - 副本 (2)\边缘.csv')
#b_km.to_csv(r'C:\Users\Administrator\Desktop\C碎纸片\碎5题解 - 副本 (2)\非边缘.csv')
###-------------------------------------------------------------------------
##然后人工干预分组微调
##用分类的组来拼接
#read_path=r'C:\Users\Administrator\Desktop\C碎纸片\碎5题解'
#for k in range(10):
#    a_re,idc=ReGetdir(read_path+'\\'+str(k))
#    b_re=Imagedata(a_re)
#    b_dic=ReDictation(b_re,idc)
#    ri=Righter(b_dic,5)
#    le=Lefter(b_dic,5)
#
#    bian_le=Bianyuan(le)
#    bian_ri=Bianyuan(ri)
#
#    ri=Righter(b_dic,1)
#    le=Lefter(b_dic,1)
#
#    save_path=r'C:\Users\Administrator\Desktop\C碎纸片\碎5题解\heng'+'\\'+str(k)
#    for i in range(200):
#        random.shuffle(le)
#        random.shuffle(ri)
#        aa=Compute(le,ri)
#        random.shuffle(bian_le)
#        bb=Paixu_left(aa,bian_le)
#        if len(bb)==19:
#            ff=Select_heng(b_dic,bb)
#            new_im1 = Image.fromarray((ff).astype(np.uint8))
#            new_im1.save(save_path+'\\'+str(i)+'.bmp')
#            bb=pd.Series(bb)
#            bb.to_csv(save_path+'\\'+str(i)+'.csv')
###之后在人工筛选，选出最佳的拼图横条，再导入进行上下拼接
###----------------------------------------------------------------------------------
#read_path=r'C:\Users\Administrator\Desktop\C碎纸片\碎3题解\zong'
#save_path=r'C:\Users\Administrator\Desktop\C碎纸片\碎3题解\总'
#a,idc=ReGetdir(read_path)
#b=Imagedata(a)
#b_dic=ReDictation(b,idc)
#
#
#up=Uper(b_dic,25)
#do=Downer(b_dic,25)
#
#bian_up=Bianyuan(up)
#bian_do=Bianyuan(do)
#
#b_not=Be_not(b_dic,np.concatenate((bian_up,bian_do),axis=0))
#b_in=Be_in(b_dic,np.concatenate((bian_up,bian_do),axis=0))
#
#le=Uper(b_dic,1)
#ri=Downer(b_dic,1)
#
#
#for i in range(100):
#    random.shuffle(le)
#    random.shuffle(ri)
#    bb=Compute(le,ri)
#    cc=Paixu_left(bb,bian_up)
#    if len(cc)==11:
#        ee=Select_zong(b_dic,cc)
#        new_im0 = Image.fromarray((ee).astype(np.uint8))
#        new_im0.save(save_path+'\\'+str(i)+'.bmp')
#        dd=pd.Series(cc)
#        dd.to_csv(save_path+'\\'+str(i)+'.csv')
###-----------------------------------------------------------------------------
###人工筛选 便邮为首 且折为尾
###然后再进行表格处理
#read_path=r'C:\Users\Administrator\Desktop\C碎纸片\碎4题解\csv'
#save_path=r'C:\Users\Administrator\Desktop\C碎纸片\碎4题解'
#aa=[]
#for i in range(11):
#    c=pd.read_csv(read_path+'\\'+str(i)+'.csv',header=None)
#    aa.append(c.ix[:,1].values)
#
#bb=np.vstack(aa)
#z=pd.read_csv(read_path+'\\'+'zong.csv',header=None)
#z=z.ix[:,1].values
#
#cc=[]
#for i in z:
#    cc.append(bb[i])
#    
#cc=pd.DataFrame(cc)
#cc.to_csv(save_path+'\\'+'表格.csv')
