# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@Blog: https://www.umeai.top/
@File:appGenerateAds.py
@Time:2023/2/21 17:36
@ReadMe: 这个是为了生成广告语和新的标题：为了方便优化写信息，只传递text参数的情况
"""
import requests
import flask
from flask import Flask
from flask import Flask, jsonify, request
from apiKeys import *
import clueai
import random

app = Flask(__name__)

# todo initialize the Clueai Client with an API Key
cl = clueai.Client(yuanyuKeys, check_api_key=True)


@app.route('/generateContent', methods=['GET', 'POST'])
def returnAds():
    # tagDict = request.args.get('tagDict')  # todo get

    # todo 不同的任务   # todo post
    # postValues = request.values
    postValues = request.json
    # print(postValues)
    taskName = postValues['taskName']  # ads / title

    if taskName == 'title':
        title = postValues['title1688']
        try:
            # todo 首先明确这个商品具备的标签
            url = 'http://192.168.4.132:5003/goodsInfo'
            params = {'goodsId': 0, 'goodsTitle': title}
            tags = requests.get(url=url, params=params).text
            if not tags or tags is None or len(tags) == 0:
                return {
                    "status": -2,
                    "Note": "由模型没有从给定的商品标题中识别出来有效的标签/卖点信息，因此无法进一步操作，请手动编写新标题"
                }
            tagDict, newTagDict = {}, {}
            for _ in eval(tags):
                tagCls = _[0]
                tagValue = _[-1]
                if tagCls not in tagDict:
                    tagDict[tagCls] = set()
                tagDict[tagCls].add(tagValue)
            for _, v in tagDict.items():
                newTagDict[_] = list(v)

            # todo 确定是什么商品 - 因为外部不传，因此这里必须有商品信息
            includeOtherCls = newTagDict.get('prt品类')  # 其实是proName
            if includeOtherCls is None:
                return {
                    "status": -1,
                    "tagInfo": "基于给定的商品标题，该商品包含如下标签/卖点信息：",
                    "tags": newTagDict,
                    "Note": "由模型没有从给定的商品标题中识别出来商品类别信息，因此无法进一步操作，请手动编写新标题!!"
                }

            # todo 有 pro proName 的情况下，抽取出来一个 proName，以备生成标题
            # print(includeOtherCls)
            proName = random.choice(includeOtherCls)
            # print(proName)

            # todo 拼接除了cls之外的其他标签信息以生成标题
            targetTags = ''
            for _, eachTagValue in newTagDict.items():
                if _ == 'prt品类':
                    continue
                targetTags += ','.join(eachTagValue)

            results = {}
            for i in range(6):
                prompt = "请针对：{}，卖点信息：{}写一个商品标题" \
                         "小元：".format(proName, targetTags)
                prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
                results[i] = prediction.generations[0].text
            for i in range(6, 11):
                prompt = "请针对：{}，卖点信息：{}写一个电商标题" \
                         "小元：".format(proName, targetTags)
                prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
                results[i] = prediction.generations[0].text
            return {
                "status": 1,
                "Note": "从给定的商品标题中抽取了如下标签卖点信息，尝试生成了6条新的商品标题，仅做参考，如果使用建议微调文本内容！",
                "tags": newTagDict,
                "titles": results
            }
        except Exception as e:
            print(e)
            return {
                "status": 0,
                "Note": "【无微调权重】在生成New Title时发生了一些预料之外的错误！请稍后再试或尝试传入新一个商品标题！",
            }

    if taskName == 'ads':
        try:
            proName = postValues.get('proName')
            proCode = float(postValues.get('proCode'))
            goodsCode = float(postValues.get('goodsCode'))
            tags = postValues.get('tags')
            text = postValues.get('text')
            lineName = postValues.get('lineName')

            """ 
            todo 这里是解析text参数以生成广告了 
            """
            # wait  是不是应该对text进行一些分割处理？暂时是直接过model重新识别标签
            url = 'http://192.168.4.132:5003/goodsInfo'
            params = {'goodsId': 0, 'goodsTitle': text}
            tags = requests.get(url=url, params=params).text
            print("*" * 50)
            print(tags)
            print("*" * 50)
            # model没有识别出来标签的情况
            if tags is None or not tags or len(tags) == 0:
                # 拼接后直接去生成广告语
                prompt = "请针对：{}，卖点信息：{}写一段广告文案" \
                         "小元：".format(proName, text)
                # todo six piece
                results = {}
                # generate a prediction for a prompt；需要返回得分的话，指定return_likelihoods = "GENERATION"
                for i in range(6):
                    prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
                    results[i] = prediction.generations[0].text
                return {
                    "status": 1,
                    "Note": "从给定的商品标题中抽取了如下标签卖点信息，尝试生成了6条新的商品广告文案，仅做参考，如果使用建议组合或微调文本内容！",
                    "Ads": results
                }
            tagDict, newTagDict = {}, {}
            for _ in eval(tags):
                tagCls = _[0]
                tagValue = _[-1]
                if tagCls not in tagDict:
                    tagDict[tagCls] = set()
                tagDict[tagCls].add(tagValue)
            for _, v in tagDict.items():
                newTagDict[_] = list(v)
            targetTags = ''
            for _, eachTagValue in newTagDict.items():
                if _ == 'prt品类':
                    continue
                targetTags += ','.join(eachTagValue)

            prompt = "请针对：{}，卖点信息：{}写一段广告文案" \
                     "小元：".format(proName, targetTags)

            # todo six piece
            results = {}
            # generate a prediction for a prompt；需要返回得分的话，指定return_likelihoods = "GENERATION"
            for i in range(6):
                prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
                results[i] = prediction.generations[0].text
            return {
                "status": 1,
                "Note": "从给定的商品标题中抽取了如下标签卖点信息，尝试生成了6条新的商品广告文案，仅做参考，如果使用建议组合或微调文本内容！",
                "Ads": results
            }
        except Exception as e:
            print(e)
            return {"status": 0, "Note": "【无微调权重】在生成新的广告文案时好像出了一些问题！"}


if __name__ == '__main__':
    # todo 优化和生成新标题使用：模型不支持微调
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=5001)
    # app.run(host='127.0.0.1', debug=True, port=5000)
    # app.run(debug=False, port=5000)
