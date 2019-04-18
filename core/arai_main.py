'''
Created on 2019/04/17

@author: Rohto
'''
from requests_oauthlib import OAuth1Session
from datetime import datetime
from dateutil.create_str import dateTimeToParamStr #@UnresolvedImport
import os

def main():
    
    now_str = dateTimeToParamStr(datetime.now())
    print(now_str)
#     getAraiList()

def getAraiList():
    print("アライさんだらけなのだ")
    
    '''
    検索初期設定
    '''
    # 取得したい期間
    s_period = dateTimeToParamStr(datetime.now(), 60)
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
    
# アクセス制限を確認
# 引っかかれば解除までsleep
def checkLimit():
    return True
    
# result.user.nameにs_usernameが含まれているか確認
def checkInTheName():
    return True

# アライさんリストにユーザ情報を追加
# ユーザ名 / ユーザ表示ID / 自己紹介 / フォロー数 / フォロワー数
# フォロワー比率 / @ツイート比率 / 勢い
def addAraiList():
    print("アライさんリストに情報を保存")
    

# フォロワー比率計算


# @ツイート比率計算


# 勢い計算


# 設定読み込み
# 検索ワード="アライさん"固定
# 実行日時(いつ実行したか)
# 最終取得日時(どこまで遡ったか)
def readSetting():
    return True

# 結果書き込み
def writeAraiList():
    print("結果をexcelか何かに書き込む")


# 



# twitterセッション取得
def createSession():
    session = OAuth1Session(os.environ['CONSUMER_KEY'],os.environ['CONSUMER_SECRET'],\
                            os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    return session

if __name__ == '__main__':
    main()