#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: api.py

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
def get_index():
    message = request.args['msg']
    data = hyatt.status()
    #return jsonify(r)
    return render_template('status.html', message=message, status=data)


@app.route('/<string:date>', methods=['GET'])
def get_page(date):
    print('get')
    data = hyatt.get_date(date)
    if type(data) == type(''):
        # 301
        return jsonify([])
    elif data == None:
        # 301
        return jsonify([])
    elif type(data) == type([]):
        #return jsonify(data)
        return render_template('template.html', date=date, hotels=data)



if __name__ == '__main__':
    from pprint import pprint
    from Hyatt import Hyatt
    hyatt = Hyatt()
    from config import server_port
    app.run(host='0.0.0.0', port=server_port, debug=False, threaded=True, processes=False)
