# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@Blog: https://www.umeai.top/
@File:appGenerateAds.py
@Time:2023/2/21 17:36
@ReadMe: 这个是为了生成广告语和新的标题：为了方便优化写信息，只传递text参数的情况
"""
import re
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


def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


@app.route('/clientGenerateContent', methods=['GET', 'POST'])
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
            # for i in range(6, 11):
            #     prompt = "请针对：{}，卖点信息：{}写一个电商标题" \
            #              "小元：".format(proName, targetTags)
            #     prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
            #     results[i] = prediction.generations[0].text
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

            # todo 处理产品名：such as X22010703DB-汽车去痕研磨剂; 仅仅是为了获取这个产品的产品名（类别）
            if '-' in proName:
                proName = proName.split('-')[1]
            else:
                cut_idx = 0
                for idx, i in enumerate(proName):
                    if is_all_chinese(i):
                        cut_idx = idx
                        break
                proName = proName[cut_idx:]

            # todo text中包含的产品名也要进行上述的工作以去除相同的信息
            if '-' in text:
                text = text.split('-')[1]
            else:
                cut_idx = 0
                for idx, i in enumerate(text):
                    if is_all_chinese(i):
                        cut_idx = idx
                        break
                text = text[cut_idx:]

            # todo 直接请求产品名，最好是从产品名中识别产品的proName参数
            url = 'http://192.168.4.132:5003/goodsInfo'
            params = {'goodsId': 0, 'goodsTitle': proName}
            tags = requests.get(url=url, params=params).text
            tags = eval(tags)

            # todo 再次通过模型识别的品类标签，确定是否需要直接使用传入的proName
            #      判断有几个品类；以决定是以模型识别出来的proName还是直接传入的清洗过的产品名作为产品名
            count = 0
            for i in tags:
                if i[0] == 'prt品类':
                    count += 1
            # todo 如果模型只识别出来一个pro品类；那就把这个品类当作产品名字
            if count == 1:
                for i in tags:
                    if i[0] == 'prt品类':
                        proName = i[-1]

            # todo 这里是解析text参数以生成标签，其实这里是已经进行过当前这个产品涉及的所有的商品的标签的生成了
            #      但是这里又一次请求，是因为标签是被拼接到text中，且text还可能有新的人工输入，才又请求以捕获最完整的标签信息
            # wait  是不是应该对text进行一些分割处理？暂时是直接过model重新识别标签
            url = 'http://192.168.4.132:5003/goodsInfo'
            params = {'goodsId': 0, 'goodsTitle': text}
            tags = requests.get(url=url, params=params).text
            # print("*" * 50)
            # print(tags)
            # print("*" * 50)

            # todo model没有识别出来标签的情况
            if tags is None or not tags or len(tags) == 0:
                # todo six piece； 这种情况只有输入的text信息，不需要处理tags信息
                prompt = "请针对商品：{}，卖点如下：{}，写一段广告文案。" \
                         "小元：".format(proName, text)
                results = {}
                for i in range(6):
                    prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
                    results[i] = prediction.generations[0].text
                return {
                    "status": 2,
                    "Note": "NOTags-根据给定的产品和其背后的标签信息，"
                            "\n尝试生成了6条新的商品广告文案，仅做参考，如果使用建议组合或微调文本内容！",
                    "Ads": results
                }

            # todo 真正的基于标签进行广告生成
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

            # todo six piece ；此时其实没有用 text 信息，因为text的信息已经被简化为了从其中识别出来的tags；故单纯使用标签就可以
            prompt = "请针对商品：{}，卖点如下：{}，写一段广告文案。" \
                     "小元：".format(proName, targetTags)
            results = {}
            for i in range(6):
                prediction = cl.generate(model_name='ChatYuan-large', prompt=prompt)
                results[i] = prediction.generations[0].text
            return {
                "status": 1,
                "Note": "Giikin - 根据给定的产品和其背后的标签信息，\n"
                        "尝试生成了6条新的商品广告文案，仅做参考，如果使用建议组合或微调文本内容！",
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
