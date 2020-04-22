# -*- coding: utf-8 -*-
'''
Created on 2019/04/10

@author: Rohto
'''

from requests_oauthlib import OAuth1Session
from tzlocal import get_localzone
from datetime import datetime
from datetime import timedelta
import json
import os, time, calendar

def main():
    # 勢い計測実施
    ikioiMaesure()

# 勢い計測のメインクラス
def ikioiMaesure(setting_uri='setting/ikioi_setting.json'):
    # 設定読み込み
    search_set = readSetting(setting_uri)
    '''
    初期化
    '''
    # 検索キーワード
    key_list = search_set.keys()
    # 結果用辞書
    ikioi_result = {}
    key_time = getTimestamp()
    for key in key_list:
        search_word = search_set[key]['keyword']
        ikioi_result[search_word] = {key_time:{}}
    # 結果
    result_set = []
        
    print(json.dumps(ikioi_result, sort_keys=True, indent=4, ensure_ascii=False))
    
    # 検索処理  設定されたキーワード分繰り返す
    for key in key_list:
        # 設定１つに対して勢い検索を実施
        search_set[key]['keytime'] = key_time
        search_setting = search_set[key]
        search_word = search_set[key]['keyword']
        
        result = ikioiSearch(search_setting)
        # 計算処理
        # 辞書形式で格納
        ikioi_result[search_word][key_time] = ikioiCalc(search_setting, result)
        # 結果記録
#         print(json.dumps(ikioi_result, sort_keys=True, indent=4, ensure_ascii=False))
        result_set.append(writeResult(search_setting, ikioi_result[search_word]))
    
    return result_set

# 設定ファイル読み込み
def readSetting(setting_uri):
    f = open(setting_uri, 'r', encoding='utf-8')
    json_data = json.load(f)
    # 確認用
#     print(json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False))
    return json_data

# 設定１つに対して検索を実施する
def ikioiSearch(search_set):
    # Twitterのセッションを取得
    twitter = createSession()
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    
    # 検索設定
    if search_set['is_hashtag'] == "True":
        search_set['keyword'] = '#' + search_set['keyword']
    elif search_set['is_userid'] == "True":
        search_set['keyword'] = '@' + search_set['keyword']
    
    params = {
        'q':search_set['keyword'],
        'lang':'ja',
        'result_type':'recent',
        'count':100
        }
    
    '''
    取得部
    '''
    # 取得したツイートの最古投稿時間
    old_created_at = True
    # 対象時刻
    scope_date = True
    # 取得したツイートの一時データ
    tmp_result = {'created_at':[], 'text':[]}
    # 取得したツイートの合計件数
    total_count = 0
    
    print('----検索開始')
    while True:
        # 検索実施
        print(params)
        res = twitter.get(url, params = params)
        res_text = json.loads(res.text)
        if res.headers['X-Rate-Limit-Remaining'] is not None:
            print ('アクセス可能回数 %s' % res.headers['X-Rate-Limit-Remaining'])
            print ('リセット時間 %s' % res.headers['X-Rate-Limit-Reset'])
        else:
            print('ヘッダが正常に取得できませんでした')
        
        # 結果を結果リストに追加
        for tweet_data in res_text['statuses']:
            tmp_result['created_at'].append(tweet_data['created_at'])
            tmp_result['text'].append(tweet_data['text'])

        # 一時データの末尾インデックスを設定      
        total_count = len(tmp_result['created_at'])
        
        # 最古投稿時間を設定
        old_created_at = tmp_result['created_at'][total_count-1]
        # 比較可能な形式に整形
        old_created_at_param = createdAtToParamStr(old_created_at)
        # 現在時刻 (now)
        now_date = dateTimeToParamStr(datetime.now())
        # 対象時刻 (scope)
        scope_date = dateTimeToParamStr(datetime.now(), minutes=int(search_set['scope']))
        
        # 判定出力
        print("取得件数   : " + str(total_count) + "件")
        print("created_at : " + old_created_at_param)
        print("now_date     : " + now_date)
        print("scope_date   : " + scope_date)
        
        # 再検索判定
        print('----再検索判定')
        if old_created_at_param > scope_date:
            # 再検索用パラメータを設定
            params['until'] = old_created_at_param
            
        else:
            print('----検索終了')
            break

    '''
    カウント部
    '''
    # 結果を絞る
    print('----結果絞り込み')
    # 計測対象の件数
    ikioi_target_count = 0
    # 新しいものから順番に読み込み
    # scope内 => スキップ
    # scope外 => 対象数を増加
    # 
    for data in tmp_result['created_at']:
        created_at_str = createdAtToParamStr(data)
        
        if scope_date > created_at_str:
            # 以降を対象にしない
            break
        # 計測対象の件数
        ikioi_target_count += 1
    
    return ikioi_target_count

# 勢い計算処理
def ikioiCalc(search_setting, count):
    ikioi = (1440 / int(search_setting['scope'])) * count
    ikioi_result = {
        'scope':search_setting['scope'],
        'count':str(count),
        'ikioi':str(ikioi),
        }
    print(ikioi_result)
    return ikioi_result

# 結果をファイルの末尾に追加
def writeResult(search_setting, report):
    path = 'result/ikioi_report.json'
    
    print('----結果書き込み')
    # 読み込み用
    fr = open(path, 'r', encoding='utf-8')
    report_r = json.load(fr)
    # エラー発生中 TODO
    # 初回キーワード検索時に、keyが見つからない旨
    report_r[search_setting['keyword']][search_setting['keytime']] = report[search_setting['keytime']]
    
    # 書き込み用
#     print(json.dumps(report_r, sort_keys=True, indent=4, ensure_ascii=False))
    report_w = open(path, 'w', encoding='utf-8')
    result = json.dump(report_r, report_w, sort_keys=True, indent=4, ensure_ascii=False)
        
    return result

# Twitterから取得できる日付の形式から
# 比較可能で、params['until']に設定可能な形式に変換する
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
# 比較可能で、params['until']に設定可能な形式に変換する
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

# レポートキーに使用するタイムスタンプを取得する
def getTimestamp():
    now = datetime.now()
    fmt = '%Y/%m/%d_%H:%M:%S'
    key_timestamp = now.strftime(fmt)
    return key_timestamp

# twitterセッション取得
def createSession():
    session = OAuth1Session(os.environ['CONSUMER_KEY'],os.environ['CONSUMER_SECRET'],\
                            os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    return session

# 引数がなければmainメソッドを実行
if __name__=='__main__':
    main()