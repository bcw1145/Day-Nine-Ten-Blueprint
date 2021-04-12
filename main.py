import requests
import os
import json
from flask import Flask, render_template, request, redirect
base_url = "http://hn.algolia.com/api/v1"

new_url = f"{base_url}/search_by_date?tags=story"

popular_url = f"{base_url}/search?tags=story"

db_new = {}
db_popular = {}

os.system("clear")


def make_detail_url(id):
    return f"{base_url}/items/{id}"


def get_item(result):
    item = json.loads(result)
    title = item['title']
    url = item['url']
    point = item['points']
    author = item['author']
    if item['children']:
        comment = item['children']
        num_comment = len(comment)
    else:
        comment = None
        num_comment = 0
    return {
        'title': title,
        'url': url,
        'point': point,
        'author': author,
        'comment': comment,
        'num_comment': num_comment
    }


def get_data_new(url):
    results = requests.get(url).text
    items = json.loads(results)
    for item in items['hits']:
        id = item['objectID']
        result = requests.get(make_detail_url(id)).text
        db_new[id] = get_item(result)


def get_data_popular(url):
    results = requests.get(url).text
    items = json.loads(results)
    for item in items['hits']:
        id = item['objectID']
        result = requests.get(make_detail_url(id)).text
        db_popular[id] = get_item(result)


app = Flask("DayNine")


@app.route("/")
def home():
    order_by = request.args.get('order_by')
    if order_by == 'new':
        if not db_new:
            get_data_new(new_url)
            db_popular.update(db_new)
        return render_template('index.html', datas=db_new)
    else:
        if not db_popular:
            get_data_popular(popular_url)
        return render_template('index.html', datas=db_popular)


@app.route("/data")
def comment():
    id = request.args.get('id')
    return render_template('detail.html', datas=db_popular[id])


app.run(host="0.0.0.0")
