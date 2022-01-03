import time
import numpy as np

"""
代码流程：
item_score = []
for item in 待推荐物品集合:
    for item_like in 用户喜欢的物品集合:
        score = get_score_from_similar_items()
        item_score.append([item,score])
"""


def build_i2s_i2n(user_item_score_path, item_name_path):
    # 读取电影id-电影名字文件
    item2name = {}
    with open(item_name_path, encoding="ISO-8859-1") as lines:
        for line in lines:
            item_id, item_name = line.split('|')[:2]
            item_id = int(item_id)
            item2name[item_id] = item_name
    movie_num = len(item2name)

    # 获取用户数量
    user_dict = {}
    with open(user_item_score_path, encoding="ISO-8859-1") as lines:
        for line in lines:
            user_id, item_id, score, timestamp = line.split('\t')
            user_id, item_id, score = int(user_id), int(item_id), int(score)
            if user_id not in user_dict:
                user_dict[user_id] = user_id
    user_num = len(user_dict)

    # 读取用户id-电影id-分数文件
    item2score = {}
    with open(user_item_score_path, encoding="ISO-8859-1") as lines:
        for line in lines:
            user_id, item_id, score, timestamp = line.split('\t')
            user_id, item_id, score = int(user_id), int(item_id), int(score)
            if item_id not in item2score:
                item2score[item_id] = [0] * user_num
            item2score[item_id][user_id - 1] = score
    return item2score, item2name


def cosine(v1, v2):
    v1dv2 = v1.dot(v2)
    v1n = np.sqrt(np.sum(np.square(v1)))
    v2n = np.sqrt(np.sum(np.square(v2)))
    return v1dv2 / (v1n * v2n)


def find_similar_item(item2score):
    item2sitem = {}
    for item, score in item2score.items():
        similar_item = []
        for item_temp, score_temp in item2score.items():
            if item == item_temp or item > 500 or item_temp > 500:  # 跳过超过500的item
                continue
            similarity = cosine(np.array(score), np.array(score_temp))
            similar_item.append([item_temp, similarity])
        similar_item = sorted(similar_item, reverse=True, key=lambda x: x[1])
        item2sitem[item] = similar_item
    return item2sitem


def item_cf(user_id, item_id, item2sitem, item2score, topk):
    pred_score, count = 0, 0
    for similar_item, similarity in item2sitem[item_id][:topk]:
        score_from_similar_item = item2score[similar_item][user_id - 1]
        pred_score += score_from_similar_item * similarity
        if score_from_similar_item != 0:
            count += 1
    pred_score /= count + 1e-5
    return pred_score


def movie_recommand(user_id, item2sitem, item2score, item2name, topk=16):
    possible_items = [item_id for item_id, user_score_list in item2score.items() \
                      if item_id < 500 and user_score_list[user_id - 1] == 0]
    result = []
    for item_id in possible_items:
        score = item_cf(user_id, item_id, item2sitem, item2score, topk)
        result.append([item2name[item_id], score])
    result = sorted(result, reverse=True, key=lambda x: x[1])
    return result[:topk]


if __name__ == '__main__':

    user_item_score_path = "./data/ml-100k/u1.base"
    item_name_path = "./data/ml-100k/u.item"
    item2score, item2name = build_i2s_i2n(user_item_score_path, item_name_path)
    s = time.time()
    item2sitem = find_similar_item(item2score)
    print("计算相似用户耗时：%s s" % (time.time() - s))

    # 通过用户获取推荐电影
    while True:
        user_id = int(input('请输入待推荐用户id:'))
        recommands = movie_recommand(user_id, item2sitem, item2score, item2name)
        for recommand, score in recommands:
            print("%.4f | %s" % (score, recommand))
