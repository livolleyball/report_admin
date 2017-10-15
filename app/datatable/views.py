# coding:utf8
import pymysql
from flask import request, render_template, jsonify

from . import datatable
from .forms import SendGoods_listdirect, Buiform, CityByCityIdForm

connection = pymysql.connect(host='', user='lihm', passwd='', port=53307,
                             db='', charset='utf8')
cur = connection.cursor()


# @cache.cached(timeout=50)
@datatable.route('/sendGoods_list', methods=["GET", "POST"])
def sendGoods_list():
    if request.method == 'POST':
        # cur = connection.cursor().execute('''TopJet560Report.pr_listredbag_sendGoods(?,?,?,?)''', ['2017-08-15', '2017-08-16',
        #                                   ' ', '2'])
        limit = request.values.get('limit', type=int)
        start = request.values.get('start', type=int)
        print(limit, start)
        cur = connection.cursor()
        rv1 = cur.execute(
            '''SELECT id,ownerId,serialNo,createTime from TopJet560.orderInfo where createTime>=%s and createTime <%s''',
            ['2017-01-15', '2017-09-26'])
        rv = cur.execute(
            '''SELECT id,ownerId,serialNo,createTime from TopJet560.orderInfo where createTime>=%s and createTime <%s limit %s,%s''',
            ['2017-01-15', '2017-09-26', start, limit if limit != -1 else rv1])
        result = cur.fetchall()
        data = {"draw": 1,
                "total": rv1,
                "recordsFiltered": rv,
                'data': [{'id': rv[2], 'dt': rv[3].strftime('%Y-%m-%d')} for rv in result]}
        # data ={'data' :[rv.to_json() for rv in result]}   object has no attribute 'to_json
        return jsonify(data)
    else:
        return render_template('/datatable/sendGoods_list.html')


# @cache.cached(timeout=50)
@datatable.route('/sendGoods_listdirect', methods=["GET", "POST"])
def sendGoods_listdirect():
    form = SendGoods_listdirect()
    if form.validate_on_submit():

        cur = connection.cursor()
        rv = cur.execute(
            '''SELECT id,ownerId,serialNo,createTime from TopJet560.orderInfoHistory where createTime>=%s and createTime <%s''',
            [form.startdt.data, form.endt.data])
        if rv > 0:
            result = cur.fetchall()
            return render_template('/datatable/sendGoods_listdirect.html', form=form, result=result)
        return render_template('/datatable/sendGoods_listdirect.html', form=form)
    return render_template('/datatable/sendGoods_listdirect.html', form=form)


@datatable.route('/buiform', methods=["GET", "POST"])
def buiform():
    form = Buiform()
    if request.method == 'POST':
        ms = form.SelectMultipleField.data
        username = form.username.data
        print(username)
        print(ms)
        return render_template('/bui/form.html', form=form, ms=ms)
    return render_template('/bui/form.html', form=form)


@datatable.route('/citybycityId', methods=["GET", "POST"])
def cityBycityId():
    if request.method == 'POST':
        print([request.form['city']])
        rv = cur.execute('''select cityId,cityName from city where cityId=%s''', [request.form['city']])
        data = cur.fetchall()
        return render_template('/bui/cityBycityId.html', data=data)

    return render_template('/bui/cityBycityId.html')


@datatable.route('/citybycityIdForm', methods=["GET", "POST"])
def cityBycityIdForm():
    form = CityByCityIdForm()
    if request.method == 'POST':
        starttime = form.starttime.data
        print(starttime)
        endtime = form.endtime.data
        mobile1 = form.mobile1.data
        mobile2 = form.mobile2.data
        classify = form.classify.data
        # province =form.city.data
        city = form.city.data
        authstarttime = form.authstarttime.data
        authendtime = form.authendtime.data
        rv = cur.execute('''call TopJet560Report.report_station(%s,%s,%s,%s,%s,%s,%s,%s)''',
                         [starttime, endtime, authstarttime, authendtime,
                          mobile1, mobile2, classify, city])
        data = cur.fetchall()
        # print(data)
        return render_template('/bui/cityBycityIdForm.html', form=form, data=data)

    return render_template('/bui/cityBycityIdForm.html', form=form)


@datatable.route("/city1", methods=["GET", "POST"])
def city1():
    rv = cur.execute('''select cityId,cityName from city where parentId=0''')
    return jsonify({"city": [v for v in cur.fetchall()]})


@datatable.route("/city2/<int:province>", methods=["GET", "POST"])
def city2(province):
    rv = cur.execute('''select cityId,cityName from city where parentId=%s Union select %s cityId,'全选' cityName''',
                     (province, province))
    return jsonify({"city": [v for v in cur.fetchall()]})
