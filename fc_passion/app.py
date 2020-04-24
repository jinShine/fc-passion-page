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

#########################################################
# Home
@app.route('/')
def home():

    notice_list = mongo.fcpassion_db().notice.find({}, {'_id': False}).sort("date", -1).limit(3)
    insta_list = mongo.fcpassion_db().instagram.find({}, {'_id': False}).sort("id", -1).limit(12)
    match_schedule_list = mongo.fcpassion_db().match_schedule.find({}, {'_id': False}).limit(3)

    return render_template(
        'home/index.html',
        notice_list=notice_list,
        match_schedule_list=match_schedule_list,
        insta_list=insta_list
    )
    
        
@app.route('/api/index', methods=['GET'])
def index():
    return jsonify({
        'result': 'success'
    })

#########################################################
# 로그인
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
                'msg': 'DB 에러, 관리자에게 문의 바랍니다.'
            })

#########################################################
# 소개
@app.route('/introduce', methods=['GET'])
def introduce_view():
    return render_template('introduce/introduce.html')

@app.route('/api/introduce/member', methods=['GET'])
def introduce_list():
    try:
        member_list = list(mongo.fcpassion_db().member.find({}, {'_id': False, 'phone': False}))
    
        return jsonify({
            'result': 'success',
            'data': member_list
        })
    except:
        return jsonify({
            'result': 'failure',
            'msg': 'DB 에러, 관리자에게 문의 바랍니다.'
        })

@app.route('/api/introduce/member-phone', methods=['GET'])
def emergency_infomation():

    if session.get('logged_in') != True :
        return jsonify({
            'result': 'failure',
            'redirect_url': '/api/login'
        })

    try:
        member_list = list(mongo.fcpassion_db().member.find({}, {'_id': False}))
    
        return jsonify({
            'result': 'success',
            'data': member_list
        })
    except:
        return jsonify({
            'result': 'failure',
            'msg': 'DB 에러, 관리자에게 문의 바랍니다.'
        })

#########################################################
# 경기 일정
@app.route('/schedule/list', methods=['GET'])
def schedule_list_view():
    if request.method == 'GET':
        return render_template('match_schedule/match_schedule_list.html')
        
@app.route('/api/schedule/list', methods=['GET'])
def schedule_list():
    if request.method == 'GET':

        try:
            match_schedule_list = mongo.fcpassion_db().match_schedule.find({}, {'_id': False})
            data = list(match_schedule_list)

            # return data
            return jsonify({
                'result': 'success',
                'data' : data
            })
        except:
            return jsonify({
                'result': 'failure'
            })

@app.route('/schedule/write', methods=['GET', 'POST'])
def schedule_write_view():
    if request.method == 'GET':
        return render_template('match_schedule/match_schedule_write.html')
    elif request.method == 'POST':

        input_title = request.form.get('title')
        input_description = request.form.get('description')
        input_date = request.form.get('date')
        input_time = request.form.get('time')


        start_time = input_time.split('-')[0]
        end_time = input_time.split('-')[1]

        start = input_date + 'T' + start_time
        end = input_date + 'T' + end_time

        list_count = len(list(mongo.fcpassion_db().match_schedule.find({}, {'_id': False})))
        schdule_id = str(list_count + 1)

        try:
            mongo.fcpassion_db().match_schedule.insert_one({
                "id": schdule_id,
                "title": input_title,
                "description": input_description,
                "start": start,
                "end": end,
                "type": "카테고리1",
                "username": "관리자",
                "backgroundColor": "#D25565",
                "textColor": "#ffffff",
                "allDay": False
            })

            return jsonify({
                'result': 'success'
            })
        except:
            return jsonify({
                'result': 'failure'
            })

@app.route('/schedule/delete', methods=['POST'])
def schedule_delite():
    if request.method == 'POST':

        schedule_id = request.form.get('id')

        try:
            mongo.fcpassion_db().match_schedule.delete_one({'id':schedule_id})

            return jsonify({
                'result': 'success',
                'msg': '삭제되었습니다.'
            })
        except:
            return jsonify({
                'result': 'failure',
                'msg': 'DB 에러, 관리자에게 문의 바랍니다.'
            })

@app.route('/schedule/update', methods=['POST'])
def schedule_update():
    if request.method == 'POST':

        schedule_id = request.form.get('id')
        schedule_title = request.form.get('title')
        schedule_start = request.form.get('start')
        schedule_end = request.form.get('end')
        schedule_description = request.form.get('description')

        try:
            mongo.fcpassion_db().match_schedule.update_one(
                {'id': schedule_id},
                {'$set': {
                    'title':schedule_title,
                'start':schedule_start,
                'end':schedule_end,
                'description':schedule_description
                }  
            })

            return jsonify({
                'result': 'success',
                'msg': '수정되었습니다.'
            })
        except:
            return jsonify({
                'result': 'failure',
                'msg': 'DB 에러, 관리자에게 문의 바랍니다.'
            })   
    

#########################################################
# 공지 사항
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

#########################################################
# 일상
@app.route('/daily-life/list', methods=['GET'])
def daily_life_list_view():
    insta_list = mongo.get_insta_api()

    return render_template(
        'daily_life/daily_life_list.html',
        insta_list=insta_list
    )

if __name__ == '__main__':
    app.run('0.0.0.0',port=5132,debug=True)