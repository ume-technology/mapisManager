# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:app.py
@Time:2023/1/6 10:04
@Read: 
"""
import json
import openai
import pickle
import requests
from flask import Flask
from flask import Flask, jsonify, request
from apiKeys import *

app = Flask(__name__)

openai.api_key = openAIKey

# prompt = "请用户外运动，悬浮式背包，超大容量写一段广告语，重点突出轻便，高效，全年龄段适用，限时特惠，希望人们快快下单。适合情人节使用，是送给女朋友的精美礼物。"
# prompt = "请针对情人节，送女友，真皮，皮包，防水，出门旅行，逛街写一段广告语，重点突出便宜实惠，坚固耐用"

# todo postman function
post_url = 'https://api.openai.com/v1/completions'
headers = {
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip,deflate',
    'Content-Length': 1024,
    'Transfer-Encoding': 'chunked',
    'Authorization': 'Bearer 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'
}
data = {
    "model": "text-davinci-003",
    "prompt": "请用户外运动，悬浮式背包，超大容量写一段广告语",
    # "prompt": prompt,
    "max_tokens": 2048,
    "temperature": 0,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0.6,
    "stop": [" Human:", " AI:"]
}


@app.route('/getAds', methods=['GET'])
def startfun():
    # standard
    if request.method == 'GET':
        prompt = request.values.get('prompt')  # 应用场景
        ads = []
        for i in range(5):
            prompt = "请根据下列关键词写一段广告：情人节，送女友，真皮，皮包，防水，出门旅行，逛街写一段广告语，重点突出便宜实惠，坚固耐用。"
            response = openai.Completion.create(
                model="text-davinci-003",
                # prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
                #        "\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\n"
                #        "Human: I'd like to cancel my subscription.\nAI:",
                prompt=prompt, temperature=0.9, max_tokens=300, top_p=1, frequency_penalty=0.0, presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )
            # res = response.to_dict()
            res = response.to_dict()['choices'][0].text
            ads.append(res + '\n')
        return ads


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=5001)
    # app.run(host='127.0.0.1', debug=True, port=5000)
    # app.run(debug=False, port=5000)
