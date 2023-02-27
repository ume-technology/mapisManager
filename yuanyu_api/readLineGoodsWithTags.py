# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@Blog: https://www.umeai.top/
@File:readLineGoodsWithTags.py
@Time:2023/2/21 17:45
@ReadMe: 读取各个线路上老品的标签数据，方便查询获取标签
"""
import pymysql
import pandas as pd

allLabels = [
    "mar图案",
    "sce预防保护",
    "cro身体部位",
    "sce装修制造",
    "cro男性群体",
    "cro女性群体",
    "the胶皮革绒",
    "the高新技术",
    "sce户外娱乐",
    "cro工具建材",
    "cro厨房",
    "cro浴室",
    "cro生命元素",
    "sce吃美食",
    "sce整理搬运",
    "prt品类",
    "tim日常时间",
    "sce保洁洗漱",
    "sce交通出行",
    "sce运动健身",
    "cro居家",
    "cro弱势群体",
    "mar高效便捷",
    "mar风格",
    "mar舒适触感",
    "sce御寒保暖",
    "sce化妆美容",
    "mar人文宗教",
    "hod节日",
    "cro职场人群",
    "cro亲友群体",
    "the麻线丝棉",
    "sce购物送礼",
    "the植物原料",
    "mar口味",
    "mar款式",
    "mar颜色",
    "sce身体保健",
    "the金银铜铁",
    "tim秋冬时节",
    "sce维修检测",
    "sce乐业",
    "tim春夏时节",
    "cro家具设备",
    "cro有害元素",
    "cro办公学习",
    "cro娱乐场所"
]

# wait 有两个数据库，都是商品的标签信息，需要合并在一起
# todo data base select
host = '192.168.4.210'
port = 3306
user = 'zhimin'
passwd = 'uwV3n9bNPzUTf3N7'
db = 'gkml'
conn = pymysql.connect(host=host, port=port, user=user, db=db, password=passwd, charset='utf8')
cursor = conn.cursor()
# sql = """ select * from twGoods limit 1000"""
sql = """ select * from twGoods"""
# count_ = cursor.execute(sql)  # 返回的是查询到的数据库的数据条目数量
# data = cursor.fetchall()  # 获取数据
dataDF = pd.read_sql(sql, conn)
dataDF = dataDF.dropna(axis=0, subset=['opt_id'])
groupsbyID = dataDF.groupby('product_id').groups

# tagsDict = {}
# for key, lineIndex in groupsbyID.items():
#     goods_ads_with_key = dataDF.loc[lineIndex]
#     for index, row in enumerate(goods_ads_with_key.itertuples()):
#         for label in allLabels:
#             # todo 先处理一个特殊标签
#             # if label == 'prt品类':
#             #     label = '通用品类'
#             value = getattr(row, label)
#             if value == '0':
#                 continue
#             if value != '0' and label not in tagsDict:
#                 tagsDict[label] = set()
#             values = value.split()
#             for each_value in values:
#                 tagsDict[label].add(each_value)
#     a = 1
