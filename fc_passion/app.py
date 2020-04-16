from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from pymongo import MongoClient

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
            
            print("SESSION:", session.get('logged_in'))

            return jsonify({
                "result": "success",
                "msg": "로그인 성공"
            })
            
@app.route('/notice', methods=['GET', 'POST'])
def notice():
    if request.method == 'GET':
        if session['logged_in']:
            return render_template('notice/notice_list.html')
        else:
            return redirect(url_for('login'))
    elif request.method == 'POST':
        return render_template('notice/notice_write.html')
    
        

@app.route('/main', methods=['GET'])
def main():
    return jsonify({
        'result': 'success'
    })


if __name__ == '__main__':
   app.run('0.0.0.0',port=5045,debug=True)