# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:appGetTags.py
@Time:2023/2/14 15:37
@Read: 进行文案和Goods Title文案生成；这个版本的接口不能做微调；
       todo 如果未来需要长期稳定使用，需要把生成goods tags的服务接口部署在ap_loadmodel.py上一份。
"""
import json
import flask
import clueai
import pymysql
import pandas as pd
from flask import Flask
from flask import Flask, jsonify, request
from yuanyu_api.readLineGoodsWithTags import dataDF, groupsbyID, allLabels

app = Flask(__name__)


@app.route('/baseInfo', methods=['GET', 'POST'])
def getProductCode():
    try:
        # todo get values
        # proCode = request.args.get('proCode')
        # proCode = float(proCode)
        # proName = request.args.get('proName')
        # goodsCode = request.args.get('goodsCode')
        # lineName = request.args.get('lineName')

        # todo post values
        # postValues = request.values
        postValues = request.json
        proCode = float(postValues.get('proCode'))
        proName = postValues.get('proName')
        goodsCode = postValues.get('goodsCode')
        lineName = postValues.get('lineName')

        # todo 获取传入的productID的line index
        targetProductndex = groupsbyID[proCode]
        targetProductDF = dataDF.loc[targetProductndex]
        tagsDict = {}
        countTags = 0
        for index, row in enumerate(targetProductDF.itertuples()):
            for label in allLabels:
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
            # todo save mysql
            pass
            return {'status Code': 0, 'info': '该产品的标签暂时空缺，正在补充完善该产品的标签信息！'}
        else:
            for k, v in tagsDict.items():
                tagsDict[k] = list(v)

            # todo save mysql
            pass
            return {'status Code': 1, 'info': tagsDict}
    except Exception as e:
        print(e)
        return {'status Code': -1, 'info': '在给定产品ID和产品名称请求相应标签时，出现了一些预料之外的错误。\n'
                                           '可能是因为传入了错误的商品ID或商品名称导致商品查询时出现异常。'}


if __name__ == '__main__':
    # todo 优化使用：生成广告语之前首先获取商品标签
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run(host='127.0.0.1', debug=True, port=5000)
    # app.run(debug=False, port=5000)
