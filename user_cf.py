import time
import numpy as np


def build_u2s_i2n(user_item_score_path, item_name_path):
    # 读取电影id-电影名字文件
    item2name = {}
    with open(item_name_path, encoding="ISO-8859-1") as lines:
        for line in lines:
            item_id, item_name = line.split('|')[:2]
            item_id = int(item_id)
            item2name[item_id] = item_name
    movie_num = len(item2name)

    # 读取用户id-电影id-分数文件
    user2score = {}
    with open(user_item_score_path, encoding="ISO-8859-1") as lines:
        for line in lines:
            user_id, item_id, score, timestamp = line.split('\t')
            user_id, item_id, score = int(user_id), int(item_id), int(score)
            if user_id not in user2score:
                user2score[user_id] = [0] * movie_num
            user2score[user_id][item_id - 1] = score
    return user2score, item2name


def cosine(v1, v2):
    v1dv2 = v1.dot(v2)
    v1n = np.sqrt(np.sum(np.square(v1)))
    v2n = np.sqrt(np.sum(np.square(v2)))
    return v1dv2 / (v1n * v2n)


def find_similar_user(user2score):
    user2suser = {}
    for user, score in user2score.items():
        similar_user = []
        for user_temp, score_temp in user2score.items():
            if user == user_temp or user > 500 or user_temp > 500:  # 跳过自己和编号超过500的人不然太久了
                continue
            similarity = cosine(np.array(score), np.array(score_temp))
            similar_user.append([user_temp, similarity])
        similar_user = sorted(similar_user, reverse=True, key=lambda x:x[1])
        user2suser[user] = similar_user
    return user2suser

def user_cf(user_id, item_id, user2suser, user2score, topk):
    pred_score, count = 0, 0
    for similar_user, similarity in user2suser[user_id][:topk]:
        score_from_similar_user = user2score[similar_user][item_id - 1]
        pred_score += score_from_similar_user * similarity
        if score_from_similar_user != 0:
            count += 1
    pred_score /= count + 1e-5
    return pred_score

def movie_recommand(user_id, user2suser, user2score, item2name, topk=16):
    possible_items = [item_id for item_id, score in enumerate(user2score[user_id]) if score == 0]
    result = []
    for item_id in possible_items:
        score = user_cf(user_id, item_id, user2suser, user2score, topk)
        result.append([item2name[item_id], score])
    result = sorted(result, reverse=True, key=lambda  x:x[1])
    return result[:topk]

if __name__ == '__main__':
    user_item_score_path = "./data/ml-100k/u1.base"
    item_name_path = "./data/ml-100k/u.item"
    user2score, item2name = build_u2s_i2n(user_item_score_path, item_name_path)

    # user-cf
    s = time.time()
    user2suser = find_similar_user(user2score)
    print("计算相似用户耗时：%s s" % (time.time() - s))

    # 通过用户获取推荐电影
    while True:
        user_id = int(input('请输入待推荐用户id:'))
        recommands = movie_recommand(user_id, user2suser, user2score, item2name)
        for recommand, score in recommands:
            print("%.4f | %s" % (score, recommand))
