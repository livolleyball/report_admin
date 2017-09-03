
import sqlite3
import string
import random
import json
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)
# 连接
conn = sqlite3.connect(os.path.join(basedir, 'data-dev.sqlite'))
c = conn.cursor()

# print(c)
#
# 创建表
c.execute('''DROP TABLE IF EXISTS bubble_gradient''')
c.execute('''CREATE TABLE bubble_gradient (year INT, county text, population INT, age INT)''')

# # # 数据
# # # 格式：月份,蒸发量,降水量
# # purchases = [('1月', 2, 2.6),
# #              ('2月', 4.9, 5.9),
# #              ('3月', 7, 9),
# #              ('4月', 23.2, 26.4),
# #              ('5月', 25.6, 28.7),
# #              ('6月', 76.7, 70.7),
# #              ('7月', 135.6, 175.6),
# #              ('8月', 162.2, 182.2),
# #              ('9月', 32.6, 48.7),
# #              ('10月', 20, 18.8),
# #              ('11月', 6.4, 6),
# #              ('12月', 3.3, 2.3)
# #             ]
# #
# # # 插入数据
# # c.executemany('INSERT INTO weather VALUES (?,?,?)', purchases)
# #
# # # 提交！！！
# # conn.commit()
#
for i in string.ascii_lowercase:
    c.execute('INSERT into bubble_gradient VALUES (?,?,?,?,?)',(2005,i,random.uniform(20000,30000),random.uniform(20000,30000),random.uniform(0,100)))
    c.execute('INSERT into bubble_gradient VALUES (?,?,?,?,?)',
              (1900, i, random.uniform(10000, 20000),random.uniform(20000,30000),random.uniform(0, 80)))
conn.commit()

# rv=c.execute('SELECT * from bubble_gradient')
# res=[]
# res2=[]
# # for i in rv:
# #     res.append(list(i) for i in rv if i[0]=='1900')
# # else:
# #     res2.append(list(i) for i in rv if i[0]=='2005')
# # #
# # print(rv.fetchone())
# for i in rv:
#     if i[0]=='1900':
#         res.append(list(i))
#     else:
#         res2.append(list(i))

# print(res)
# # print('''----------''')
# # for i in rv:
# #     res2=[list(i) for i in rv if i[0]=='2005']
# #
# print(res2)

# print(rv.fetchone())
