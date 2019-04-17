'''
Created on 2019/04/12

@author: Rohto
'''
from datetime import datetime
from tzlocal import get_localzone
import json
import sys

SETTING_PATH = 'setting/ikioi_setting.json'
DIR = 'setting/'
FILENAME= 'ikioi_setting.json'

def main():
    # 起動画面
    while True:
        print('--------------------')
        print('1.add set')
        print('2.update set(未実装)')
        print('3.show list')
        print('4.remove set')
        print('5.backup')
        print('999.clear(未実装)')
        print('0.exit')
        print('--------------------')
        print('select operation number >> ')
        
        try:
            num = input()
            in_num_int = int(num)
            
        except ValueError : 
            print('半角数字で入力してください')
            continue
        
        if in_num_int == 1:
            addSet()
        elif in_num_int == 2:
            updateSet()
        elif in_num_int == 3:
            showList()
        elif in_num_int == 4:
            removeSet()
        elif in_num_int == 5:
            backup()
        elif in_num_int == 999:
            clear()
        elif in_num_int == 0:
            doExit()

def test():
    fr = open(SETTING_PATH, 'r', encoding='utf-8')
    setting_list = json.load(fr)
    
    print(setting_list.keys())
    
# 追加
# 実装済み
# エラーテスト未実施
def addSet():
    while True:
        print("キーワード (str)")
        in_keyword = input()
        print(type(in_keyword))
        if type(in_keyword) is str:
            break
    
    while True:
        print("scope (int)")
        
        try:
            in_scope = input()
            in_scope_int = int(in_scope)
            
        except ValueError : 
            print('ValueError')
            continue
        
        if type(in_scope_int) is int:
            break
    
    while True:
        print("hashtag? (Y/N)")
        in_hash = input()
        if in_hash in('Y','N','y','n'):
            # 保存形式に合わせる
            if in_hash in('Y','y'):
                in_hash = 'True'
            elif in_hash in('N','n'):
                in_hash = 'False'
            break
    
    while True:
        print("userid? (Y/N)")
        in_user = input()
        if in_user in('Y','N','y','n'):
            # 保存形式に合わせる
            if in_user in('Y','y'):
                in_user = 'True'
            elif in_user in('N','n'):
                in_user = 'False'
            break
    
    print("■" + in_keyword + " : scope[" + in_scope + "] #=" + in_hash + " @="+ in_user)
    print("以上の内容で設定を追加しますか? (Y/N)")

    is_add = input()
    
    if is_add in('Y','y'):
        # 追加
        fr = open(SETTING_PATH, 'r', encoding='utf-8')
        setting_list = json.load(fr)
        index_list = setting_list.keys()
        
        # 設定の末尾のインデックスを取得
        last_index = 1 + int(max(index_list))
        
        setting_list[last_index] = {
            'keyword':in_keyword,
            'scope':str(in_scope),
            'is_hashtag':str(in_hash),
            'is_userid':str(in_user)
            }
        print(setting_list)
        writer = open(SETTING_PATH, 'w', encoding='utf-8')
        
        # sort_keys=Trueでエラー落ちするため非ソート
        json.dump(setting_list, writer, indent=4, ensure_ascii=False)
        
        print("設定を追加しました")
    else:
        print("中止しました")

# 更新
# 未実装
# エラーテスト未実施
def updateSet():
    print('未実装')

# 設定
# 実装済み
def showList():
    fr = open(SETTING_PATH, 'r', encoding='utf-8')
    setting_list = json.load(fr)
    print("設定表示")
    
    key_list = setting_list.keys()
    
    for key in key_list:
        keyword = setting_list[key]['keyword']
        scope = setting_list[key]['scope']
        ishash = setting_list[key]['is_hashtag']
        isuser = setting_list[key]['is_userid']
        print("■" + str(key) + "." + keyword +  " : scope[" + scope + '] #=' + ishash + " @=" + isuser)

# 削除
# 未実装
# エラーテスト未実施
def removeSet():
    print('--------------------')
    showList()
    print('--------------------')
    
    # 入力受付
    while True:
        print("削除する設定Noを入力してください。")
    
        try:
            in_index = input()
            in_index_int = int(in_index)
            
        except ValueError : 
            print('ValueError')
            continue
        
        if type(in_index_int) is int:
            break
    
    # インデックスチェック
    f = open(SETTING_PATH, 'r', encoding='utf-8')
    json_data = json.load(f)
    index_str = str(in_index)
    
    if in_index in json_data.keys():
        # 存在する場合
        # 削除確認
        print(json_data[index_str])
        keyword = json_data[in_index]['keyword']
        scope = json_data[in_index]['scope']
        ishash = json_data[in_index]['is_hashtag']
        isuser = json_data[in_index]['is_userid']
        
        print("この設定を削除します")
        print("■" + in_index + "." + keyword +  " : scope[" + scope + '] #=' + ishash + " @=" + isuser)
        print("よろしいですか? (Y/N)")
        is_add = input()
        
        # 削除実施
        if is_add in('Y','y'):
            # 辞書から削除
            del json_data[in_index]
            
            # 書き込み
            with open(SETTING_PATH, 'w', encoding='utf-8') as fw:
                json.dump(json_data, fw, ensure_ascii=False, indent=4)

            print("削除しました") 
        else:
            print("中止しました")
    else:
        print("存在しないインデックス")
    
# バックアップ
# 実装済み
# エラーテスト未実施
def backup():
    # ネーミング
    ja = get_localzone()
    now = ja.localize(datetime.now())
    now_str = now.strftime("%Y%m%d%H%M%S_")
    save_filename = now_str + FILENAME
    
    # 既存設定オープン
    setting_uri = DIR + FILENAME
    fr = open(setting_uri, 'r', encoding='utf-8')
    setting_data = json.load(fr)
    
    # 複製
    with open(DIR + save_filename, 'w', encoding='utf-8') as fw:
        json.dump(setting_data, fw, ensure_ascii=False, indent=4)
    
    print("現在の設定内容をバックアップしました。")
    print("ファイル名 : " + save_filename)
    
# 全削除
# 未実装
# エラーテスト未実施
def clear():
    print("未実装")

# 終了
def doExit():
    print("終了します")
    sys.exit()

if __name__ == '__main__':
    main()