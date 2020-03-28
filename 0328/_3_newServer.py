from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

@app.route('/')
def home():
   return render_template('cos.html')

@app.route('/jacket', methods=['POST'])
def buy_jacket():
   name = request.form['name']
   address = request.form['address']
   phone = request.form['phone']
   inputGroupSelect01 = request.form['inputGroupSelect01']
   defaultCheck1 = request.form['defaultCheck1']

   print(name, address, phone, inputGroupSelect01, defaultCheck1)
   db.jacket.insert_one({'name': name,
                          'address': address,
                          'phone': phone,
                          'inputGroupSelect01': inputGroupSelect01
                          return ''

@app.route('/jacket', methods=['GET'])
def order_jacket():
    send_data = []
    buyer_jacket = list(db.jacket.find({}))
    for jacket in buyer_jacket:
        send_data.append({
            'title':jacket['title'],
            'address': jacket['address'],
            'phone': jacket['phone'],
            'inputGroupSelect01':jacket['inputGroupSelect01']
            })
    return jsonify({'result':'success', 'data': send_data})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)