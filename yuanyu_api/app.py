# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:app.py
@Time:2023/1/14 16:08
@Read: 
"""
import clueai
from clueai.classify import Example

cl = clueai.Client("", check_api_key=False)
response = cl.classify(
    model_name='clueai-base',
    task_name='产品分类',
    inputs=["强大图片处理器，展现自然美丽的你,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
    labels=["美颜", "二手", "外卖", "办公", "求职"])
print('prediction: {}'.format(response.classifications))

"""
curl --location --request POST 'https://www.clueai.cn/modelfun/api/serving_api'     --header 'Content-Type: application/json'     --header 'Model-name: clueai-base'     --data '{
       "task_type": "classify",
       "task_name": "产品分类",
       "input_data": ["强大图片处理器，展现自然美丽的你,修复部分小错误，提升整体稳定性。", "求闲置买卖，精品购物，上畅易无忧闲置商城，安全可信，优质商品有保障"],
       "labels": ["美颜", "二手", "外卖", "办公", "求职"]
       }'

"""
# initialize the Clueai Client with an API Key
cl = clueai.Client("", check_api_key=False)
prompt = '''
信息抽取：
这是一个高效的，适用于职场女性的背包，它漂亮，是可爱风格，让你在办公环境中脱颖而出
问题：风格，人群，地点
答案：
'''
prediction = cl.generate(model_name='clueai-base', prompt=prompt)
# 需要返回得分的话，指定return_likelihoods="GENERATION"

# print the predicted text
print('prediction: {}'.format(prediction.generations[0].text))

from PIL import Image

# import Image

cl = clueai.Client("", check_api_key=False)
response = cl.text2image(
    model_name='clueai-base',
    prompt="秋日的晚霞",
    style="毕加索",
    out_file_path="test.png")

try:
    im = Image.open('test.jpg')
    im.show()
except:
    pass
