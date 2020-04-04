#-*- coding:utf-8 -*-
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    # 2. articles라는 키 값으로 영화정보 내려주기
    article = list(db.article.find({},{'_id':0}))

    if len(article) == 0:
        return jsonify({'result':'empty'})
    else :
        return jsonify({'result':'success', 'msg':'GET 연결되었습니다!', 'data': article})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
	# 1. 클라이언트로부터 데이터를 받기
    print(request.form)
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

	# 2. meta tag를 스크래핑하기

    url = url_receive
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    if og_image == None:
        url_image = ''
    else:
        url_image = og_image['content']

    if og_title == None:
        url_title = '제목없음'
    else:
        url_title = og_title['content']
    
    if og_description == None:
        url_description = '내용없음'
    else:
        url_description = og_description['content']

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

	# 3. mongoDB에 데이터 넣기
    item = {
        "url": url_receive,
        "meta_title": url_title,
        "meta_image": url_image,
        "meta_description": url_description,
        "comment": comment_receive
    }

    db.article.insert_one(item)

    return jsonify({'result': 'success', 'msg':'POST 연결되었습니다!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
