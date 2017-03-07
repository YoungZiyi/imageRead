# coding=utf-8
import os, sys
import random
import string
import requests
from queue import Queue
import threading

support_system = [
    # 'zhengfang',
    # 'qingguo',
    'qiangzhi',
]

zhengfang_captcha_url = [
    'http://222.179.134.225:81/CheckCode.aspx',
]

qiangzhi_captcha_url = [
    'http://jw.whcvc.edu.cn/other/CheckCode.aspx',  # 200786422
    'http://jwoa.jxjtxy.com/jxjtxy/other/CheckCode.aspx',  # 200637371
    'http://221.234.72.4/jiaowu_eszy/other/CheckCode.aspx',  # 200478089
]

def genStr(N):
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits
    ) for _ in range(N))

def downloadImg(url, path):
    try:
        rsp = requests.get(url, stream=True)
        with open(path, 'wb') as fd:
            for chunk in rsp.iter_content(chunk_size=128):
                fd.write(chunk)
    except Exception as e:
        return False
    else:
        return True

if __name__ == '__main__':
    save_dir = ''
    captcha_url_list = []

    try:
        system_type = sys.argv[1]
        save_dir = 'sample/' + system_type + '/'
        get_num = sys.argv[2]

        # download [get_num] pictures
        if not get_num.isdigit():
            get_num = 10
        else:
            get_num = int(get_num)

        if not system_type in support_system:
            raise Exception('System type not support')

        exec('captcha_url_list = ' + system_type + '_captcha_url')
        if captcha_url_list == []:
            raise Exception('url list is empty')

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('err_file:' + fname + '|err_line:' + str(exc_tb.tb_lineno) + '|err_msg:' + e.__str__())
        sys.exit(1)

    for i in range(get_num):
        msg = str(i+1) + ':downloading image from '

        url =random.choice(captcha_url_list)
        path = save_dir + genStr(10)

        result = downloadImg(url, path)

        msg = msg + url + ' '

        if result:
            msg = msg + 'successfully'
        else:
            msg = msg + 'failed'

        print(msg)
