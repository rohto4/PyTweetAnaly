'''
Created on 2019/04/12

@author: Rohto
'''

import json
'''
キーワード毎に最新データを表示
'''
def main():
    path = 'result/ikioi_report.json'
    
    fr = open(path, 'r', encoding='utf-8')
    report_r = json.load(fr)
    
    # キーワード分ループ
    for key in report_r.keys():
        # レポート日付を取得
        date_list = report_r[key].keys()
        new_date = ""
        
        # 新しい日付を取得
        for date in date_list:
            if new_date == ""  or new_date < date:
                new_date = date
        
        # 表示
        keyword = report_r[key]
        scope = report_r[key][new_date]['scope']
        ikioi = report_r[key][new_date]['ikioi']
        count = report_r[key][new_date]['count']
        
        print("==========")
        print("■"+ key + " [" + new_date + "]")
        print("[ " + scope + " ]分間に[ " + count + " ]のTweet  勢い [ " + ikioi + " ]")

if __name__ == '__main__':
    main()