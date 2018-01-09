#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Sword

import hashlib
import urllib.request
import urllib
import json
import base64


def md5str(string):
    """md5加密字符串"""
    m = hashlib.md5(string.encode(encoding='utf8'))
    return m.hexdigest()


def md5(byte):
    """md5加密byte"""
    return hashlib.md5(byte).hexdigest()


class DamatuApi:

    ID = '47673'
    KEY = '9905665302f343891944acb947c6f713'
    HOST = 'http://api.dama2.com:7766/app/'

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def get_sign(self, param=b''):
        return (md5(bytes(self.KEY, encoding='utf8') + bytes(self.username, encoding='utf8') + param))[:8]

    def get_pwd(self):
        return md5str(self.KEY + md5str(md5str(self.username) + md5str(self.password)))

    def post(self, path, params):
        data = urllib.parse.urlencode(params).encode('utf-8')
        url = self.HOST + path
        response = urllib.request.Request(url,data)
        return urllib.request.urlopen(response).read()

    def get_balance(self):
        """
        查询余额
        return 是正数为余额 如果为负数 则为错误码
        """
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': dmt.get_pwd(),
                'sign': dmt.get_sign()
                }
        res = self.post('d2Balance', data)
        res = str(res, encoding='utf8')
        json_res = json.loads(res)
        if json_res['ret'] == 0:
            return json_res['balance']
        else:
            return json_res['ret']

    def decode(self, file_path, type_content):
        """
        上传验证码
        参数filePath 验证码图片路径
        如d:/1.jpg type是类型，查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc
        return 是答案为成功 如果为负数 则为错误码
        """
        with open(file_path, 'rb') as f:
            fdata = f.read()
            filedata = base64.b64encode(fdata)

        data = {'appID': self.ID,
                'user': self.username,
                'pwd': dmt.get_pwd(),
                'type': type_content,
                'fileDataBase64': filedata,
                'sign': dmt.get_sign(fdata)
                }
        res = self.post('d2File', data)
        res = str(res, encoding='utf8')
        json_res = json.loads(res)
        if json_res['ret'] == 0:
            # 注意这个json里面有ret，id，result，cookie，根据自己的需要获取
            return json_res['result']
        else:
            return json_res['ret']

    def decode_url(self, url, type_content):
        """
        url地址打码
        参数 url地址
        type是类型(类型查看http://wiki.dama2.com/index.php?n=ApiDoc.Pricedesc)
        return 是答案为成功 如果为负数 则为错误码
        """
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': dmt.get_pwd(),
                'type': type_content,
                'url': urllib.parse.quote(url),
                'sign': dmt.get_sign(url.encode(encoding='utf8'))
                }
        res = self.post('d2Url', data)
        res = str(res, encoding='utf8')
        json_res = json.loads(res)
        if json_res['ret'] == 0:
            # 注意这个json里面有ret，id，result，cookie，根据自己的需要获取
            return json_res['result']
        else:
            return json_res['ret']

    def report_error(self, error_id):
        """
        报错
        参数id(string类型)由上传打码函数的结果获得
        return 0为成功 其他见错误码
        """
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': dmt.get_pwd(),
                'id': error_id,
                'sign': dmt.get_sign(error_id.encode(encoding='utf8'))
                }
        res = self.post('d2report_error', data)
        res = str(res, encoding='utf8')
        json_res = json.loads(res)
        return json_res['ret']


if __name__ == '__main__':
    # 调用类型实例：
    # 1.实例化类型 参数是用户账号和密码
    dmt = DamatuApi("test", "test")
    # 2.调用方法：
    # 查询余额
    print(dmt.get_balance())
    # 上传打码
    print(dmt.decode('0349.bmp', 200))
    # 上传打码
    print(dmt.decode_url('http://captcha.qq.com/getimage?aid=549000912&r=0.7257105156128585&uin=3056517021', 200))
    # print(dmt.report_error('894657096'))