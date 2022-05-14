import re
from time import sleep as sleep
from selenium.webdriver.common.by import By
import pandas as pd
from LAC import LAC
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import tqdm

import jieba
import jieba.posseg as psg
from functools import reduce

from selenium import webdriver    # Selenium是一种自动化测试工具，爬虫中主要用来解决JavaScript渲染问题
from selenium.webdriver.chrome.options import Options

# 导入外部词典，txt格式，每行  “词汇 bio[abc]” abc分别对应1,3,5等级
def load_dict(word_path):
    jieba.load_userdict(word_path)
    jieba.initialize()
    
# 获取文字中出现的人名、机构名
def lac_name_institution(sentence):
    name_list, institution_list = [], []
    lac = LAC(mode='lac')
    lac_result = lac.run(sentence)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "PER":
            name_list.append(lac_result[0][index])
        elif lac_label == "ORG":
            institution_list.append(lac_result[0][index])
    return set(name_list), set(institution_list)

# 对news进行分词，得到其中的敏感词和等级对
def extract_mingan_words(sentence):
    pairs = psg.cut(sentence)
    lst = []
    warning_value = 0
    for pair in pairs:
        token = pair.word
        clss = pair.flag
        if "bio" not in clss:
            continue
        if [token, ord(clss[-1]) - ord('a') + 1] in lst: continue
        lst.append([token, ord(clss[-1]) - ord('a') + 1])
    return lst

# 对list进行去重
def list_duplicate_removal(list_data):
    run_function = lambda x, y: x if y in x else x + [y]
    return reduce(run_function, [[], ] + list_data)

# 计算新闻敏感值得分
def calculate_waring_value(mingan_lst):
    # 计算敏感词分数，输入与extract_mingan_words()返回的格式相同
    # 公式： 预警值=（0.5*N1 + 0.30*N2 + 0.20*N3）/（0.5*（N1+N2+N3））
    if len(mingan_lst) == 0:
        return 0.0
    fenzi, fenmu = 0, 0
    score_ratio_dct = {1: 0.2, 2: 0.3, 3: 0.5}
    for item in mingan_lst:
        fenmu += 1
        fenzi += score_ratio_dct[item[1]]
    return fenzi * 2 / fenmu

# all_words_path = "origin_data/shuyu_word.txt"   # 专业词表对应的路径
# load_dict(all_words_path)  # 先导入外部词典，只用导入一次即可


def get_keywords(file_path):
    if re.match('txt', file_path.split('.')[-1]):
        with open(file_path) as file:
            data = file.read()
            data = data.split('\n')
            keywords = []
            for keyword in data:
                keywords.append(keyword.strip('\"'))
        return keywords
    elif re.match('xlsx', file_path.split('.')[-1]):
        df = pd.read_excel(file_path)
        keywords = df['姓名'].to_list()
        return keywords
    else: raise Exception('无法从 {} 获取关键字！')