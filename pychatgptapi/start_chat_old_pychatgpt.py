# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:start_chat_old_pychatgpt.py
@Time:2023/1/5 18:05
@Read: 
"""
from pychatgpt import Chat

chat = Chat(email="newswithspring@gmail.com", password="aa1230.aa")
chat.cli_chat()

# Initializing the chat class will automatically log you in, check access_tokens
chat = Chat(email="newswithspring@gmail.com", password="aa1230.aa")
answer = chat.ask("Hello!")
