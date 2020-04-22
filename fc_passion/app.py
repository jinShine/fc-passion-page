import datetime
import math
import config
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from db import DB
from bson.objectid import ObjectId
from instagram_api import insta_fetch_feed

app = Flask(__name__)
app.secret_key = b'1234wqerasdfzxcv' 

mongo = DB()

@app.route('/')
def home():
    # print(list(mongo.get_insta_api()))
    # list = mongo.get_insta_api()

    notice_list = mongo.fcpassion_db().notice.find({}, {'_id': False}).sort("date", -1).limit(3)
    insta_list = mongo.fcpassion_db().instagram.find({}, {'_id': False}).sort("id", -1).limit(12)

    return render_template(
        'home/index.html',
        notice_list=notice_list,
        insta_list=insta_list
    )
        
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
            found_admin = mongo.fcpassion_db().admin.find_one({
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

        notice_collection = mongo.fcpassion_db().notice

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

        notice_collection = mongo.fcpassion_db().notice

        if list(notice_collection.find()) == []:
            return render_template('notice/notice_list.html')
        
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
        print("!!!", session.get('logged_in'))
        if session.get('logged_in') == None or session['logged_in'] == False:
            return redirect(url_for('login'))

        return render_template('notice/notice_write.html')
    elif request.method == 'POST':
        name = session['name']
        title = request.form.get('input_title')
        content = request.form.get('input_content')
        now = str(datetime.datetime.now()).split('.')[0]
    
        try:
            mongo.fcpassion_db().notice.insert_one({
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
        
        notice_collection = mongo.fcpassion_db().notice
        notice = notice_collection.find_one({'_id': ObjectId(notice_id)})

        return render_template(
            '/notice/notice_detail.html',
            notice=notice
        )


@app.route('/daily-life/list', methods=['GET'])
def daily_life_list_view():
    insta_list = mongo.get_insta_api()

    return render_template(
        'daily_life/daily_life_list.html',
        insta_list=insta_list
    )

if __name__ == '__main__':
    app.run('0.0.0.0',port=5040,debug=True)