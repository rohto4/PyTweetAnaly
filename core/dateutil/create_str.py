'''
Created on 2019/04/17

@author: Rohto
'''
from tzlocal import get_localzone
from datetime import timedelta


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
