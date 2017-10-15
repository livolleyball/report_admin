# coding:utf8
from flask import request, render_template, jsonify, g
from flask_login import login_required

from test import *
from . import echarts


# conn = sqlite3.connect(os.path.join(basedir, 'data-dev.sqlite'))
# c = conn.cursor()

# from .forms import SendGoods_listdirect

def connect_db():
    """Connects to the specific database."""
    # rv = sqlite3.connect(app.config['DATABASE'])
    rv = sqlite3.connect("data-dev.sqlite")
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv


@echarts.route('/bar_line', methods=["GET", "POST"])
@login_required
def bar_line():
    if request.method == "POST":
        res = query_db("select * from weather")
        return jsonify(month=[x[0] for x in res],
                       evaporation=[x[1] for x in res],
                       precipitation=[x[2] for x in res])
    else:
        return render_template("echarts/bar_line.html")


@echarts.route('/bar1', methods=["GET", "POST"])
@login_required
def bar1():
    print(request.url_rule)
    if request.method == "POST":
        res = query_db("select * from bar1")
        return jsonify(name=[x[1] for x in res],
                       amount=[x[2] for x in res])
    else:
        return render_template("echarts/bar1.html")


@echarts.route('/bubble_gradient', methods=["GET", "POST"])
@login_required
def bubble_gradient():
    if request.method == "POST":
        res = query_db("SELECT age,population,county,year from bubble_gradient")

        a = []
        b = []
        for i in res:
            if i[3] == 1900:
                a.append(list(i))
            else:
                b.append(list(i))
        return jsonify(a, b)

    else:
        return render_template("echarts/bubble_gradient.html")

@echarts.route('/pie', methods=["GET", "POST"])
@login_required
def pie():
    list1=[]
    if request.method == "POST":
        res = query_db("SELECT county,sum(age) amount from bubble_gradient group by county")

        name=[x[0] for x in res]

        for x in res:
            dict1=dict(name=x[0],value=x[1])
            list1.append(dict1)

        return jsonify(dict(value=list1,name=name))

    else:
        return render_template("echarts/pie.html")

@echarts.route('/tree', methods=["GET", "POST"])
def tree():
    res = query_db("SELECT county,sum(age) amount from bubble_gradient group by county")
    return jsonify('a')


@echarts.route('/authMenu', methods=["GET", "POST"])
def authMenu():
    rv = query_db('''SELECT  B.id,B.parent_id,B.name,B.url,B.authlevel FROM role_auth A LEFT JOIN
      auth B ON A.auth_id= B.id
      WHERE role_id=1''')
    list = []

    def getall():
        for i in rv:
            temp = {"id": str(i[0]), "text": i[2], "href": i[3], 'level': i[4], "pid": str(0 if i[1] is None else i[1])}
            list.append(temp)
        return list

    def gettree(date, pid):
        tree = []
        for i in date:
            if i['pid'] == pid:
                # print(i['pid'],pid)
                if len(gettree(date, i['id'])) > 0:
                    if i['level'] == 1:
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
        return gettree(data, '0')
        # print(gettree(data, 0))
        # print(gettree(data, 0))

    return jsonify(maintree())
