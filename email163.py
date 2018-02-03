#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 14:58
# @Author  : Sword
# @Site    : 
# @File    : email163.py
# @Software: PyCharm

import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


poplib._MAXLINE = 20480  # 防止异常"line too long"


class EMail163(object):
    def __init__(self, email, password):
        self.server = poplib.POP3('pop.163.com')
        self.server.set_debuglevel(0)  # 关闭调试信息
        self.server.user(email)
        self.server.pass_(password)

    def guess_charset(self, message):
        charset = message.get_charset()
        if charset is None:
            content_type = message.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def decode_str(self, astr):
        value, charset = decode_header(astr)[0]
        if charset:
            value = value.decode(charset)
        return value

    def get_message_count(self):
        """获取邮件总数"""
        total, _ = self.server.stat()
        return total

    def get_message_list(self):
        """获取邮件列表"""
        response, messages, octets = self.server.list()
        return messages

    def get_message_content(self, index):
        """获取邮件内容"""
        resp, lines, octets = self.server.retr(index)
        try:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
        except UnicodeDecodeError:
            msg_content = b'\r\n'.join(lines).decode('gbk')

        return Parser().parsestr(msg_content)

    def get_subject(self, message):
        """获取主题"""
        content = message.get('subject')
        # 如果主题无法正常解码则返回原数据
        try:
            subject = self.decode_str(content)
        except UnicodeDecodeError:
            subject = content
        return subject

    def get_from_info(self, message):
        """获取发件人信息"""
        # 如果发件人信息无法正常解码则返回原数据
        content = message.get('from')
        try:
            result = self.decode_str(content)
        except UnicodeDecodeError:
            result = content
        return result

    def get_message_text(self, message):
        for part in message.walk():
            if part.get_content_type() == 'text/html':
                content = part.get_payload(decode=True)
                charset = self.guess_charset(part)
                if charset:
                    content = content.decode(charset)
                    return content


if __name__ == '__main__':
    foo = EMail163('chenjianbird@163.com', '123456aa')
    total = foo.get_message_count()
    for each in range(total, 0, -1):
        message = foo.get_message_content(each)
        print('{}第{}封邮件{}'.format('-'*40, total-each, '-'*40))
        print('主题: {}'.format(foo.get_subject(message)))
        print('发件人: {}'.format(foo.get_from_info(message)))
        print(foo.get_message_text(message))