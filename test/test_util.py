'''
Created on 2019/04/19

@author: Rohto
'''

import json

def main():
    test2()
    
def test1():
    # open×2
    uri1 = 'test1.json'
    uri2 = 'test2.json'
    
    f1 = open(uri1, 'r', encoding='utf-8')
    json_data1 = json.load(f1)
    f2 = open(uri2, 'r', encoding='utf-8')
    json_data2 = json.load(f2)
    
    json_data3 = {**json_data1, **json_data2}
    
    print(json.dumps(json_data3, sort_keys=True, indent=4, ensure_ascii=False))
    
def test2():
    # open + 辞書
    uri1 = 'test1.json'
    
    f1 = open(uri1, 'r', encoding='utf-8')
    json_data1 = json.load(f1)
    f2 = {
        '4':{
            "keyword": "内田彩",
            "scope": "720",
            "is_hashtag": "False",
            "is_userid": "False"
        },
        '5':{
            "keyword": "テトリス",
            "scope": "360",
            "is_hashtag": "False",
            "is_userid": "False"
        },
    }
    
    json_data3 = {**json_data1, **f2}
    
    print(json.dumps(json_data3, sort_keys=True, indent=4, ensure_ascii=False))
    
    print('')
    
if __name__=='__main__':
    main()