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
# 创建表 age,population,county,year
# c.execute('''DROP TABLE IF EXISTS bubble_gradient''')
# c.execute('''CREATE TABLE bubble_gradient (year INT, county text, population INT, age INT)''')

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
# #
# for i in string.ascii_lowercase:
#     # c.execute('INSERT into bubble_gradient VALUES (?,?,?,?)',(2005,i,random.uniform(20000,30000),random.uniform(20000,30000),random.uniform(0,100)))
#     c.execute('INSERT into bubble_gradient VALUES (?,?,?,?)',
#               (2010, i, random.uniform(10000, 20000),random.uniform(20000,30000)))
# conn.commit()

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

rv = c.execute('''SELECT  B.id,B.parent_id,B.name,B.url,B.authlevel FROM role_auth A LEFT JOIN
  auth B ON A.auth_id= B.id
  WHERE role_id=1''')
list = []


def getall():
    for i in rv:
        temp = {"id": i[0], "text": i[2], "href": i[3],'level':i[4], "pid": 0 if i[1] is None else i[1] }
        list.append(temp)
    return list


def gettree(date, pid):
    tree = []
    for i in date:
        if i['pid'] == pid:
            # print(i['pid'],pid)
            if len(gettree(date, i['id'])) > 0:
                if  i['level']==1:
                    i['menu'] = gettree(date, i['id'])
                else:
                    i['items'] = gettree(date, i['id'])
            tree.append(i)
        else:
            pass
    # print(tree)
    return tree


def maintree():
    data = getall()
    # print(data)
    return gettree(data, 0)
    # print(gettree(data, 0))
    # print(gettree(data, 0))

if __name__ == '__main__':
    tree=maintree()
    print(tree)

