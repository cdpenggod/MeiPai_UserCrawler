# -*-coding:utf8-*-

import pandas as pd
import codecs
import csv

#对meipaiData.csv去重
def uniq():
	df=pd.read_csv('meipaiData.csv',header=0,names=['id','姓名','性别','年龄','头像','生日','星座','粉丝数','关注数','被赞数','注册时间','签名描述','主页url'])
	df=df.drop_duplicates(['id'])
	csvfile = open('meipaiData.csv','wb')
	csvfile.write(codecs.BOM_UTF8)
	df.to_csv('meipaiData.csv',index=False)
	print("去重完成")


#将meipaiData1.csv和meipaiData2.csv合并为meipaiData3.csv
def merge():
    df=pd.read_csv('meipaiData1.csv',header=0,names=['id','姓名','性别','年龄','头像','生日','星座','粉丝数','关注数','被赞数','注册时间','签名描述','主页url'])
    dfother=pd.read_csv('meipaiData2.csv',header=0,names=['id','姓名','性别','年龄','头像','生日','星座','粉丝数','关注数','被赞数','注册时间','签名描述','主页url'])
    data=pd.concat([dfother,df],axis=0)
    csvfile = open('meipaiData3.csv','wb')
    csvfile.write(codecs.BOM_UTF8)
    data.to_csv('meipaiData3.csv',index=False)
    print("合并完成")


#使用去重
uniq()

