# 基于协同过滤的电影推荐

# 一，介绍

数据来源：https://files.grouplens.org/datasets/movielens/ml-100k.zip

## 1.原理

> 用户协同过滤与物品协同过滤两种

```python
"""
代码流程：
item_score = []
for item in 待推荐物品集合:
    for user_like in 相似用户集合:
        score = get_score_from_similar_users() # 需要根据数据和需要设计这个函数
        item_score.append([item,score])
"""

"""
代码流程：
item_score = []
for item in 待推荐物品集合:
    for item_like in 用户喜欢的物品集合:
        score = get_score_from_similar_items()  # 需要根据数据和需要设计这个函数
        item_score.append([item,score])

"""
```

## 2.结构

```bash
│  item_cf.py  # 物品cf
│  LICENSE
│  README.md
│  user_cf.py  # 用户cf
│
└─data
    │  ml-100k.zip
    │
    └─ml-100k  # 电影评论数据集
            allbut.pl
            mku.sh
            README
            u.data
            u.genre
            u.info
            u.item
            u.occupation
            u.user
            u1.base
            u1.test
            u2.base
            u2.test
            u3.base
            u3.test
            u4.base
            u4.test
            u5.base
            u5.test
            ua.base
            ua.test
            ub.base
            ub.test
```

# 二，使用

环境

```bash
numpy==1.20.1
```

## 1.下载

## 2.运行

> 为了节约计算时间，用户协同过滤只用了前500个用户的数据，用户id输入范围（1-500）

`python user_cf.py`

```markdown
计算相似用户耗时：36.7337863445282 s
请输入待推荐用户id:>? 1
1.7831 | Living in Oblivion (1995)
1.7622 | Some Folks Call It a Sling Blade (1993)
1.7414 | Bringing Up Baby (1938)
1.7414 | Little Princess, A (1995)
1.7158 | Bitter Moon (1992)
1.6883 | Maltese Falcon, The (1941)
1.6737 | L.A. Confidential (1997)
1.6661 | Cat on a Hot Tin Roof (1958)
1.6555 | Wrong Trousers, The (1993)
1.6374 | Bridge on the River Kwai, The (1957)
1.6152 | Star Wars (1977)
1.6059 | Seven Years in Tibet (1997)
1.6059 | Amistad (1997)
1.6059 | War, The (1994)
1.6059 | Prefontaine (1997)
1.6059 | Walking and Talking (1996)
请输入待推荐用户id:>? 2
1.9419 | Eve's Bayou (1997)
1.9086 | Love Jones (1997)
1.9086 | Boy's Life 2 (1997)
1.9086 | City of Industry (1997)
1.8656 | Boot, Das (1981)
1.8132 | Antonia's Line (1995)
1.7779 | Oscar & Lucinda (1997)
1.7675 | Blues Brothers, The (1980)
1.7616 | When We Were Kings (1996)
1.7444 | Soul Food (1997)
1.7278 | Courage Under Fire (1996)
1.7234 | Midnight in the Garden of Good and Evil (1997)
1.7039 | Godfather, The (1972)
1.6518 | Titanic (1997)
1.6339 | Breaking the Waves (1996)
1.6339 | Pillow Book, The (1995)
请输入待推荐用户id:
```

> 为了节约计算时间，物品协同过滤只计算了前500个物品，用户id输入范围（1-943）

`python item_cf.py`

```bash

数据加载完成
计算相似用户耗时：21.749663829803467 s
请输入待推荐用户id:>? 1
2.4774 | Usual Suspects, The (1995)
2.3552 | Willy Wonka and the Chocolate Factory (1971)
2.3160 | Independence Day (ID4) (1996)
2.2754 | Fargo (1996)
2.2722 | Rock, The (1996)
2.2364 | Star Trek: First Contact (1996)
2.1069 | Mission: Impossible (1996)
2.0078 | Mars Attacks! (1996)
1.9687 | Twister (1996)
```
