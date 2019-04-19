# -*- coding: utf-8 -*-
'''
Created on 2019/04/18

@author: Rohto
'''
from requests_oauthlib import OAuth1Session
import os, json, datetime, time

# twitterセッション取得
def createTwitterSession():
    session = OAuth1Session(os.environ['CONSUMER_KEY'],os.environ['CONSUMER_SECRET'],\
                            os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    return session

# 回数制限を問合せ、アクセス可能になるまで wait する
def checkLimit(self):
    unavailableCnt = 0
    while True:
        url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
        res = self.session.get(url)
        
        if res.status_code == 503:
            # 503 : Service Unavailable
            if unavailableCnt > 10:
                raise Exception('Twitter API error %d' % res.status_code)
            
            unavailableCnt += 1
            print ('Service Unavailable 503')
            self.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
            continue
        
        unavailableCnt = 0
        
        if res.status_code != 200:
            raise Exception('Twitter API error %d' % res.status_code)
        
        remaining, reset = self.getLimitContext(json.loads(res.text))
        if (remaining == 0):
            self.waitUntilReset(reset)
        else:
            break

# 最古取得日付を設定する
# 引数はres_text['statuses']を受け取る
def setOldDate(tweet_list):
    length = len(tweet_list)
    last_created_at = tweet_list[length-1]['created_at']
    return last_created_at

# tmp_tweet_list から tmp_user_infoに設定する
# 一人分
def setToUserInfo(info):
    # tmp_user_info = info[各種情報]
    # 無加工データ
    tmp_user_info = {}
    tmp_user_info['id'] = info['id']
    tmp_user_info['name'] = info['name']
    tmp_user_info['screen_name'] = info['screen_name']
    tmp_user_info['friends_count'] = info['friends_count']
    tmp_user_info['followers_count'] = info['followers_count']
    tmp_user_info['statuses_count'] = info['statuses_count']
    tmp_user_info['favourites_count'] = info['favourites_count']
    tmp_user_info['created_at'] = info['created_at']
    tmp_user_info['profile_image_url']= info['profile_image_url']
    tmp_user_info['description'] = info['description']
    # 加工データ
    # フォロー数 / フォロワー数(値が大きい程一方的なフォローが多い)
    tmp_user_info['followers_rate'] = info['friends_count'] / info['followers_count']
    # いいね数 / Tweet数（値が大きい程いいね数が多い）
    tmp_user_info['favorites_rate'] = info['favourites_count'] /info['statuses_count']

    return tmp_user_info




