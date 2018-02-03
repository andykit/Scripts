#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/30 16:26
# @Author  : Sword
# @Site    : http://www.ruokuai.com/
# @File    : verification.py
# @Software: PyCharm

import requests
import hashlib


class RClient(object):
    """若快打码平台"""

    def __init__(self, username, password, soft_id='96088', soft_key='6ee6f31019e04559892b1c47ad7c138f'):
        self.username = username
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {'username': self.username,
                            'password': self.password,
                            'softid': self.soft_id,
                            'softkey': self.soft_key}
        self.headers = {'Connection': 'Keep-Alive',
                        'Expect': '100-continue',
                        'User-Agent': 'ben'}

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {'typeid': im_type,
                  'timeout': timeout}
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json',
                          data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {'id': im_id}
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json',
                          data=params, headers=self.headers)
        return r.json()

    def print_balance(self):
        """获取余额"""
        r = requests.post('http://api.ruokuai.com/info.json', data=self.base_params, headers=self.headers)
        print('快豆余额：{}'.format(r.json()['Score']))
        return r.json()


if __name__ == '__main__':
    ck = RClient('china5', '123456aa', '96088', '6ee6f31019e04559892b1c47ad7c138f')
    ck.print_balance()