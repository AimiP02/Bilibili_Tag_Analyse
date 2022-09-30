# -*- coding:utf-8 -*-

# 定位Conda的包管理库
import sys

from requests.api import head
sys.path.append("C:\\ProgramData\\Miniconda3\\Lib\\site-packages")

import asyncio
from asyncio.events import get_event_loop
from bilibili_api import video

import bs4
import lxml
import requests
import re
from bs4 import BeautifulSoup

import pandas as pd
import time
import random
import json
import collections

from tqdm import tqdm
import math
import binascii

# 随机化User-Agent模拟登入信息
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
]
proxy_list = [
    'http://117.177.250.151:8081',
    'http://111.85.219.250:3129',
    'http://122.70.183.138:8118'
]

headers = {
    "user-agent": random.choice(user_agent),
    "cookie": "buvid3=2CDC5D14-536C-4904-A78B-23C51FEE844D155820infoc; rpdid=|(Y|YmRRRuY0J'ul)kmll)YJ; LIVE_BUVID=AUTO7615829665538340; _ga=GA1.2.1311233708.1588267031; blackside_state=1; CURRENT_FNVAL=80; buivd_fp=2CDC5D14-536C-4904-A78B-23C51FEE844D155820infoc; buvid_fp_plain=2CDC5D14-536C-4904-A78B-23C51FEE844D155820infoc; balh_is_closed=; balh_server_inner=__custom__; _uuid=8DE6DB1A-F3AE-F6CE-99E1-8401997F655953490infoc; buvid_fp=2CDC5D14-536C-4904-A78B-23C51FEE844D155820infoc; AMCV_98CF678254E93B1B0A4C98A5@AdobeOrg=359503849|MCIDTS|18734|MCMID|13684765034003240302232968420877664697|MCAAMLH-1619152037|11|MCAAMB-1619152037|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1618554437s|NONE|vVersion|5.0.1; dy_spec_agreed=1; SESSDATA=d7763ff8,1639655297,9f2eb*61; bili_jct=0eb701e82f7ef3cdd4fdeadd55f8bf1e; DedeUserID=3805775; DedeUserID__ckMd5=7fb0bde29d11859a; sid=5zebmbj9; CURRENT_BLACKGAP=1; CURRENT_QUALITY=120; fingerprint3=38e09d4b222e6218e6f386358ecb025e; fingerprint_s=0d65a194dbce9c32f1368bfe498445ea; fingerprint=a545a6171cfebc54d6c89b1c4932ead6; PVID=5; bp_t_offset_3805775=565692242803620506; arrange=matrix; bp_video_offset_3805775=565704968791787293; innersign=1; bsource=search_google"
}

# 随机获取代理ip
proxy_ip = random.choice(proxy_list)
proxies = {'http': proxy_ip}

# 获取用户搜索的Tag下综合排序状态下前15页（300个视频）的BV号并返回List
def getVideoBVID(targetTag):
    result = []
    # 解析目标网页
    for i in range(1, 11):
        if i == 1:
            targetUrl = "https://search.bilibili.com/all?keyword=" + targetTag
        else:
            targetUrl = "https://search.bilibili.com/all?keyword=" + targetTag + "&page={}".format(i)
        response = requests.get(url=targetUrl, headers=headers, proxies=proxies)
        response.encoding = "utf-8"
        searchHtml = response.text
        pageBS = BeautifulSoup(searchHtml, "lxml")
        # 定位Html中视频标题的链接
        pageBS = pageBS.find("ul", class_="video-list clearfix")
        pageBS = pageBS.find_all("a", class_="title")
        # 返回每一页视频链接List
        for page in pageBS:
            link = page.get("href")
            link = str(link).strip("//")
            link = link.split("?")
            link[0] = link[0].split("/")
            result.append(link[0][-1])
        time.sleep(1.2)
    return result

# 获取视频的泛Tag并返回Dict
async def getVideoTag(bvidList):
    temp = []
    for BVID in tqdm(bvidList):
        # 实例化Video类
        v = video.Video(bvid=BVID)
        tags = await v.get_tags()
        r = []
        for dic in tags:
            r.append(dic["tag_name"])
        temp.extend(r)
        time.sleep(1.2)
    result = collections.Counter(temp)
    # 按Tag出现次数从大至小排序
    sorted(result.items(), key=lambda x: x[1], reverse=False)
    # 返回按次数排序后前300个标签名
    return dict(result.most_common(300))

# BV号解码转AV号
def getAid(bvid):
    table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
    tr={}
    for i in range(58):
    	tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608
    r = 0
    for i in range(6):
        r += tr[bvid[s[i]]] * 58 ** i
    return (r - add) ^ xor

# 获取目标视频评论区评论总数
def getCommentSum(bvid):
    aid = getAid(bvid=bvid)
    targetUrl = "https://api.bilibili.com/x/v2/reply?type=1&oid={}&sort=0&pn=1&ps=49".format(aid)
    response = requests.get(url=targetUrl, headers=headers, proxies=proxies)
    response.encoding = "utf-8"
    data = json.loads(response.text)
    commentSum = data["data"]["page"]["acount"]
    return commentSum

# 获取目标视频评论区用户uid信息
def getCommentUsers(bvidList):
    uidList = []
    for bvid in bvidList:
        # 获取视频AV号
        aid = getAid(bvid=bvid)
        # 获取视频评论总数
        total = getCommentSum(bvid=bvid)
        # 计算爬取评论区页数
        pageNumber = int(math.ceil(total / 20))
        for i in tqdm(range(1, pageNumber + 1)):
            targetUrl = "https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&sort=0".format(i, aid)
            response = requests.get(url=targetUrl, headers=headers, proxies=proxies)
            response.encoding = "utf-8"
            data = json.loads(response.text)
            try:
                for val in data["data"]["replies"]:
                    try:
                        uid = val["member"]["mid"]
                        uidList.append(uid)
                    except Exception:
                        continue
                for val in data["data"]["hots"]:
                    try:
                        uid = val["member"]["mid"]
                        uidList.append(uid)
                    except Exception:
                        continue
            except:
                time.sleep(1)
                continue
            time.sleep(1.2)
    uidList = set(uidList)
    return list(uidList)

# 根据弹幕xml文件加密代码反查用户uid
def getUserUid(item):
    for i in range(1, 100000000):
        if binascii.crc32(str(i).encode("utf-8")) == int(item, 16):
            return i

# 获取目标视频弹幕中用户uid信息
def getDanmuUsers(bvidList):
    users = []
    for bvid in bvidList:
        # 获取视频AV号
        aid = getAid(bvid=bvid)
        # 获取视频cid
        cidUrl = "https://api.bilibili.com/x/player/pagelist?aid={}&jsonp=jsonp".format(aid)
        response = requests.get(url=cidUrl, headers=headers, proxies=proxies)
        data = json.loads(response.text)
        cid = data["data"][0]["cid"]
        # 获取视频弹幕xml文件
        danmuFileUrl = "https://comment.bilibili.com/{}.xml".format(cid)
        danmuResponse = requests.get(url=danmuFileUrl, headers=headers, proxies=proxies)
        # 处理网页访问异常
        danmuResponse.raise_for_status()
        danmuResponse.encoding = "utf-8"
        danmuBS = BeautifulSoup(danmuResponse.text, "lxml")
        danmuBS = danmuBS.find_all("d")
        for danmu in danmuBS:
            p = danmu.get("p")
            p = str(p).split(",")
            users.append(p[-3])
        time.sleep(1.2)
    users = set(users)
    result = set()
    # 将加密的用户数据解码成正确的uid
    for uid in users:
        temp = getUserUid(item=uid)
        result.add(temp)
    return list(result)

# 获取已知Tag观众的关注列表
def getFollowList(usersList):
    res = []
    for user in tqdm(usersList):
        userUP = set()
        for i in range(1, 6):
            # 逆序
            targetUrl_asc = "https://api.bilibili.com/x/relation/followings?vmid={}&pn={}&ps=50&order=asc".format(user, i)
            # 正序
            targetUrl_desc = "https://api.bilibili.com/x/relation/followings?vmid={}&pn={}&ps=50&order=desc".format(user, i)
            response_asc = requests.get(url=targetUrl_asc, headers=headers, proxies=proxies)
            response_asc.encoding = "utf-8"
            data_asc = json.loads(response_asc.text)
            # 测试用户是否关闭了关注列表
            if data_asc["message"] == "用户已设置隐私，无法查看":
                break
            response_desc = requests.get(url=targetUrl_desc, headers=headers, proxies=proxies)
            response_desc.encoding = "utf-8"
            data_desc = json.loads(response_desc.text)

            # 判断是否为空
            try:
                for key in data_desc["data"]["list"]:
                    try:
                        if key["uname"] == "账号已注销":
                            continue
                        userUP.add(key["uname"])
                    except:
                        continue
                for key in data_asc["data"]["list"]:
                    try:
                        if key["uname"] == "账号已注销":
                            continue
                        userUP.add(key["uname"])
                    except:
                        continue
            except:
                time.sleep(1)
                continue
            time.sleep(1.2)
        res.extend(list(userUP))
        time.sleep(1.2)
    result = collections.Counter(res)
    sorted(result.items(), key=lambda x: x[1], reverse=False)
    return dict(result.most_common(300))


getUserUid("f96e2b47")