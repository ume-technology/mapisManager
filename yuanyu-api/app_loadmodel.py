# !usr/bin/env python
# -*- coding:utf-8 _*-
"""
@Author:UmeAI
@File:app_loadmodel.py
@Time:2023/2/15 9:21
@Read: 
"""
import torch
from transformers import AutoTokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration

print('start  loading  model. . . . . . . .')
# tokenizer = T5Tokenizer.from_pretrained(r"F:\Pictures\premodelfiles\ClueAIChatYuan-large-v1")  # todo change windows
tokenizer = T5Tokenizer.from_pretrained("/mnt/f/Pictures/premodelfiles/ClueAIChatYuan-large-v1")  # todo change linux
# model = T5ForConditionalGeneration.from_pretrained(r"F:\Pictures\premodelfiles\ClueAIChatYuan-large-v1")  # todo change windows
model = T5ForConditionalGeneration.from_pretrained("/mnt/f/Pictures/premodelfiles/ClueAIChatYuan-large-v1")  # todo change linux

device = torch.device('cuda')  # todo change linux
model.to(device)
print('end  loading  model . . . . . . .  .')


def preprocess(text):
    text = text.replace("\n", "\\n").replace("\t", "\\t")
    return text


def postprocess(text):
    return text.replace("\\n", "\n").replace("\\t", "\t")


def answer(text, sample=True, top_p=1, temperature=0.6): # 建议 temperature = 0.6
    ''' sample：是否抽样。生成任务，可以设置为True; top_p：0-1之间，生成的内容越多样'''
    text = preprocess(text)
    encoding = tokenizer(text=[text], truncation=True, padding=True, max_length=768, return_tensors="pt").to(device)  # todo change linux with GPU
    # encoding = tokenizer(text=[text], truncation=True, padding=True, max_length=768, return_tensors="pt").to('cpu')
    if not sample:
        out = model.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_new_tokens=512, num_beams=1, length_penalty=0.6)
    else:
        out = model.generate(**encoding, return_dict_in_generate=True, output_scores=False, max_new_tokens=512, do_sample=True, top_p=top_p, temperature=temperature, no_repeat_ngram_size=3)
    out_text = tokenizer.batch_decode(out["sequences"], skip_special_tokens=True)
    return postprocess(out_text[0])


print("load model end...")


def generateAdsContents(text):
    output_text = answer(text)
    # print(f"{input_text}{output_text}")
    print(f"{output_text}")


input_text = '''请针对：矫视镜，老年，小孩；自动变焦，自动调焦，防蓝光，抗疲劳写一段广告文案
小元：'''
for _ in range(5):
    print("***" * 10, _)
    generateAdsContents(input_text)

# if __name__ == '__main__':
#     # input_text = '''请针对：矫视镜，老年，小孩；自动变焦，自动调焦，防蓝光，抗疲劳写一段广告文案
#     # 小元：'''
#     input_text = '''请针对：矫视镜，老年，小孩；自动变焦，自动调焦，防蓝光，抗疲劳写一段广告文案
#     '''
#     for _ in range(5):
#         generateAdsContents(input_text)
