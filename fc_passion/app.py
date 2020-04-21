from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from flask_paginate import Pagination, get_page_parameter
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import math
import config

app = Flask(__name__)
app.secret_key = b'1234wqerasdfzxcv' 

client = MongoClient(config.MongoDB_URL, 27017)
db = client.fcpassion

@app.route('/')
def home():
    db.notice.get
    return render_template('home/index.html')
        
@app.route('/api/index', methods=['GET'])
def index():
    return jsonify({
        'result': 'success'
    })

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login/login.html')
    elif request.method == 'POST':

        input_id = request.form.get('input_id')
        input_pw = request.form.get('input_pw')

        try:
            found_admin = db.admin.find_one({
                'id': input_id,
                'pw': input_pw
            })

            if found_admin == None:
                return jsonify({
                    "result": "failure",
                    "msg": "ID 및 Password를 확인해주세요."
                })
            else:
                if not session.get('logged_in') in session:
                    session['logged_in'] = True
                    session['name'] = found_admin.get('name')
                
                print("SESSION:", session.get('logged_in'))

                return jsonify({
                    "result": "success",
                    "msg": "로그인 성공"
                })
        except:
            return jsonify({
                "result": "failure",
                "msg": "DB 에러"
            })

@app.route('/notice/search', methods=['GET'])
def notice_search_view():
    if request.method == 'GET':

        option = request.args.get('option')
        query = request.args.get('query')

        notice_collection = db.notice

        result = []

        if option == 'title':
            result = list(notice_collection.find({'title': {'$regex':query}}, {'_id': False}).sort('date', -1))
        else:
            result = list(notice_collection.find({'content': {'$regex':query}}, {'_id': False}).sort('date', -1))

        return render_template(
            'notice/notice_list.html',
            notice_list=result,
            type='search'
        )

@app.route('/api/notice/search', methods=['GET'])
def notice_search():
    if request.method == 'GET':
        return jsonify({
            'result': 'success'
        })

@app.route('/notice/list', methods=['GET'])
def notice_list_view():
    if request.method == 'GET':

        if list(db.notice.find()) == []:
            return render_template('notice/notice_list.html')

        notice_collection = db.notice
        
        offset = 0
        limit = 9

        if not request.args.get('offset') == None:
            offset = int(request.args.get('offset'))
        
        if not request.args.get('limit') == None:
            limit = int(request.args.get('limit'))

        first_id = list(notice_collection.find({}).sort('date', -1))
        last_id = first_id[offset]['date']

        notice_list = list(notice_collection.find({'date' : {'$lte' : last_id}}).sort('date', -1).limit(limit))

        next_url = '/notice/list?limit=' + str(limit) + '&offset=' + str(offset + limit)
        prev_url = '/notice/list?limit=' + str(limit) + '&offset=' + str(offset - limit)

        total = math.ceil(notice_collection.find().count() / limit)
        current_page = math.ceil((offset / limit) + 1)

        return render_template(
            'notice/notice_list.html',
            notice_list=notice_list,
            prev_url=prev_url,
            next_url=next_url,
            total=total,
            current_page=current_page
        )
            
@app.route('/api/notice/write', methods=['GET', 'POST'])
def notice_write():
    if request.method == 'GET':
        if session['logged_in'] == False:
            return redirect(url_for('login'))

        return render_template('notice/notice_write.html')
    elif request.method == 'POST':
        name = session['name']
        title = request.form.get('input_title')
        content = request.form.get('input_content')
        now = str(datetime.datetime.now()).split('.')[0]
    
        try:
            db.notice.insert_one({
                'name': name,
                'title': title,
                'content': content,
                'date': now
            })

            return jsonify({
                "result": "success",
                "msg": "공지사항 등록 성공"
            })
        except:
            return jsonify({
                "result": "failure",
                "msg": "DB 에러"
            })

@app.route('/notice/detail/<notice_id>', methods=['GET'])
def notice_detail(notice_id):
    if request.method == 'GET':
        
        notice_collection = db.notice
        notice = notice_collection.find_one({'_id': ObjectId(notice_id)})

        return render_template(
            '/notice/notice_detail.html',
            notice=notice
        )


if __name__ == '__main__':
   app.run('0.0.0.0',port=5040,debug=True)