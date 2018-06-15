# -*-coding:utf8-*-

import requests
import json
import threading
import random
import sys
import os
import csv
import codecs
import datetime
import time
from imp import reload
from multiprocessing.dummy import Pool as ThreadPool


reload(sys)
sys.setdefaultencoding('utf8')


#判断文件是否存在,不存在则创建
if os.path.exists('meipaiData.csv') == False:
    with open('meipaiData.csv','wb+') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        writer.writerow(["id","姓名","性别","年龄","头像","生日","星座","粉丝数","关注数","被赞数","注册时间","签名描述","主页url"])


#设置初始默认代理ip
proxies={'http': 'http://120.26.110.59:8080'}


#定时更换新ip代理
def getNewIP():
    global proxies
#    try:
#        #可加入请求自己的代理ip设置进行定时更换
#        ipjson = requests.get('http://xxxxxx.json').text
#        ipDic = json.loads(ipjson)
#        ipArr=ipDic['proxy']
#        oneip=random.sample(ipArr,1)[0]
#        theip=str(oneip['ip'])+":"+str(oneip['port'])
#        proxies['http']=theip
#    except:
        oriIPArr=['http://120.26.110.59:8080','http://120.52.32.46:80','http://218.85.133.62:80']
        proxies['http']=random.sample(oriIPArr,1)[0]
#    finally:
        timer = threading.Timer(5,getNewIP)
        timer.start()


#计时器换代理ip
getNewIP()


head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}


#抓取用户数据(里面会筛选用户粉丝量达标的用户)
def getsource(url):
    print("开始抓:"+str(url)+"****ip地址:"+str(proxies))
    try:
        response = requests.get(url,proxies=proxies,timeout=2.5)
        jscontent = response.text
    except:
        print("请求出错"+str(url)+"****ip地址:"+str(proxies))
        return
    else:
        if response.status_code==200:
            try:
                jsDict = json.loads(jscontent)
                id=jsDict['id']
                name=jsDict['screen_name']
                gender=jsDict['gender']
                avatar=jsDict['avatar']
                birthday=jsDict['birthday']
                age=jsDict['age']
                constellation=jsDict['constellation']
                fans=jsDict['followers_count']
                followers=jsDict['friends_count']
                beLikedCount=jsDict['be_liked_count']
                url=jsDict['url']
                regtimestamp = jsDict['created_at']
                regtime_local = time.localtime(regtimestamp)
                regtime = time.strftime("%Y-%m-%d %H:%M:%S",regtime_local)
                des=jsDict['description']
                print("Succeed get user info name:"+str(name)+"****id:"+ str(id))
                
                #深度遍历抓取该用户关注列表用户数据
                #打开以下注释后会加快获取用户数据,但文件里请求到的数据会有重复,所以需要抓取完后根据文件里的用户id进行去重(查看uniq.py)
#                try:
#                    followPool.map(getFollowUid,[str(id)])
#                except Exception as e:
#                    print(e)
                #判断粉丝数是否达标
                #50000改为0即去除用户粉丝量筛选,保存所有用户数据
                if fans>=50000:
                    try:
                        with open('meipaiData.csv','ab+') as csvfile:
                            csvfile.write(codecs.BOM_UTF8)
                            writer = csv.writer(csvfile)
                            writer.writerow([str(id),str(name),str(gender),str(age),str(avatar),str(birthday),str(constellation),str(fans), \
                                             str(followers),str(beLikedCount),str(regtime),str(des),str(url)])
                            print("存入数据 name:"+str(name)+"\t粉丝:"+str(fans))
                    except Exception as e:
                        print("错误"+e)
                else:
                    print("fans不够:"+str(fans))
            except Exception as e:
                print(e)
                pass
        else:
            print("请求失败"+str(response.status_code))



#深度遍历抓取用户关注列表用户(里面会筛选用户粉丝量达标的用户)
def getFollowUid(uid):
    print("抓取用户最多100页关注列表用户"+str(uid))
    for i in range(1,100):
        url="https://api.meipai.com/friendships/friends.json?page="+str(i)+"&uid="+str(uid)
        try:
            response = requests.get(url,headers = {'content-type': 'application/json'},proxies=proxies,timeout=2.5)
            jscontent = response.text
        except:
            print("请求关注列表出错"+str(url)+"****ip地址:"+str(proxies))
            return
        else:
            try:
                list = json.loads(jscontent)
                if len(list)==0:
                    return
                for dic in list:
                    id=dic['id']
                    name=dic['screen_name']
                    gender=dic['gender']
                    avatar=dic['avatar']
                    birthday=dic['birthday']
                    age=dic['age']
                    constellation=dic['constellation']
                    fans=dic['followers_count']
                    followers=dic['friends_count']
                    beLikedCount=dic['be_liked_count']
                    url=dic['url']
                    regtimestamp = dic['created_at']
                    regtime_local = time.localtime(regtimestamp)
                    regtime = time.strftime("%Y-%m-%d %H:%M:%S",regtime_local)
                    print("成功获取关注者信息 info  name:"+str(name)+"  **id:"+ str(id))
                    #判断粉丝数是否达标
                    #50000改为0即去除用户粉丝量筛选,保存所有用户数据
                    if fans>=50000:
                        try:
                            with open('meipaiData.csv','ab+') as csvfile:
                                csvfile.write(codecs.BOM_UTF8)
                                writer = csv.writer(csvfile)
                                writer.writerow([str(id),str(name),str(gender),str(age),str(avatar),str(birthday),str(constellation),str(fans), \
                                                 str(followers),str(beLikedCount),str(regtime),"",str(url)])
                                print("存入数据 name:"+str(name)+"\t粉丝:"+str(fans))
                        except Exception as e:
                            print("错误"+e)
                    else:
                        print("关注者fans不够:"+str(fans))
                print("成功请求用户关注列表"+str(uid))
            except Exception as e:
                print(e)
                return




if __name__ == "__main__":
    #开启线程池进行抓取
    followPool = ThreadPool(2)
    pool = ThreadPool(20)
    try:
        #设定爬取的用户id范围
        for m in range(10000000,100000000):
            urls = []
            for i in range(m * 100, (m + 1) * 100):
                url = 'https://api.meipai.com/users/show.json?id=' + str(i)
                urls.append(url)
            results = pool.map(getsource,urls)

    except Exception as e:
        print(e)

    followPool.close()
    followPool.join()
    pool.close()
    pool.join()
