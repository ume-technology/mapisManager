import pickle
import requests
from flask import Flask
from flask import Flask, jsonify, request

with open('all.pick', 'rb') as f:
    tags = pickle.load(f)

with open('all-no.pick', 'rb') as f:
    tags_no = pickle.load(f)

all_prt_dict = tags[5] + tags_no[5]

sp_list = []
mat_list = []
fun_list = []
for o in all_prt_dict:
    sp = o['商品卖点']
    sp_list += sp
    mt = o['商品材质或材料']
    mat_list += mt
    func = o['商品功能']
    fun_list += func

sp_list = list(set(sp_list))
mat_list = list(set(mat_list))
fun_list = list(set(fun_list))

# all_keys = list(tags[0]) + list(tags[1]) + list(tags[2]) + list(tags[3]) + list(tags[4]) \
#            + list(tags_no[0]) + list(tags_no[1]) + list(tags_no[2]) + list(tags_no[3]) + list(tags_no[4])

# all_keys = {
#     '卖点 - sp': sp_list,
#     '材料 - material': mat_list,
#     '功能 - func': fun_list,
#     '场景 - scene': list(tags[0]) + list(tags_no[0]),
#     '人群 - toobj': list(tags[1]) + list(tags_no[1]),
#     '时间 - usetime': list(tags[2]) + list(tags_no[2]),
#     '应用 - location': list(tags[3]) + list(tags_no[3]),
#     # '品牌': list(tags[4]) + list(tags_no[4]),
# }

all_keys = [
    {
        "key": "sp",
        "desc": "卖点",
        "values": sp_list
    },
    {
        "key": "material",
        "desc": "材料",
        "values": mat_list
    },
    {
        "key": "func",
        "desc": "功能",
        "values": fun_list
    },
    {
        "key": "scene",
        "desc": "场景",
        "values": list(tags[0]) + list(tags_no[0])
    },
    {
        "key": "toobj",
        "desc": "人群",
        "values": list(tags[1]) + list(tags_no[1])
    },
    {
        "key": "usetime",
        "desc": "时间",
        "values": list(tags[2]) + list(tags_no[2])
    },
    {
        "key": "location",
        "desc": "应用",
        "values": list(tags[3]) + list(tags_no[3])
    },
]

app = Flask(__name__)


@app.route('/get_tags', methods=['GET'])
def startfun():
    # return all_keys
    return jsonify(all_keys)


@app.route('/get_goods_with_tags', methods=['GET'])
def hello_world():
    try:
        # if request.method == 'GET':
        #     sp = request.values.get('sp')
        #     return sp
        if request.method == 'GET':
            # ok, no = readtags()
            to_return_goods = []
            scene = request.values.get('scene')  # 应用场景
            if scene is None:
                scene = ''
            toobj = request.values.get('toobj')  # 适用对象
            if toobj is None:
                toobj = ''
            utime = request.values.get('usetime')  # 应用时间；   比如牙刷；就不具备应用时间等标签；
            if utime is None:
                utime = ''
            location = request.values.get('location')  # 地点/位置
            if location is None:
                location = ''
            sp = request.values.get('sp')  # 卖点
            if sp is None:
                sp = ''
            material = request.values.get('material')  # 材料
            if material is None:
                material = ''
            func = request.values.get('func')  # 功能
            if func is None:
                func = ''

            suit = request.values.get('suit')
            if suit is None:
                suit = ''
            touch = request.values.get('touch')  # 不是所有商品都会有这样的标签；工具等商品可能就不具备触感；其他标签一样
            if touch is None:
                touch = ''

            for i in all_prt_dict:  #
                s_sp = i.get('商品卖点')
                if s_sp is None:
                    s_sp = []
                if isinstance(s_sp, str):
                    s_sp = [s_sp]

                s_toobj = i.get('适配人群或对象')
                if s_toobj is None:
                    s_toobj = []
                if isinstance(s_toobj, str):
                    s_toobj = [s_toobj]

                s_mat = i.get('商品材质或材料')
                if s_mat is None:
                    s_mat = []
                if isinstance(s_mat, str):
                    s_mat = [s_mat]

                s_loc = i.get('适用场地或部位')
                if s_loc is None:
                    s_loc = []
                if isinstance(s_loc, str):
                    s_loc = [s_loc]

                s_func = i.get('商品功能')
                if s_func is None:
                    s_func = []
                if isinstance(s_func, str):
                    s_func = [s_func]

                s_time = i.get('应用时间')
                if s_time is None:
                    s_time = []
                if isinstance(s_time, str):
                    s_time = [s_time]

                s_scene = i.get('适用场景')
                if s_scene is None:
                    s_scene = []
                if isinstance(s_scene, str):
                    s_scene = [s_scene]

                each_tags = s_sp + s_toobj + s_mat + s_loc + s_func + s_time + s_scene
                if not each_tags:
                    continue
                # print(each_tags)
                if sp in each_tags or toobj in each_tags or material in each_tags or location in each_tags or func \
                        in utime in each_tags or scene in each_tags:
                    to_return_goods.append({i['product_id']: i['product_name']})

            res = {
                'code': 0,
                'data': to_return_goods,
                'comment': 'success'
            }
            return jsonify(res)

    except:
        res = {
            'code': -1,
            'data': [],
            'comment': '没有符合查询条件要求的产品信息'
        }
        return jsonify(res)


code = {
    0: 'success',
    -1: '没有符合查询条件要求的产品信息'  # -1 就是没有找到符合要求的数据
}

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run(host='127.0.0.1', debug=True, port=5000)
    # app.run(debug=False, port=5000)
