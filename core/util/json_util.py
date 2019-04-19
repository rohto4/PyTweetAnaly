# -*- coding: utf-8 -*-
'''
Created on 2019/04/18

@author: Rohto
'''
from datetime import datetime
import json
import os

# 設定ファイル読み込み
def readCommonSetting(setting_uri):
    f = open(setting_uri, 'r', encoding='utf-8')
    json_data = json.load(f)
    return json_data

# 中断状況をbreak_status.jsonとして保存
# break_statusファイルが既にあればバックアップ
# last_get_date_param    : 中断時点の最古記録日付
# old_break_status : 前回の中断記録
def writeBreakStatus(last_get_date_param, old_break_status=False):
    break_status_dir = '../setting/'
    break_status_filename = 'break_status.json'
    break_status_path = break_status_dir + break_status_filename
    break_status = {}
    
    # 既存ファイルチェック
    if os.path.isfile(break_status_path):
        # バックアップ
        datetime_str = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_filename = datetime_str + '_' + break_status_filename
        backup_data = readCommonSetting(break_status_path)
        
        bkfw = open(backup_filename, 'w', encoding='utf-8')
        json.dump(backup_data, bkfw, indent=4, ensure_ascii=False)
    
    break_status['last_get_date'] = last_get_date_param
    fw = open(break_status_path, 'w', encoding='utf-8')
    json.dump(break_status, fw, indent=4, ensure_ascii=False)

# 汎用メソッド
# ユーザ情報を書き込む
def writeJsonData(json_data, path):
    fw = open(path, 'w', encoding='utf-8')
    json.dump(json_data, fw, sort_keys=True, indent=4, ensure_ascii=False)

# 取得済みのユーザ情報があった場合、こちらを呼び出す
# 取得済みのユーザ情報に追記する
# TODO 未実装
def addJsonData(json_data, path, key_list):
    return None