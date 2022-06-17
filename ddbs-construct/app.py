import os
import shutil
import time
import json

from flask import Flask, request
from flask_cors import CORS

from ddbs_core import *
from hadoop.hdfs_core import HDFSCore
from mongodb.collection import *


TMP_FILE_DIR = 'static/'


app = Flask(__name__)
hdfs = HDFSCore()

CORS(app, resources={r"/*": {"origins": "*"}})

def request_parse(req):
    data = None
    if req.method == 'POST':
        data = req.form.to_dict()
    elif req.method == 'GET':
        data = req.args
    elif req.method == 'DELETE':
        print(req.form, req.data)
        data = eval(str(req.data,'utf-8'))
    else:
        raise Exception('Unsupported method: ' + req.method)
    return data


@app.route('/api/user', methods=['GET', 'POST', 'DELETE'], endpoint='user')
def manage_user():
    # get user by uid
    if request.method == 'GET':
        data = request_parse(request)
        if data.get('uid', None):
            res = DDBSCore.query_user({'uid': {'$in': data.get('uid').split(',')}})
            
            users = []
            for user in sorted(res, key=lambda x: int(x['uid'])):
                users.append({
                    'uid': user['uid'],
                    'name': user['name'],
                    'region': user['region'],
                    'gender': user['gender'],
                    'email': user['email'],
                    'phone': user['phone'],
                    'dept': user['dept'],
                    'grade': user['grade'],
                    'language': user['language'],
                    'role': user['role'],
                    'preferTags': user['preferTags'],
                    'obtainedCredits': user['obtainedCredits']
                })
            return json.dumps({'status': 'success', 'msg': 'Get users successfully', 'data': {'user': users}})
        else:
            return json.dumps({'status': 'error', 'msg': 'Missing uid'})
    # add or edit user [param: action]
    elif request.method == 'POST':
        data = request_parse(request)
        if not data.get('uid', None):
            return json.dumps({'status': 'error', 'msg': 'Missing uid'})
            
        # edit user
        if data.get('action', None) == 'edit':
            DDBSCore.update_user(data)

            return json.dumps({'status': 'success', 'msg': 'Edit user successfully'})
        # add user
        elif data.get('action', None) == 'add':
            data['id'] = 'u' + data.get('uid')
            data['timestamp'] = str(round(time.time() * 1000))
            
            DDBSCore.insert_user(data)

            return json.dumps({'status': 'success', 'msg': 'Add user successfully'})

        else:
            return json.dumps({'status': 'error', 'msg': 'Missing uid'})
    # delete user by uid
    elif request.method == 'DELETE':
        data = request_parse(request)
        if data.get('uid', None):
            DDBSCore.delete_user({'uid': data.get('uid', None)})

            return json.dumps({'status': 'success', 'msg': 'Delete user successfully'})
        else:
            return json.dumps({'status': 'error', 'msg': 'Missing uid'})
    # other request methods
    else:
        return json.dumps({'status': 'error', 'msg': 'Unsupported method: ' + request.method})


@app.route('/api/article', methods=['GET'], endpoint='article')
def manage_article():
    # get article by aid
    if request.method == 'GET':
        data = request_parse(request)
        if data.get('aid', None):
            res = DDBSCore.query_article({'aid': {'$in': data.get('aid').split(',')}})
            
            articles = []
            for article in sorted(res, key=lambda x: int(x['aid'])):
                articles.append({
                    'aid': article['aid'],
                    'title': article['title'],
                    'category': article['category'],
                    'abstract': article['abstract'],
                    'articleTags': article['articleTags'],
                    'authors': article['authors'],
                    'language': article['language'],
                    'text': article['text'],
                    'image': article['image'],
                    'video': article['video']
                })
            return json.dumps({'status': 'success', 'msg': 'Get articles successfully', 'data': {'article': articles}})
        else:
            return json.dumps({'status': 'error', 'msg': 'Missing aid'})
    # other request methods
    else:
        return json.dumps({'status': 'error', 'msg': 'Unsupported method: ' + request.method})


@app.route('/api/article/detail', methods=['GET'], endpoint='article_detail')
def get_article_status():
    # get article detail by aid
    if request.method == 'GET':
        data = request_parse(request)
        if data.get('aid', None):
            article = 'article' + data.get('aid')
            article_files = hdfs.list_article(article)
            files = {
                'jpg': [],
                'flv': ''
            }
            for file in article_files:
                ext = file.split('.')[-1]
                if ext == 'txt':
                    text = hdfs.read_file(article, file).decode('utf-8')
                elif ext == 'jpg':
                    hdfs.download_file(article, file, TMP_FILE_DIR + file)
                    files['jpg'].append('/' + TMP_FILE_DIR + file)
                elif ext == 'flv':
                    hdfs.download_file(article, file, TMP_FILE_DIR + file)
                    files['flv'] = ('/' + TMP_FILE_DIR + file)
            
            return json.dumps({'status': 'success', 'msg': 'Get article detail successfully', 'data': {'article': {'content': text, 'image': files['jpg'], 'video': files['flv']}}})
        else:
            return json.dumps({'status': 'error', 'msg': 'Missing aid'})
    # other request methods
    else:
        return json.dumps({'status': 'error', 'msg': 'Unsupported method: ' + request.method})


@app.route('/api/article/status', methods=['GET'], endpoint='article_status')
def get_article_status():
    # get article status by aid
    if request.method == 'GET':
        data = request_parse(request)
        if data.get('aid', None):
            res = DDBSCore.query_be_read({'aid': {'$in': data.get('aid').split(',')}})
            
            articles_status = []
            for article_status in sorted(res, key=lambda x: int(x['aid'])):
                articles_status.append({
                    'aid': article_status['aid'],
                    'readNum': article_status['readNum'],
                    'commentNum': article_status['commentNum'],
                    'agreeNum': article_status['agreeNum'],
                    'shareNum': article_status['shareNum']
                })
            return json.dumps({'status': 'success', 'msg': 'Get articles status successfully', 'data': {'article_status': articles_status}})
        else:
            return json.dumps({'status': 'error', 'msg': 'Missing aid'})
    # other request methods
    else:
        return json.dumps({'status': 'error', 'msg': 'Unsupported method: ' + request.method})


@app.route('/api/record/user', methods=['GET'], endpoint='user_record')
def get_record():
     # articles read by the user
    if request.method == 'GET':
        data = request_parse(request)
        if data.get('uid', None):
            res_read = DDBSCore.query_read({'uid': data.get('uid')})
            aids = list(map(lambda x: x['aid'], res_read))
            res_articles = DDBSCore.query_article({'aid': {'$in': aids}})
            
            articles = []
            for article in sorted(res_articles, key=lambda x: int(x['aid'])):
                articles.append({
                    'aid': article['aid'],
                    'title': article['title'],
                    'category': article['category'],
                    'abstract': article['abstract'],
                    'articleTags': article['articleTags'],
                    'authors': article['authors'],
                    'language': article['language'],
                    'text': article['text'],
                    'image': article['image'],
                    'video': article['video']
                })
            return json.dumps({'status': 'success', 'msg': 'Get articles read by the user successfully', 'data': {'article': articles}})
        else:
            return json.dumps({'status': 'error', 'msg': 'Missing uid'})
    # other request methods
    else:
        return json.dumps({'status': 'error', 'msg': 'Unsupported method: ' + request.method})


@app.route('/api/record/article', methods=['GET'], endpoint='article_record')
def get_record():
    # users who read the book
    if request.method == 'GET': 
        data = request_parse(request)
        if data.get('aid', None):
            res_read = DDBSCore.query_read({'aid': data.get('aid')})
            uids = list(map(lambda x: x['uid'], res_read))
            res_users = DDBSCore.query_user({'uid': {'$in': uids}})
            
            users = []
            for user in sorted(res_users, key=lambda x: int(x['uid'])):
                users.append({
                    'uid': user['uid'],
                    'name': user['name'],
                    'region': user['region'],
                    'gender': user['gender'],
                    'email': user['email'],
                    'phone': user['phone'],
                    'dept': user['dept'],
                    'grade': user['grade'],
                    'language': user['language'],
                    'role': user['role'],
                    'preferTags': user['preferTags'],
                    'obtainedCredits': user['obtainedCredits']
                })
            return json.dumps({'status': 'success', 'msg': 'Get users who read the book successfully', 'data': {'user': users}})
    # other request methods
    else:
        return json.dumps({'status': 'error', 'msg': 'Unsupported method: ' + request.method})


@app.route('/api/popular_rank', methods=['GET'], endpoint='popular_rank')
def get_popular_rank():
    if request.method == 'GET':
        data = request_parse(request)
        if not data.get('date', None):
            return json.dumps({'status': 'error', 'msg': 'Missing date'})

        if not data.get('num', None):
            return json.dumps({'status': 'error', 'msg': 'Missing num'})
        
        # get rank in a day, format: dd-mm-yyyy
        if data.get('period', None) == 'day':
            day = DateToTimestamp.day_tmp(data.get('date', None))
            res_rank = DDBSCore.query_popular_rank({'timestamp': day, 'temporalGranularity': 'daily'})
        # get rank in a week, format: ww-yyyy (ww in [00, 53])
        elif data.get('period', None) == 'week':
            week = DateToTimestamp.week_tmp(data.get('date', None))
            res_rank = DDBSCore.query_popular_rank({'timestamp': week, 'temporalGranularity': 'weekly'})
        # get rank in a month, format: mm-yyyy
        elif data.get('period', None) == 'month':
            month = DateToTimestamp.month_tmp(data.get('date', None))
            res_rank = DDBSCore.query_popular_rank({'timestamp': month, 'temporalGranularity': 'monthly'})
        # get articles
        if not res_rank:
            return json.dumps({'status': 'success', 'msg': 'No rank data'})
        aids = res_rank[0]['articleAidList'][:int(data.get('num', None))]

        res_articles = DDBSCore.query_article({'aid': {'$in': aids}})
        
        articles = []
        for article in sorted(res_articles, key=lambda x: int(x['aid'])):
            articles.append({
                'aid': article['aid'],
                'title': article['title'],
                'category': article['category'],
                'abstract': article['abstract'],
                'articleTags': article['articleTags'],
                'authors': article['authors'],
                'language': article['language'],
                'text': article['text'],
                'image': article['image'],
                'video': article['video']
            })
        return json.dumps({'status': 'success', 'msg': 'Get articles read by the user successfully', 'data': {'article': articles}})
    # other request methods
    else:
        return json.dumps({'status': 'error', 'msg': 'Unsupported method: ' + request.method})


if __name__ == '__main__':
    if not os.path.isdir(TMP_FILE_DIR):
        os.mkdir(TMP_FILE_DIR)

    app.run(debug=True, port=5001)

    if os.path.isdir(TMP_FILE_DIR):
        shutil.rmtree(TMP_FILE_DIR, ignore_errors=True)