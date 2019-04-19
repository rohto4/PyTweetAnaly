# -*- coding: utf-8 -*-
'''
Created on 2019/04/17

@author: Rohto
'''

from datetime import datetime
from util.date_util import dateTimeToParam #@UnresolvedImport
from util.twitter_util import createTwitterSession, checkLimit, setOldDate, setToUserInfo #@UnresolvedImport
from util.json_util import readCommonSetting, writeBreakStatus, writeJsonData #@UnresolvedImport
import os
import json

def main():
    
    getAraiList()

def getAraiList():
    '''
    初期化
    '''
    # 結果用
    user_info = {}              # ユーザ詳細リスト。最終的な成果物。
    write_break_status = {}     # 中断時の状態を保存
    # 一時結果用
    user_list = []              # 成果物に追加したユーザリスト。ユーザ詳細リストのkeyと一致
    tmp_tweet_list = {}         # 1アクセスで取得したツイートデータ
    tmp_user_info = {}          # 1アクセスで追加したユーザリストの詳細データ
    read_break_status = ""      # 中断した日付データ

    # 共通設定
    twitter = createTwitterSession()
    
    
    # 限定設定
    '''
    検索初期設定
    '''
    # 取得したい期間
    s_period = dateTimeToParam(datetime.now(), 60)
    # 検索ワード
    s_keyword = 'アライさん'
    # ユーザー名
    s_username = 'アライさん'
    # 必須パラメータ
    params = {
        'q':s_keyword,
        'lang':'ja',
        'result_type':'recent',
        'count':100
        }
    
    # loop開始
    # 期間中のarai_listの作成完了まで
    while True:
        
        # アクセス制限を確認
        checkLimit()
        # 検索実施
        
        # 
        for i in range(100):
            # アライさんが名前に含まれていることをチェック
            username = ""
            is_contain = checkInTheName(username, s_username) # 既存メソッドでよさそう
            
            # Trueならユーザーリストに追加
            if is_contain == True:
                # 
                addAraiList()
            
            # 
        
        # 継続判定
        # scopedate, lastdate
        
        
        # 追加パラメータ設定
        params['until'] = "xxxx/xx/xx_xx:xx:xx_JST"
    # 
    #
    #
    #

if __name__ == '__main__':
    main()


