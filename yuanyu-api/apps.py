# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:apps.py
@Time:2023/2/14 15:37
@Read: 
"""
import clueai
# from apiKeys import *
import flask
from flask import Flask
from flask import Flask, jsonify, request
import pymysql
import pandas as pd
import json

app = Flask(__name__)

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
sql = """ select * from twGoods limit 1000"""
# sql = """ select * from twGoods"""
# count_ = cursor.execute(sql)  # 返回的是查询到的数据库的数据条目数量
# data = cursor.fetchall()  # 获取数据
dataDF = pd.read_sql(sql, conn)
dataDF = dataDF.dropna(axis=0, subset=['opt_id'])
groupsbyID = dataDF.groupby('product_id').groups
a = 1

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

# todo initialize the Clueai Client with an API Key
yuanyuKeys = 'Jk4lmhsCvklYhtUdyxiuK1010010001'
cl = clueai.Client(yuanyuKeys, check_api_key=True)

prompt = '''请针对材质原料：小牛皮，产品品类：登山背包，适用场景：登山旅行，适合收纳，突出超大容量，背包坚固耐用写一段广告文案
小元：'''
prompt = '''请针对：矫视镜，老年，小孩；自动变焦，自动调焦，防蓝光，抗疲劳写一段广告文案
小元：'''
# 2022秋新款厚底摇摇鞋百搭时尚女单鞋高帮小白鞋休闲复古女鞋
prompt = """请针对：秋冬，厚底，小白鞋，写一个商品标题
小元：
"""
"""
3.皮面透气休闲鞋一脚蹬透气皮鞋2022秋季新款工装鞋外贸批发男鞋子
4.2022秋新款厚底摇摇鞋百搭时尚女单鞋高帮小白鞋休闲复古女鞋
5.跨境批发皮鞋男春季2023新款男士休闲鞋一脚蹬软皮软底透气鞋子
"""

# prompt = """根据以下5个产品描述，总结出这类产品的主要特点:2022秋新款厚底摇摇鞋百搭时尚女单鞋高帮小白鞋休闲复古女鞋
# 小元：
# """

# prompt = '''根据以下1个产品描述，总结出这类产品的主要特点：高帮小白鞋女2022秋冬新款厚底中筒马丁靴外穿时尚拼接休闲运动鞋
# 小元：'''

# prompt = '''写一个欢迎刘同学加入ChatYuan技术交流群的欢迎词，用英文吧
# 小元：'''


# todo ten piece
# generate a prediction for a prompt
# 需要返回得分的话，指定return_likelihoods="GENERATION"
for i in range(10):
    prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
    print()
    # print the predicted text
    print('prediction: {}'.format(prediction.generations[0].text))
a = 1
# todo one piece
# prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
print()
# print the predicted text
print('prediction: {}'.format(prediction.generations[0].text))
a = 1


@app.route('/boseInfo', methods=['GET'])
def getProductCode():
    try:
        # todo get parameters
        proCode = request.args.get('proCode')
        proCode = float(proCode)
        # print(proCode)
        proCls = request.args.get('proCls')
        goodsCode = request.args.get('goodsCode')
        lineName = request.args.get('lineName')
        # todo 获取传入的productID的line index
        targetProductndex = groupsbyID[proCode]
        targetProductDF = dataDF.loc[targetProductndex]
        tagsDict = {}
        countTags = 0
        for index, row in enumerate(targetProductDF.itertuples()):
            for label in allLabels:
                # todo 先处理一个特殊标签
                # if label == 'prt品类':
                #     label = '通用品类'
                value = getattr(row, label)
                if value == '0':
                    continue
                else:
                    countTags = 1
                    if value != '0' and label not in tagsDict:
                        tagsDict[label] = set()
                    values = value.split()
                    for each_value in values:
                        tagsDict[label].add(each_value)
        if countTags == 0:
            return {
                'status Code': 0,
                'info': '该产品的标签暂时空缺，目前正在补充该产品的标签信息！'
            }
        else:
            for k, v in tagsDict.items():
                tagsDict[k] = list(v)
            return {
                'status Code': 1,
                'info': tagsDict
            }
    except Exception as e:
        print(e)
        return {
            # 'exception': e,
            'status Code': -1,
            'info': '参数传入错误！'
        }


@app.route('/getTags', methods=['GET'])
def returnAds():
    # parsing tags from ad public
    pass


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run(host='127.0.0.1', debug=True, port=5000)
    # app.run(debug=False, port=5000)
