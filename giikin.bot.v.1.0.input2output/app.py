from flask import Flask, jsonify, request
from zhconv import convert
import re
import json
import requests
import secrets

app = Flask(__name__)


# todo 用的时候就可以调用 - 这是返回所有意图用的，什么时候用什么时候做一个 get 请求就可以
def get_all_intents():
    kv = {
        'howuse': '如何使用',
        'price': '询问商品详情(price)',
        'httpurl': 'URL',
        'greetwithnothing': '展开对话',
        'greetwithgoodsinfo': '询问商品/展开对话',
        'cancel': '取消订单',
        'usertellphone': '用户告知电话信息',
        'orderinfo': '确认订单信息',
        'express_out': '出货物流',
        'express_back': '退货物流',
        'faq/quality': '确认商品质量',
        'faq/origin': '确认产品产地',
        'faq/payment': '确认付款方式',
        'faq/receipt': '商品收据',
        'faq/store': '客服信息',
        'faq/time': '沟通收货时间',
        'faq/repeace': '骂人',
    }
    return kv


# todo-note:该方法要第一步就调用
def translatetochcha(text):
    try:
        textchn = convert(text, 'zh-cn')
        textchn = textchn.replace(' ', '')
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 匹配不是中文、大小写、数字的其他字符
        textchn_clean = cop.sub('', textchn)
        res = {'res': '如果用户输入的数据在预处理接阶段出现问题，那么将会把这句话送入模型'} if not textchn_clean else {'res': textchn_clean}
        return res
    except:
        res = {'res': '如果用户输入的数据在预处理接阶段出现问题，那么将会把这句话送入模型'}
        return res


def post(url, data=None):
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    r = json.loads(r.text)
    return r


# # todo 模型相关接口配置 POST
# @app.route('/max_conf_with_rep', methods=['POST'])
# def final_core_response():
#     import requests
#     goods = requests.get(
#         'https://gimp.giikin.com/service?service=inner.sale&action=getSaleInfo&t=1656312415&token=d3b9d87e7873363321022493025a5cfa52284c32&appKey=intent&sale_id=1001895321')
#
#     data = request.data
#     print(data)


# 模型相关接口配置 GET
@app.route('/max_conf_with_rep', methods=['GET'])
def final_core_response():
    # first：意图枚举
    allintents_kv = get_all_intents()

    # 外部传入的信息：用户消息和可能存在的商品信息
    demo_data = {
        "text": "هدى الشمري\n0596735888\nحقيبه لون بني\nعدد واحد\nوسط",
        "sale": {
            "link": "https:\/\/loy-mall.com\/index\/detail.html?sno=MTAwMjA3MTQ2MQ==&coll_id=1001755947&cssptpsywwbwhic=&from=tiktok&utm_content=1738744299177986&adset_id=1738744303785985&ad_id=1738744307431458&opt_id=631374&ttclid=E.C.P.CsQBQ3fsJHedzWpvunCeFXyx6BDFj9KKh82rzCL4YPU1GbK1f5gFHbyT2rlM-ViYRlL6a0_Oyqpyz3BVMBSqVDysBAEMxsHB-ctjxmLQzb8mL0rORGXbaXnCxysFGKB_WJog2K3Ak_2E7ZzwerJ8dTBS7JAplc5DVSKHflPBq6Mx1x9yP_wre40i_bKqD1FumBQlTeDKbQn12les3vddMHI6BFp6y5ifLzJBSqXnZRCc5VkLxwiy5hhSaLOpJIihUmeclNea-RIEdjIuMBogoYkxjNwNdU2ucGqPc1plJdG2f6naQHygGzVAyEuqLVw",
            "sale": {
                "special_price": 899,
                "product_id": 1002045,
                "product_name": "SL-直筒长裤",
                "logo_url": "https:\/\/oss.giikin.cn\/uploads\/4ccc122f15eb1c14c1bb122f98780df6.jpg",
                "lang_id": 2,
                "language": "繁体中文",
                "currency": "台币",
                "area": "神龙家族-港澳台",
                "sale_id": 1002071461,
                "sale_name": "1002045#冰絲直筒長褲",
                "sale_title": "冰絲直筒長褲",
                "options": {
                    "chinese": [
                        {
                            "name": "颜色",
                            "values": "黑色，浅灰色，深灰色"
                        },
                        {
                            "name": "尺码",
                            "values": "M，L，XL，2XL，3XL，4XL，5XL"
                        }
                    ],
                    "trans": [
                        {
                            "trans_name": "顏色",
                            "trans_values": "黑色，淺灰色，深灰色"
                        },
                        {
                            "trans_name": "尺碼",
                            "trans_values": "M (45-50kg)，L (50-57kg)，XL (57-65kg)，2XL (65-75kg)，3XL (75-85kg)，4XL (85-95kg)，5XL (95-100kg)"
                        }
                    ]
                },
                "rules": "",
                "currencyList": [

                ],
                "isMultiCurrency": 0
            }
        }
    }

    # 传入的是一个字典的情况
    text = request.values.get('text')
    sale = request.values.get('sale')

    # 只是传入一个 text 的情况
    # text = request.values.get('text')
    print('original: ', text)
    # second：用户消息预处理
    message = translatetochcha(text)
    message = message['res']
    print('after clean: ', message)

    """ 关于 rasa 服务的接口映射 - rasa . rasa 用到了下面两个服务,分别映射如下：
             1.模型相关 api-max-confidence-1 http://localhost:5005/model/parse  to  http://117.160.132.162:55555/model/parse
             2.模型相关 api-core-2 http://localhost:5005/webhooks/rest/webhook  to  http://117.160.132.162:55555/webhooks/rest/webhook
    """
    # third core-api - 1 : 调用上面的服务接口：api-max-confidence-1
    url_intents = "http://localhost:5005/model/parse"  # to  http://117.160.132.162:55555/model/parse

    data2intent = {"text": message}  # only text
    # data2intent = {"text": message, 'sale': sale}  # with sale

    data2intent = json.dumps(data2intent, ensure_ascii=False)
    data2intent = data2intent.encode(encoding="utf-8")
    r = requests.post(url=url_intents, data=data2intent)
    # print(r.text)
    print(json.loads(r.text))
    print('-----------------------------------------------------------------------------------------------------------')

    # fourth core-api - 2: 调用上面的服务接口：api-core-2
    url_core = "http://localhost:5005/webhooks/rest/webhook"  # to http://117.160.132.162:55555/webhooks/rest/webhook
    user_idx = secrets.token_urlsafe(16)  # print(type(secrets.token_urlsafe(16)))
    data2reply = {"sender": user_idx, "message": message}  # print(type(data2reply))
    # print(post(url_core, data2reply))

    # todo 返回所有的数据信息
    final_res = {'allintents': allintents_kv, 'clean_text': message,
                 'max-conf': json.loads(r.text), 'maybe-response': post(url_core, data2reply)}
    return jsonify(final_res)


if __name__ == '__main__':
    """ 这个接口作为所有所有服务的入口，这个服务里面包含了返回所有意图枚举的接口。
        因为是本地的局域网，因此做了端口映射如下：
            1.该端口(5001 ---> 55557)目前是服务的入口； 
            2.在这个主入口里，调用了 rasa core 服务的 5005(55555)；
    """
    app.run(host='0.0.0.0', debug=True, port=5001)  # to  http://117.160.132.162:55557/
