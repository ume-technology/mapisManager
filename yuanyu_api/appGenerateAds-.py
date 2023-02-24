# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@Blog: https://www.umeai.top/
@File:appGenerateAds.py
@Time:2023/2/21 17:36
@ReadMe: 这个是为了生成广告语和新的标题
"""
import flask
from flask import Flask
from flask import Flask, jsonify, request
from apiKeys import *
import clueai
from yuanyu_api.readLineGoodsWithTags import allLabels

# app = Flask(__name__)

# todo initialize the Clueai Client with an API Key
cl = clueai.Client(yuanyuKeys, check_api_key=True)


# @app.route('/generateContent', methods=['GET', 'POST'])
def returnAds():
    prompt = '''请针对材质原料：小牛皮，产品品类：登山背包，适用场景：登山旅行，适合收纳，突出超大容量，背包坚固耐用写一段广告文案
    小元：'''
    prompt = '''请针对：矫视镜，老年，小孩；自动变焦，自动调焦，防蓝光，抗疲劳写一段广告文案
    小元：'''

    # 2022秋新款厚底摇摇鞋百搭时尚女单鞋高帮小白鞋休闲复古女鞋
    prompt = """请针对：秋冬，厚底，小白鞋，写一个商品标题
    小元："""

    """ 3.皮面透气休闲鞋一脚蹬透气皮鞋2022秋季新款工装鞋外贸批发男鞋子
        4.2022秋新款厚底摇摇鞋百搭时尚女单鞋高帮小白鞋休闲复古女鞋
        5.跨境批发皮鞋男春季2023新款男士休闲鞋一脚蹬软皮软底透气鞋子 """
    # prompt = """根据以下5个产品描述，总结出这类产品的主要特点:2022秋新款厚底摇摇鞋百搭时尚女单鞋高帮小白鞋休闲复古女鞋
    # 小元："""
    # prompt = '''根据以下1个产品描述，总结出这类产品的主要特点：高帮小白鞋女2022秋冬新款厚底中筒马丁靴外穿时尚拼接休闲运动鞋
    # 小元：'''
    # prompt = '''写一个欢迎刘同学加入ChatYuan技术交流群的欢迎词，用英文吧
    # 小元：'''

    # todo input data from opt page
    tagsDict = {
        "cro弱势群体": ["小孩", "老年", "大人"],
        "mar款式": ["自动变焦", "变焦"],
        "mar高效便捷": ["自动调节", "自动调焦", "焦距"],
        "prt品类": ["矫视镜", "眼镜"],
        "sce身体保健": ["眼科"],
        "sce预防保护": ["防蓝光", "抗疲劳"]
    }

    prompt = '''请针对：矫视镜，老年，自动变焦，防蓝光写一段广告文案
                小元：'''
    targetTags = ''
    for _, eachTagValue in tagsDict.items():
        targetTags += ','.join(eachTagValue)

    prompt = "请针对：{}，卖点信息：{}写一段广告文案" \
             "小元：".format('矫视镜', targetTags)

    prompt = "请针对：{}，卖点信息：{}写一个电商标题" \
             "小元：".format('矫视镜', targetTags)
    # todo ten piece
    # generate a prediction for a prompt；需要返回得分的话，指定return_likelihoods="GENERATION"
    for i in range(6):
        prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
        print()
        print('prediction: {}'.format(prediction.generations[0].text))  # print the predicted text
    a = 1


returnAds()
import json
import requests

url = 'http://192.168.4.132:5003/goodsInfo'
params = {
    'goodsId': 0,
    'goodsTitle': '皮面透气休闲鞋一脚蹬透气皮鞋2022秋季新款工装鞋外贸批发男鞋子'
}
# tags = requests.get(url=url, params=params).text
#
# tagDict = {}
# newTagDict = {}
# for _ in eval(tags):
#     tagCls = _[0]
#     tagValue = _[-1]
#     if tagCls not in tagDict:
#         tagDict[tagCls] = set()
#     tagDict[tagCls].add(tagValue)
# for _, v in tagDict.items():
#     newTagDict[_] = list(v)
