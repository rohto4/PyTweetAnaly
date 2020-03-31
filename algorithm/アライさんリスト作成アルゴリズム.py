■アライさん検索アルゴリズム


'''
初期化
'''
# 結果
user_info => json保存				# 最終的な成果物
write_break_status => json保存		# 中断時の状態を保存。untilを設定して再開可能にする。
# 一時結果
user_list 			# 重複チェックのために保持するユーザリスト (user_infoのkeyと一致)
next_index			# 辞書のインデックス (len(user_list)と一致)
tmp_tweet_list 		# 1回のアクセスで取得したツイートデータ
tmp_user_info		# 1回のアクセスで追加したユーザリストの詳細データ
read_break_status	# 中断状態を読み込む

# 共通設定
twitter = セッション取得メソッド() # 引用
common_setting = json設定取得メソッド() # 引用
period_params = common_setting['period']
params = {} # 引用

# 限定設定
# break_statusの存在チェック
result = break_status存在判定メソッド('json_filename')

if result:
	# break_statusがある場合の設定
	read_break_status = break_status設定取得メソッド('json_filename')
	until_params = read_break_status['last_get_date']
	params['until'] = until_params
else:
	# break_statusがない場合の設定
	# ないか

'''
# 構造
# -----loop-----
    # 100件取得
    # -----loop-----
        # 名前確認
        # 重複確認
        # user_list追加
        # tmp_user_ingo追加
        # 期間判定
        # アクセス制限判定
        # params上書き
    # -----loop-----
# -----loop-----
'''

while True:
	'''
	取得処理
	'''
	gettweet (100)
	
	'''
	リスト作成処理
	'''
	while (range(tmp_tweet_list): # 1アクセス分のtweetを処理
		# 名前確認
		# 重複をidで確認
		if result.user.id in (user_list):    # ユーザ重複確認
		    ユーザ情報を設定するメソッド(tmp_tweet_list['text']['user'])
		    
		    user_list.add(tmp_tweet_list['user']['id'])
		else:
		    処理しない
	
	'''
	判定処理
	'''
	last_created_at = 一番古い取得日付を設定するメソッド() # 引用
	last_created_at_params = created_at → until_params 変換メソッド(last_created_at)
	
	# 取得期間チェック
	if period_params > last_created_at_params:
	    break
	
	# アクセス制限回避
	checkLimit() # 引用
	'''
	設定上書き
	'''
	params['until'] = last_created_at

# 書き込み処理
break_status書き込みメソッド(read_break_status, last_created_at_params)
user_info結果書き込みメソッド(user_info)


※取得範囲日付は大体でいいため、中身の日付はチェックしない



# ツイート検索実施
tweet検索 "アライさん"

# ツイート検索結果 > ユーザ情報 > ユーザ名 "アライさん" で絞る
result.user.name LIKE "%アライさん%"

# ユーザIDリストになければ追加
if (user_id in not user_list)
    user_list.add(user_id)
else 
    continue


【メソッド】
------------------------------
■[twitter_util]
# twitterセッションを取得する # 引用
■createTwitterSession():
	# return session
# tmp_tweet_list から tmp_user_infoに設定する # 新規
■setToUserInfo(info):
	# tmp_user_info = info[各種情報]
	# …
	# return tmp_user_list
# アクセス制限解除までwaitする # 引用
■checkLimit():
    # return None
# 一番古い取得日付を設定する # 新規
■setOldDate(tweet_list):
    # return last_created_at
------------------------------
[json_util]
# 共通設定読み込む # 引用
■readCommonSetting(setting_uri):
	# return json_data
# break_status書き込む # 新規
■writeBreakStatus(old_break_status, last_get_date):
    # old_break_status バックアップ (YYYYMMDDHHMMSS_break_status.json)
    # break_status = old_break_status
    # break_status['last_get_date'] = last_get_date
    # 最古取得日のみ 書き込み
    # return None
# 結果を書き込む # 引用
■writeJsonData(json_data, path)
	# return None
# 結果を追記する # 新規
□addUserInfoList(path, user_info)
	# break_statusからpathを取得

#os.path.isfile(path)があるため不要
## jsonfile存在を確認する
#isJsonFile(dir, json_filename):
#	# return boolean

------------------------------
■[date_util]
# created_at → params_until 変換 # 引用
■createdAtToParam(created_at):
    # return params_until
# datetime → params_until 変換 # 引用
■dateTimeToParam(datetime):
    # return params_until
# datetime → params_until 変換 # 引用
# 時間増減オプション
■dateTimeToParamOption(datetime, minutes=0, is_plus=False):
    # return params_until
------------------------------


※追加別モジュール
●結果読み込みメソッド # ほぼ引用
	# コピペしてexcelに貼り付けたい
	# return None

■課題
【取得期間について】
目標 = 過去１か月でアクティブなユーザーを対象にしたい
１日分実施(実行時間60分くらい想定)
・取得したユーザ情報の保存
・取得した最古時間の保存



