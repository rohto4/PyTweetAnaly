# -*- coding: utf-8 -*-
'''
Created on 2019/04/10

@author: Rohto
'''

from requests_oauthlib import OAuth1Session
from pytz import utc
from tzlocal import get_localzone
from datetime import datetime
from datetime import timedelta
import json
import os, sys, time, calendar

def main(setting_uri='setting/ikioi_setting.json'):
    # 勢い計測実施
    ikioiMaesure()

# 勢い計測のメインクラス
def ikioiMaesure():
    # 設定読み込み
    search_set = readSetting("setting/ikioi_setting.json")
    
    # 検索処理  設定されたキーワード分繰り返す
    key_list = search_set.keys()
    
    for key in key_list:
        # 設定１つに対して勢い検索を実施
        result = ikioiSearch(search_set[key])
    
    # 計算処理
    ikioi = ikioiCalc(result)
    
    # 結果記録
    writeResult(ikioi)
    
    return True

# 設定ファイル読み込み
def readSetting(setting_uri):
    f = open(setting_uri, 'r', encoding='utf-8')
    json_data = json.load(f)
    # 確認用
#     print(json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False))
    return json_data

# 設定１つに対して検索を実施する
def ikioiSearch(set):
    # Twitterのセッションを取得
    twitter = createSession()
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    
    # 初期化
    ikioi_result = {}
    
    # 検索設定
    if set['is_hashtag'] == "True":
        # hashtag
        set['keyword'] = '#' + set['keyword']
    elif set['is_userid'] == "True":
        # userid
        set['keyword'] = '@' + set['keyword']
    
    params = {
        'q':set['keyword'],
        'lang':'ja',
        'result_type':'recent',
        'count':100
        }
    
    '''
    ===================
    =====テスト用======
    ===================
    '''
    # 検索実施
    res = twitter.get(url, params = params)
    res_text = json.loads(res.text)
    writer = open('result/tweet.json', 'w', encoding='utf-8')
    json.dump(res_text, writer, indent=8, ensure_ascii=False)
    
    '''
    ===================
    =====テスト用======
    ===================
    '''
    # 継続判定
    # 取得件数
    count = len(res_text['statuses'])
    
    # 取得結果が時間順に並んでいるか?
    # jsonファイルのデータ順 = OK
    # foreachの出力順 = OK
    # →取得したデータの一番最後の['created_at']で調べればOK
    
    # 取得した最古投稿時間
    last_get_created_at = res_text['statuses'][count-1]['created_at']
    
    # 比較可能な形式に整形
    last_created_at = createdAtToParamStr(last_get_created_at)
    print("created_at : " + last_created_at)
    
    # 現在時刻 (now)
    now_str = dateTimeToParamStr(datetime.now())
    # 対象時刻 (scope)
    scope_date_str = \
        dateTimeToParamStr(datetime.now(), minutes=int(set['scope']), is_plus=False)
    
    print("nowStr     : " + now_str)
    print("scopeStr   : " + scope_date_str)
    
    sys.exit()
    if scope_date_str <= last_created_at:
        # True => 再検索
        do_research = True
    else:    
        # False => 結果を絞る
        do_research = False
    
    
    if do_research == True:
        # 検索範囲が不足している場合、追加で検索
        params['until'] = last_created_at
     
    else:
        # 検索範囲が超過している場合、結果を絞る
        
        # 新しいものから順番に読み込み
        # scope内 => スキップ
        # scope外 => 以降の要素を消去削除(popitem)
        for data in res_text['statuses']:
            print('a')
        
    
    sys.exit()
    
    # 件数カウント
    count = 0

    return ikioi_result

# 勢い計算処理
def ikioiCalc(data={}):
    
    return data

# 結果ファイル書き込み
def writeResult():
    
    return True

# Twitterから取得できる日付の形式から
# 比較可能かつ、params['until']に設定可能な形式に変換する
# created_at → %Y-%m-%d_%H:%M:%S_%Z
def createdAtToParamStr(created_at):
    # 結果時刻 (created_at)
    last_time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    last_unix_time = calendar.timegm(last_time_utc)
    # 日本時間に変換
    last_time_local = time.localtime(last_unix_time)
    
    # unix_time→datetime
    # print(str(datetime.utcfromtimestamp(last_unix_time)))
    
    # 現状
    # time.localtime による変換
    # strftime("%Y-%m-%d_%H:%M:%S_%Z") →2019-04-11_12:28:34_????
    # 理想
    # ja.localizeによる変換
    # strftime("%Y-%m-%d_%H:%M:%S_%Z") →2019-04-11_12:28:34_JST
    datetime_str = time.strftime("%Y-%m-%d_%H:%M:%S_JST", last_time_local)
    
    return datetime_str

# datetime型の日付形式を
# 比較可能かつ、params['until']に設定可能な形式に変換する
# 
def dateTimeToParamStr(datetime, minutes=0, is_plus=False):
    # タイムゾーンの設定
    ja = get_localzone()
    
    # 日本時刻に変換
    aware_time = ja.localize(datetime)
    
    # 時間を増減させる
    if minutes != 0:
        if is_plus == True:
            aware_time = aware_time + timedelta(minutes=minutes)
        else:
            aware_time = aware_time - timedelta(minutes=minutes)
    
    # 整形
    datetime_str = aware_time.strftime("%Y-%m-%d_%H:%M:%S_%Z")
    
    return datetime_str

# twitterセッション取得
def createSession():
    session = OAuth1Session(os.environ['CONSUMER_KEY'],os.environ['CONSUMER_SECRET'],\
                            os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    return session

# 引数がなければmainメソッドを実行
if __name__=='__main__':
    main()