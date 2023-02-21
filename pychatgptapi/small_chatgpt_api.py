# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:small_chatgpt_api.py
@Time:2023/1/5 18:43
@Read: 
"""
import os
import openai

# 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
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."
           "\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
