# -*- coding: utf-8 -*-
'''
Created on 2019/04/18

@author: Rohto
'''
from tzlocal import get_localzone
from datetime import timedelta
import time, calendar

# 形式変換
# created_at → params_until
def createdAtToParam(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    # UNIX形式に変換
    unix_time = calendar.timegm(time_utc)
    # 日本時間に変換
    time_local = time.localtime(unix_time)
    # 整形
    params_until = time.strftime("%Y-%m-%d_%H:%M:%S_JST", time_local)
    return params_until

# 形式変換
# datetime型 → params_until
def dateTimeToParam(datetime):
    # タイムゾーンの設定
    ja = get_localzone()
    # 日本時間に変換
    aware_time = ja.localize(datetime)
    # 整形
    params_until = aware_time.strftime("%Y-%m-%d_%H:%M:%S_%Z")
    return params_until

# 形式変換
# datetime型 → params_until
# 時間増減付き
def dateTimeToParamOption(datetime, minutes=0, is_plus=False):
    # タイムゾーンの設定
    ja = get_localzone()
    # 日本時刻に変換
    aware_time = ja.localize(datetime)
    # 時間増減
    if minutes != 0:
        if is_plus == True:
            aware_time = aware_time + timedelta(minutes=minutes)
        else:
            aware_time = aware_time - timedelta(minutes=minutes)
    # 整形
    params_until = aware_time.strftime("%Y-%m-%d_%H:%M:%S_%Z")
    return params_until
    
    
    
    