# -*- coding: utf-8 -*-
'''
Created on 2019/04/18

@author: Rohto
'''
from requests_oauthlib import OAuth1Session
import os, json, datetime, time, sys

# twitterセッション取得
def createTwitterSession():
    session = OAuth1Session(os.environ['CONSUMER_KEY'],os.environ['CONSUMER_SECRET'],\
                            os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    return session

# 回数制限を問合せ、アクセス可能になるまで wait する
def checkLimit(session):
    unavailableCnt = 0
    while True:
        url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
        res = session.get(url)
        
        if res.status_code == 503:
            # 503 : Service Unavailable
            if unavailableCnt > 10:
                raise Exception('Twitter API error %d' % res.status_code)
            
            unavailableCnt += 1
            print ('Service Unavailable 503')
            waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
            continue
        
        unavailableCnt = 0
        
        if res.status_code != 200:
            raise Exception('Twitter API error %d' % res.status_code)
        
        remaining, reset = getLimitContext(json.loads(res.text))
        if (remaining == 0):
            waitUntilReset(reset)
        else:
            break

def waitUntilReset(reset):
    '''
    reset 時刻まで sleep
    '''
    seconds = reset - time.mktime(datetime.datetime.now().timetuple())
    seconds = max(seconds, 0)
    print ('\n     =====================')
    print ('     == waiting %d sec ==' % seconds)
    print ('     =====================')
    sys.stdout.flush()
    time.sleep(seconds + 10)  # 念のため + 10 秒
    
def getLimitContext(res_text):
    '''
    回数制限の情報を取得 （起動時）
    '''
    remaining = res_text['resources']['statuses']['/statuses/user_timeline']['remaining']
    reset     = res_text['resources']['statuses']['/statuses/user_timeline']['reset']
    
    return int(remaining), int(reset)

# アクセス制限情報を表示する
def showLimit(res):
    print ('アクセス可能回数 %s' % res.headers['X-Rate-Limit-Remaining'])
    sec = int(res.headers['X-Rate-Limit-Reset'])\
               - time.mktime(datetime.datetime.now().timetuple())
    print ('リセット時間 （残り秒数に換算） %s' % sec)
    
    
# 最古取得日付を設定する
# 引数はres_text['statuses']を受け取る
def getOldDate(tweet_data):
    length = len(tweet_data)
    last_created_at = tweet_data['statuses'][length-1]['created_at']
    return last_created_at

# tmp_tweet_list から tmp_user_infoに設定する
# 一人分
def setToUserInfo(tmp_user_info, info, index):
    # tmp_user_info = info[各種情報]
    # 無加工データ
    tmp_user_info[str(index)] ={
        'id' : info['id'],
        'name' : info['name'],
        'screen_name' : info['screen_name'],
        'friends_count' : info['friends_count'],
        'followers_count' : info['followers_count'],
        'statuses_count' : info['statuses_count'],
        'favourites_count' : info['favourites_count'],
        'created_at' : info['created_at'],
        'profile_image_url' : info['profile_image_url'],
        'description' : info['description']
        }
    
    # 加工データ
    # フォロー数 / フォロワー数(値が大きい程一方的なフォローが多い)
    if info['friends_count'] != 0 and info['followers_count'] != 0:
        tmp_user_info[str(index)]['followers_rate'] = info['friends_count'] / info['followers_count']
    else:
        tmp_user_info[str(index)]['followers_rate'] = 0
    # いいね数 / Tweet数（値が大きい程いいね数が多い）
    if info['favourites_count'] != 0 and info['statuses_count'] != 0:
        tmp_user_info[str(index)]['favorites_rate'] = info['favourites_count'] / info['statuses_count']
    else:
        tmp_user_info[str(index)]['favorites_rate'] = 0

    print(tmp_user_info)
    return tmp_user_info

# status_idで指定したTweetを取得する
def getTweetById(twitter, status_id):
#     url= 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
    url= 'https://api.twitter.com/1.1/statuses/show.json'
    params = {
        'id':status_id,
        'lang':'ja',
        'result_type':'recent',
        'count': 100
    }
    res = twitter.get(url, params=params)
#     res_json = json.loads(res.text)
#     print(json.dumps(res_json, sort_keys=True, indent=4, ensure_ascii=False))
    return res

# in  url
# out status_id
def getStatusIdByUrl(url):
    slash_position = url.rfind('/')
    status_id = url[slash_position+1:]
    return status_id

# in res
# out show_tweet_text
def showTweetTextAll(res):
    res_json = json.loads(res.text)
    
    for tweet in res_json:
        print('text : ' + tweet['text'])
        print('id : ' + tweet['id_str'])
        print('in_reply_to_status_id : ' + str(tweet['in_reply_to_status_id_str']))
        print('----------')

# in res
# out show_tweet_text
def getAndShowTweet(twitter, url):
    status_id = getStatusIdByUrl(url)
    while True:
        res = getTweetById(twitter, status_id)
        tweet = json.loads(res.text)
        
        print('text : ' + tweet['text'])
        print('id : ' + tweet['id_str'])
        
        if tweet['in_reply_to_status_id_str'] == None:
            break
        else:
            print('in_reply_to_status_id : ' + tweet['in_reply_to_status_id_str'])
            print('in_reply_to_status_id を使って再検索します')
            status_id = tweet['in_reply_to_status_id_str']
        
        print('----------')
    

