# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
from pytz import utc
from tzlocal import get_localzone
from datetime import datetime
from datetime import timedelta
import json
import sys, time, calendar

CK = 'o46La2iGb7bIn41XyXqHyYw8A'                             # Consumer Key
CS = 'eTeaiw1nJ71KNgH2AwU6cQkgbByk6ZLfi58FEel6ENrsNAm5gR'    # Consumer Secret
AT = '773885677507321856-bypmqmScqUcCPAuEQRuhRDllEqtXXeT'    # Access Token
AS = 'pGq6OYipTDRzRtv8QXI0cdCZ2yWkXIYNLvv91fh8Cob61'         # Accesss Token Secert

session = OAuth1Session(CK, CS, AT, AS)

# 検索用URL設定
url = 'https://api.twitter.com/1.1/search/tweets.json'

# タイムゾーンの設定
ja = get_localzone()

# 現時刻にタイムゾーンを設定
# 現時刻、対象時刻をTweet検索用フォーマットに変換
# 下記参照
# https://qiita.com/areph/items/0745cb744a12810334c6
naiveNow = datetime.now()
awareNow = ja.localize(naiveNow)
nowStr = awareNow.strftime("%Y-%m-%d_%H:%M:%S_%Z")

awareUntil = awareNow - timedelta(minutes=1440)
untilStr = awareUntil.strftime("%Y-%m-%d_%H:%M:%S_%Z")

# 検索パラメータ
search_word = u'#東山奈央'
params = {
    'q':search_word,
    'until':untilStr,
}

print("時刻 : " + nowStr + " ～ " + untilStr + " を検索します。")
res = session.get(url, params = params)

#--------------------
# ステータスコード確認
#--------------------
if res.status_code != 200:
    print ("Twitter API Error: %d" % res.status_code)
    sys.exit(1)

#--------------
# ヘッダー部
#--------------
print ('アクセス可能回数 %s' % res.headers['X-Rate-Limit-Remaining'])
print ('リセット時間 %s' % res.headers['X-Rate-Limit-Reset'])
# sec = int(res.headers['X-Rate-Limit-Reset'])\
#            - time.mktime(datetime.datetime.now().timetuple())
# print ('リセット時間 （残り秒数に換算） %s' % sec)

#--------------
# テキスト部
#--------------
res_count = 0
min_create_at = ""
min_japan_time = datetime.now()
max_create_at = ""
max_japan_time = datetime.now()

res_text = json.loads(res.text)

for tweet in res_text['statuses']:
#     print('-----')
    # 
    # created_at : Tue Apr 09 01:40:42 +0000 2019
    # struct_time :  time.struct_time(tm_year=2019, tm_mon=4, tm_mday=9, tm_hour=1, tm_min=40, tm_sec=42, tm_wday=1, tm_yday=99, tm_isdst=-1)
    # unix_time : 1554774042
    # time_local : time.struct_time(tm_year=2019, tm_mon=4, tm_mday=9, tm_hour=10, tm_min=40, tm_sec=42, tm_wday=1, tm_yday=99, tm_isdst=0)
    # japan_time : 2019-04-09 10:40:42
    print("created_at" +  tweet['created_at'])
    time_utc = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
#     print("japan_time" + japan_time)
    
    if (res_count == 0):
        min_create_at = tweet['created_at']
        min_japan_time = japan_time
    else:
        max_create_at = tweet['created_at']
        max_japan_time = japan_time
#     print (tweet['text'])
    res_count += 1


print("==============================")
print("created_at : " + min_create_at + " ～ " + max_create_at)
print("japan_time : " + min_japan_time + " ～ " + max_japan_time)
# print("時刻 : " + str(untilStr) + " ～ " + str(nowStr) + " の検索が完了しました。")
print("[ " + search_word + " ]を含むTweetが[ " + str(res_count) + " ]件見つかりました。")
