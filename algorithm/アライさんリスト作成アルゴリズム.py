���A���C���񌟍��A���S���Y��


'''
������
'''
# ����
user_info => json�ۑ�				# �ŏI�I�Ȑ��ʕ�
write_break_status => json�ۑ�		# ���f���̏�Ԃ�ۑ��Buntil��ݒ肵�čĊJ�\�ɂ���B
# �ꎞ����
user_list 			# �d���`�F�b�N�̂��߂ɕێ����郆�[�U���X�g (user_info��key�ƈ�v)
next_index			# �����̃C���f�b�N�X (len(user_list)�ƈ�v)
tmp_tweet_list 		# 1��̃A�N�Z�X�Ŏ擾�����c�C�[�g�f�[�^
tmp_user_info		# 1��̃A�N�Z�X�Œǉ��������[�U���X�g�̏ڍ׃f�[�^
read_break_status	# ���f��Ԃ�ǂݍ���

# ���ʐݒ�
twitter = �Z�b�V�����擾���\�b�h() # ���p
common_setting = json�ݒ�擾���\�b�h() # ���p
period_params = common_setting['period']
params = {} # ���p

# ����ݒ�
# break_status�̑��݃`�F�b�N
result = break_status���ݔ��胁�\�b�h('json_filename')

if result:
	# break_status������ꍇ�̐ݒ�
	read_break_status = break_status�ݒ�擾���\�b�h('json_filename')
	until_params = read_break_status['last_get_date']
	params['until'] = until_params
else:
	# break_status���Ȃ��ꍇ�̐ݒ�
	# �Ȃ���

'''
# �\��
# -----loop-----
    # 100���擾
    # -----loop-----
        # ���O�m�F
        # �d���m�F
        # user_list�ǉ�
        # tmp_user_ingo�ǉ�
        # ���Ԕ���
        # �A�N�Z�X��������
        # params�㏑��
    # -----loop-----
# -----loop-----
'''

while True:
	'''
	�擾����
	'''
	gettweet (100)
	
	'''
	���X�g�쐬����
	'''
	while (range(tmp_tweet_list): # 1�A�N�Z�X����tweet������
		# ���O�m�F
		# �d����id�Ŋm�F
		if result.user.id in (user_list):    # ���[�U�d���m�F
		    ���[�U����ݒ肷�郁�\�b�h(tmp_tweet_list['text']['user'])
		    
		    user_list.add(tmp_tweet_list['user']['id'])
		else:
		    �������Ȃ�
	
	'''
	���菈��
	'''
	last_created_at = ��ԌÂ��擾���t��ݒ肷�郁�\�b�h() # ���p
	last_created_at_params = created_at �� until_params �ϊ����\�b�h(last_created_at)
	
	# �擾���ԃ`�F�b�N
	if period_params > last_created_at_params:
	    break
	
	# �A�N�Z�X�������
	checkLimit() # ���p
	'''
	�ݒ�㏑��
	'''
	params['until'] = last_created_at

# �������ݏ���
break_status�������݃��\�b�h(read_break_status, last_created_at_params)
user_info���ʏ������݃��\�b�h(user_info)


���擾�͈͓��t�͑�̂ł������߁A���g�̓��t�̓`�F�b�N���Ȃ�



# �c�C�[�g�������{
tweet���� "�A���C����"

# �c�C�[�g�������� > ���[�U��� > ���[�U�� "�A���C����" �ōi��
result.user.name LIKE "%�A���C����%"

# ���[�UID���X�g�ɂȂ���Βǉ�
if (user_id in not user_list)
    user_list.add(user_id)
else 
    continue


�y���\�b�h�z
------------------------------
��[twitter_util]
# twitter�Z�b�V�������擾���� # ���p
��createTwitterSession():
	# return session
# tmp_tweet_list ���� tmp_user_info�ɐݒ肷�� # �V�K
��setToUserInfo(info):
	# tmp_user_info = info[�e����]
	# �c
	# return tmp_user_list
# �A�N�Z�X���������܂�wait���� # ���p
��checkLimit():
    # return None
# ��ԌÂ��擾���t��ݒ肷�� # �V�K
��setOldDate(tweet_list):
    # return last_created_at
------------------------------
[json_util]
# ���ʐݒ�ǂݍ��� # ���p
��readCommonSetting(setting_uri):
	# return json_data
# break_status�������� # �V�K
��writeBreakStatus(old_break_status, last_get_date):
    # old_break_status �o�b�N�A�b�v (YYYYMMDDHHMMSS_break_status.json)
    # break_status = old_break_status
    # break_status['last_get_date'] = last_get_date
    # �ŌÎ擾���̂� ��������
    # return None
# ���ʂ��������� # ���p
��writeJsonData(json_data, path)
	# return None
# ���ʂ�ǋL���� # �V�K
��addUserInfoList(path, user_info)
	# break_status����path���擾

#os.path.isfile(path)�����邽�ߕs�v
## jsonfile���݂��m�F����
#isJsonFile(dir, json_filename):
#	# return boolean

------------------------------
��[date_util]
# created_at �� params_until �ϊ� # ���p
��createdAtToParam(created_at):
    # return params_until
# datetime �� params_until �ϊ� # ���p
��dateTimeToParam(datetime):
    # return params_until
# datetime �� params_until �ϊ� # ���p
# ���ԑ����I�v�V����
��dateTimeToParamOption(datetime, minutes=0, is_plus=False):
    # return params_until
------------------------------


���ǉ��ʃ��W���[��
�����ʓǂݍ��݃��\�b�h # �قڈ��p
	# �R�s�y����excel�ɓ\��t������
	# return None

���ۑ�
�y�擾���Ԃɂ��āz
�ڕW = �ߋ��P�����ŃA�N�e�B�u�ȃ��[�U�[��Ώۂɂ�����
�P�������{(���s����60�����炢�z��)
�E�擾�������[�U���̕ۑ�
�E�擾�����ŌÎ��Ԃ̕ۑ�



