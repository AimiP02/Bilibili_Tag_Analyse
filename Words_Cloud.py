# -*- coding:utf-8 -*-

# 定位Conda的包管理库
import sys

from stylecloud.stylecloud import file_to_text
sys.path.append("C:\\ProgramData\\Miniconda3\\Lib\\site-packages")

from Bilibili_Tag_Analyse import *

import csv
import numpy as np
import pandas as pd
import stylecloud
import matplotlib.pyplot as plt
from asyncio.events import get_event_loop
from tqdm import tqdm
from PIL import Image
from time import *

def Merge(dict1, dict2):
    return (dict2.update(dict1))

# 将'Tag':'Total'、'Name':'Total'写入CSV
def writeToCSV():
    inputTag = input("请输入您想要搜索的Tag:")
    bvidList = getVideoBVID(targetTag=inputTag)
    # 获取Tag排名
    tag_dict = asyncio.get_event_loop().run_until_complete(getVideoTag(bvidList=bvidList))
    # 获取Name排名
    users_comment_list = getCommentUsers(bvidList=bvidList)
    # 
    # 弹幕反查uid时间过长舍弃部分数据
    #
    # users_danmu_list = getDanmuUsers(bvidList=bvidList);
    name_dict = getFollowList(usersList=users_comment_list)
    # 将数据写入CSV方便生成词云
    headfile = ['名称','数量']
    with open("./data_csv/tag_rank.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headfile)
        for row in tqdm(tag_dict.items()):
            writer.writerow(row)
    with open("./data_csv/name_rank.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headfile)
        for row in tqdm(name_dict.items()):
            writer.writerow(row)

# 根据CSV文件生成词云
def wordCloud():
    bg_name=np.array(Image.open("./bg_img/bella.jpg"))
    bg_tag=np.array(Image.open("./bg_img/carol.jpg"))
    stylecloud.gen_stylecloud(
        # bg=bg_tag,
        file_path="./data_csv/tag_rank.csv",
        font_path="C:\\Users\\26252\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NotoSerifCJKsc-Bold.otf",
        output_name="./image/tag_rank_cloud.png",
        palette="colorbrewer.qualitative.Set3_8",
        icon_name='fab fa-opera',
        size=1080
    )
    stylecloud.gen_stylecloud(
        bg=bg_name,
        file_path="./data_csv/name_rank.csv",
        font_path="C:\\Users\\26252\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NotoSerifCJKsc-Bold.otf",
        output_name="./image/name_rank_cloud.png",
        palette="cmocean.sequential.Haline_13"
        # icon_name='fas fa-question-circle'
    )

# 根据数据生成柱状统计图
def censusChart_tag():
    # 解决plt中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 读取CSV文件
    data_tag = pd.read_csv("./data_csv/tag_rank.csv", encoding="utf-8")
    # 绘制条形图
    fig, bx= plt.subplots()
    bx.barh(data_tag["名称"], data_tag["数量"])
    bx.set_title("Tag排行")
    bx.set_xlabel("数量")
    bx.set_ylabel("名称")
    plt.ylim(-1, 25)
    plt.gca().invert_yaxis() # 从大到小排序
    fig.set_size_inches(30, 15)
    plt.savefig("./image/tag_chart.png")

def censusChart_name():
    # 解决plt中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 读取CSV文件
    data_name = pd.read_csv("./data_csv/name_rank.csv", encoding="utf-8")
    # 绘制条形图
    fig, bx = plt.subplot()
    bx.barh(data_name["名称"], data_name["数量"])
    bx.set_title("关注的UP排行")
    bx.set_xlabel("数量")
    bx.set_ylabel("名称")
    plt.ylim(-1, 25)
    plt.gca().invert_yaxis() # 从大到小排序
    fig.set_size_inches(30, 15)
    plt.savefig("./image/name_chart.png")

if __name__ == "__main__":
    begin_time = time()
    writeToCSV()
    wordCloud()
    censusChart_tag()
    censusChart_name()
    end_time = time()
    run_time = end_time - begin_time
    print("程序运行时间：", run_time)
