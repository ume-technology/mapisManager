import requests

""" get 请求获取参数的方法 """

url = 'http://127.0.0.1:5001/'
params = {'text': '对是的哈杀手电放费'}
res = requests.get(url=url, params=params)
print(res.text)
