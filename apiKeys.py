# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:apiKeys.py
@Time:2023/2/20 13:41
@Read: 
"""
import pymysql
import pandas as pd

openAIKey = "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"
yuanyuKeys = 'Jk4lmhsCvklYhtUdyxiuK1010010001'

host = 'ro.hwaurora.rdsdb.com'
port = 3306
db = 'gdsc'
user = 'fanzhimin'
passwd = 'x%HpQhq8m9c#5zx@'
# todo connect  and  cursor
# conn = pymysql.connect(host=host, port=port, user=user, db=db, password=passwd, charset='utf8')
# cursor = conn.cursor()
# todo run select
# sql = """ """
# count_ = cursor.execute(sql)  # 返回的是查询到的数据库的数据条目数量
# data = cursor.fetchall()  # 获取数据
# todo pandas save
# dataDF = pd.read_sql(sql, conn)
