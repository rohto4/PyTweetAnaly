# -*- coding: utf-8 -*-
'''
Created on 2019/04/17

@author: Rohto
'''

from util.date_util import createdAtToParam #@UnresolvedImport
from util.twitter_util import createTwitterSession, checkLimit, showLimit,getOldDate, setToUserInfo #@UnresolvedImport
from util.json_util import readJsonData, writeBreakStatus, writeJsonData, addJsonData #@UnresolvedImport
import os
import json

def main():
    
    getAraiList()

def getAraiList():
    '''
    --------------------
    初期化
    --------------------
    '''
    # パス
    _DATA_DIR = 'result/'
    _SETTING_DIR = 'setting/'
    _COMMON_SETTING_FILENAME = 'common_setting.json'
    _BREAK_STATUS_FILENAME = 'break_status.json'
    _RESULT_FILENAME = 'user_list.json'
    _SEARCH_TWEETS_URL = 'https://api.twitter.com/1.1/search/tweets.json'
    
    # 結果用
    user_info = {}              # ユーザ詳細リスト。最終的な成果物。
    # 一時結果用
    user_list = []              # 成果物に追加したユーザリスト。ユーザ詳細リストのkeyと一致
    next_index = 0              # 辞書のインデックス (len(user_list)と一致)
    tmp_tweet_data = {}         # 1アクセスで取得したツイートデータ
    break_status = ""           # 中断した日付データ
    last_date_params = ""       # 最古取得日付データ

    # 共通設定
    twitter = createTwitterSession()            # Twitterセッション
    common_setting = readJsonData(_SETTING_DIR+_COMMON_SETTING_FILENAME)   # 検索設定を読み込む
    period_params = common_setting['period']    # 上限取得期間
    search_word = common_setting['keyword']     # 検索する名前
    params = {                                  # 検索条件
        'q':search_word,
        'lang':'ja',
        'result_type':'recent',
        'count':100
        }
    
    # 限定設定
    # 中断情報の確認
    is_break_status = os.path.isfile(_DATA_DIR+_RESULT_FILENAME)
    # ある場合untilを設定
    if is_break_status:
        break_status = readJsonData(_SETTING_DIR+_BREAK_STATUS_FILENAME)   # 中断情報を読み込む
        until_params = break_status['last_get_date']
        params['until'] = until_params          # 検索追加条件
        next_index = break_status['next_index'] # ユーザ辞書のインデックス
    
    '''
    --------------------
    取得
    --------------------
    '''
    # -----loop-----
    while True:
        
        # アクセス制限を確認
        checkLimit(twitter)
        
        # 100件取得
        res = twitter.get(_SEARCH_TWEETS_URL, params=params)
        # アクセス情報を表示
        showLimit(res)
        # statusesを取り出す
        tmp_tweet_data = json.loads(res.text)
        print(str(len(tmp_tweet_data['statuses'])) + "件取得")
        
        for tweet_data in tmp_tweet_data['statuses']:
            # 名前に指定ワードが含まれていることをチェック
            if tweet_data['user']['name'].find(search_word) == -1:
                # 含まれないため次へ
                continue
            
            # 既に登録されたユーザでないことをチェック
            if tweet_data['user']['id'] in user_list:
                # 既存ユーザのため次へ
                continue
            '''
            --------------------
            一時登録
            --------------------
            '''
            # ユーザリストに追加
            user_list.append(tweet_data['user']['id'])
            # ユーザ詳細情報を追加
            user_info = setToUserInfo(user_info, tweet_data['user'], next_index)
            # インデックスを進める
            next_index += 1
            
        '''
        --------------------
        継続判定
        --------------------
        '''
        # 取得済みの最古日時
        last_date = getOldDate(tmp_tweet_data)
        last_date_params = createdAtToParam(last_date)
        
        print("対象期間 : " + period_params + " まで")
        print("今       : " + last_date_params + " までおわったよ")
        
        # 取得対象期間を超えていれば終了処理へ
        if last_date_params < period_params:
            break
        
        # 追加パラメータ設定
        params['until'] = last_date_params
    
    '''
    --------------------
    本登録(書き込み)
    --------------------
    ''' 
    if break_status == "":
        # 過去に中断していた場合
        writeBreakStatus(last_date_params, next_index, False)                        # 中断情報
        writeJsonData(_DATA_DIR+_RESULT_FILENAME, user_info)                                        # 書き込み
    else:
        # 初めての中断の場合
        writeBreakStatus(last_date_params, next_index, True)                       # 中断情報
        user_info = addJsonData(_DATA_DIR+_RESULT_FILENAME, user_info)  # 既存のユーザ情報と連結
        writeJsonData(_DATA_DIR+_RESULT_FILENAME, user_info)                                        # 書き込み
        
if __name__ == '__main__':
    main()


