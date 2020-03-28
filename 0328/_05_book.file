from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/reviews', methods=['POST'])
def write_review():
    # title_receive로 클라이언트가 준 title 가져오기
    title = request.form['title']
    # author_receive로 클라이언트가 준 author 가져오기
    author = request.form['author']
    # review_receive로 클라이언트가 준 review 가져오기
    review = request.form['review']

    print(title, author, review)
    db.reviews.insert_one({'title': title, 'author':author, 'review': review})
    return ''

@app.route('/reviews', methods=['GET'])
def read_reviews():
    send_data = []
    book_all_reviews = list(db.reviews.find({}))
    for reviews in book_all_reviews:
        send_data.append({
            'title':reviews['title'],
            'author':reviews['author'],
            'review':reviews['review']
        })
    return jsonify({'result':'success', 'data': send_data})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)