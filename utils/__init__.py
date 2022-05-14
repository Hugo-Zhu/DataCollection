from . import functional as F
all_words_path = "./origin_data/shuyu_word.txt"   # 专业词表对应的路径
F.load_dict(all_words_path)  # 先导入外部词典，只用导入一次即可