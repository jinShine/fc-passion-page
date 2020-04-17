from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from pymongo import MongoClient
import datetime

app = Flask(__name__)
app.secret_key = b'1234wqerasdfzxcv' 

client = MongoClient('localhost', 27017)
db = client.fcpassion

@app.route('/')
def home():
    return render_template('home/index.html')

@app.route('/login', methods=['GET', 'POST'])
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
        
            
@app.route('/notice/list', methods=['GET', 'POST'])
def notice_list():
    if request.method == 'GET':

        noticeCollection = db.notice
        offset = 0
        limit = 9

        first_id = list(noticeCollection.find({}).sort('_id', 1))
        last_id = first_id[offset]['_id']

        notice_list = list(noticeCollection.find({'_id' : {'$gte' : last_id}}, {'_id': False}).sort('_id', -1).limit(limit))
        

        # for notice in notice_list:



        print(last_id)
        # return render_template('notice/notice_list.html', notice_list = notice_list)
        return jsonify({'result': notice_list})
            
@app.route('/notice/write', methods=['GET', 'POST'])
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
    
        
@app.route('/main', methods=['GET'])
def main():
    return jsonify({
        'result': 'success'
    })


if __name__ == '__main__':
   app.run('0.0.0.0',port=5047,debug=True)