# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:start_chat.py
@Time:2023/1/5 14:21
@Read: 
"""
from pychatgpt import Chat, Options

options = Options()

# [New] Pass Moderation. https://github.com/rawandahmad698/PyChatGPT/discussions/103
# options.pass_moderation = False

# [New] Enable, Disable logs
options.log = True

# Track conversation
options.track = True

# Use a proxy
# options.proxies = 'http://117.160.246.187:46560'
options.proxies = 'http://localhost:8080'
# options.proxies = '117.160.246.187:46560'
# options.proxies = 'http://localhost:53072/JeJ18oiHsB2CbUf4IVXp0MZN4nktgEys/fei.pac'

# Optionally, you can pass a file path to save the conversation; They're created if they don't exist
options.chat_log = "chat_log.txt"
options.id_log = "id_log.txt"

# Create a Chat object
chat = Chat(email="newswithspring@gmail.com", password="aa1230.aa", options=options)
answer = chat.ask("你好，祝你新年好！")
print(answer)

# from pychatgpt import Chat
#
# # Create a Chat object
# chat = Chat(email="email", password="password",
#             conversation_id="Parent Conversation ID",
#             previous_convo_id="Previous Conversation ID")
#
# answer, parent_conversation_id, conversation_id = chat.ask("How are you?")
#
# print(answer)

# Or change the conversation id later
# answer, _, _ = chat.ask("你好，祝你新年好！",
#                         previous_convo_id="Parent Conversation ID",
#                         conversation_id="Previous Conversation ID")
# print(answer)
