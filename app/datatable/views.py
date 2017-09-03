# coding:utf8
from . import datatable
import pymysql
from flask import request,render_template,jsonify
from .forms import SendGoods_listdirect

connection = pymysql.connect(host='', user='', passwd='', port=3307,
                             db='', charset='utf8')


@datatable.route('/sendGoods_list', methods=["GET", "POST"])
def sendGoods_list():
    if request.method == 'POST':
        # cur = connection.cursor().execute('''TopJet560Report.pr_listredbag_sendGoods(?,?,?,?)''', ['2017-08-15', '2017-08-16',
        #                                   ' ', '2'])
        cur = connection.cursor()
        rv = cur.execute('''SELECT * from allUser_newAuth where dt>=%s and dt <%s''', ('2017-07-10', '2017-08-16'))

        result = cur.fetchall()
        data = {"draw": 1,
  "recordsTotal": rv,
  "recordsFiltered": rv,
 'data':[{'id':rv[2],'dt':rv[1].strftime('%Y-%m-%d')}  for rv in result]}
        # data ={'data' :[rv.to_json() for rv in result]}   object has no attribute 'to_json
        return jsonify(data)
    else:
        return render_template('/datatable/sendGoods_list.html')

@datatable.route('/sendGoods_listdirect', methods=["GET", "POST"])
def sendGoods_listdirect():
    form = SendGoods_listdirect()
    if form.validate_on_submit():

        cur = connection.cursor()
        rv = cur.execute('''SELECT * from allUser_newAuth where dt>=%s and dt <%s''', (form.startdt.data, form.endt.data))
        if rv >0:
            result = cur.fetchall()
            return render_template('/datatable/sendGoods_listdirect.html',form=form,result=result)
        return render_template('/datatable/sendGoods_listdirect.html',form=form)
    return render_template('/datatable/sendGoods_listdirect.html',form=form)