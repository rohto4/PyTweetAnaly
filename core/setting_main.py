'''
Created on 2019/04/12

@author: Rohto
'''
import json
import sys

path = 'setting/ikioi_setting.json'

def main():
    # 起動画面
    addSet()

def test():
    fr = open(path, 'r', encoding='utf-8')
    setting_list = json.load(fr)
    
    print(setting_list.keys())
    
# 追加
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
    
    if is_add  in('Y','y'):
        # 追加
        fr = open(path, 'r', encoding='utf-8')
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
        writer = open(path, 'w', encoding='utf-8')
        
        # sort_keys=Trueでエラー落ちするため非ソート
        json.dump(setting_list, writer, indent=4, ensure_ascii=False)
        
        print("設定を追加しました")
    else:
        print("中止しました")

# 更新
def updateSet():
    print('キーワード')

# 設定
def showList():
    fr = open(path, 'r', encoding='utf-8')
    setting_list = json.load(fr)
    print("設定表示")
    
    key_list = setting_list.keys()
    
    for key in key_list:
        keyword = setting_list[key]['keyword']
        scope = setting_list[key]['scope']
        ishash = setting_list[key]['is_hashtag']
        isuser = setting_list[key]['is_userid']
        print("■" + keyword +  " : scope[" + scope + '] #=' + ishash + " @=" + isuser)

if __name__ == '__main__':
    main()