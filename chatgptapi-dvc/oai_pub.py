# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:app2.py
@Time:2023/1/6 11:06
@Read: 
"""
import os
import openai
from apiKeys import *

openai.api_key = openAIKey
prompt = "请用户外运动，悬浮式背包，超大容量写一段广告语，重点突出轻便，高效，全年龄段适用，限时特惠，希望人们快快下单。适合情人节使用，是送给女朋友的精美礼物。"
response = openai.Completion.create(
    model="text-davinci-003",
    # prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
    prompt=prompt,
    temperature=0.9,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)

res = response.to_dict()['choices'][0].text
