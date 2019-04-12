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
    
    # 初期化
    # 検索キーワード
    key_list = search_set.keys()
    # 結果辞書
    ikioi_result = {}
    for key in key_list:
        ikioi_result[search_set[key]['keyword']] = {}

    # 検索処理  設定されたキーワード分繰り返す
    for key in key_list:
        # 設定１つに対して勢い検索を実施
        result = ikioiSearch(search_set[key])
    
        # 計算処理
        # 辞書形式で格納
        ikioi_result[key] = ikioiCalc(search_set[key], result)
    
    # 結果記録
    result = writeResult(ikioi_result)
    
    return result

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
    ikioi_target_count = 0
    
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
    
    # 検索実施
    print('----検索')
    res = twitter.get(url, params = params)
    print ('アクセス可能回数 %s' % res.headers['X-Rate-Limit-Remaining'])
    print ('リセット時間 %s' % res.headers['X-Rate-Limit-Reset'])
    
    res_text = json.loads(res.text)
#     writer = open('result/tweet.json', 'w', encoding='utf-8')
#     json.dump(res_text, writer, indent=8, ensure_ascii=False)
    
    # 再検索判定
    print('----再検索判定')
    # 取得件数
    count = len(res_text['statuses'])
    # 取得した最古投稿時間
    last_get_created_at = res_text['statuses'][count-1]['created_at']
    # 比較可能な形式に整形
    last_created_at = createdAtToParamStr(last_get_created_at)
    # 現在時刻 (now)
    now_str = dateTimeToParamStr(datetime.now())
    # 対象時刻 (scope)
    scope_date_str = \
        dateTimeToParamStr(datetime.now(), minutes=int(set['scope']), is_plus=False)
    
    print("取得件数   : " + str(count) + "件")
    print("created_at : " + last_created_at)
    print("nowStr     : " + now_str)
    print("scopeStr   : " + scope_date_str)
    
    if scope_date_str <= last_created_at:
        # True => 再検索
        do_research = True
    else:    
        # False => 結果を絞る
        do_research = False
    
    
    if do_research == True:
        # 検索範囲が不足している場合、追加で検索
        print('----再検索実施')
        params['until'] = last_created_at
        # TODO scopeを広げてテスト
        print(params)
        sys.exit()
     
    else:
        # 検索範囲が超過している場合、結果を絞る
        print('----結果絞り込み')
        # 新しいものから順番に読み込み
        # scope内 => スキップ
        # scope外 => 対象数を増加
        # 
        for data in res_text['statuses']:
            created_at_str = createdAtToParamStr(data['created_at'])
            
            if scope_date_str > created_at_str:
                # 以降を対象にしない
                break
            # 計測の対象件数
            ikioi_target_count += 1
    
    return ikioi_target_count

# 勢い計算処理
def ikioiCalc(set, count):
    record_date = str(datetime.now())
    ikioi = (1440 / int(set['scope'])) * count
    ikioi_result = {
        'report_date':record_date,
        'keyword':set['keyword'],
        'scope':set['scope'],
        'count':count,
        'ikioi':ikioi,
        }
    print(ikioi_result)
    return ikioi_result

# 結果をファイルの末尾に追加
def writeResult(report_list):
    path = 'result/ikioi_report.json'
    
    
    # TODO 
    # 読み込み用
    fr = open(path, 'r', encoding='utf-8')
    report_r = json.load(fr)
    
    # 書き込み用
    report_w = open(path, 'w', encoding='utf-8')
    
    # レポート件数
    report_count = len(report_r)
    
    for report in report_list:
        report_r.setdefault(report_count, report)
        report_count += 1
        print(report_r)
        
#     json.dump(report_r, report_w, indent=8, ensure_ascii=False)
    
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