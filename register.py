# -*- coding:utf-8 -*-
"""
register.db 的address表包含地名(name)和编码(code)

"""

import random
import string
import mydata
import datetime


def create_phone_number():
    """随机生成11位手机号"""
    mobile_begin_seed = ['139', '138', '137', '136', '135', '134',
                         '159', '158', '157', '150', '151', '152',
                         '188', '187', '182', '183', '184', '178',
                         '130', '131', '132', '156', '155', '186',
                         '185', '176', '133', '153', '189', '180',
                         '181', '177']

    return random.choice(mobile_begin_seed) + ''.join(random.choice("0123456789") for i in range(8))


def create_number(length=6):
    """随机数字"""
    return ''.join(random.choice(string.digits) for i in range(length))


def create_string(length=6):
    """随机字符串"""
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def create_uname():
    """随机混合字符串和数字"""
    string_length = random.randint(min_length, max_length)
    letter_length = random.randint(1, string_length - 1)
    return create_string(string_length) + create_number(letter_length)


def create_birthday(start='1960-01-01', end='2000-12-30'):
    """
    随机生成生日日期
    """
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birth_days = datetime.datetime.strftime(
        datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d")
    return birth_days


def create_id_number():
    """
    随机生成中国大陆身份证号
    """
    def get_validate_check_out(id17):
        """
        身份证号码校验码算法
        """
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 十七位数字本体码权重
        validate = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # mod11,对应校验码字符值
        sum_ = 0
        mode_ = 0
        for i in range(0, len(id17)):
            sum_ = sum_ + int(id17[i]) * weight[i]
        mode_ = sum_ % 11
        return validate[mode_]

    addr = mydata.addr
    addr_info = random.randint(0, len(addr))
    addr_id = addr[addr_info][0]
    id_number = str(addr_id)
    id_number = id_number + create_birthday()

    for i in range(2):
        n = random.randint(0, 9)
        id_number = id_number + str(n)
    sex_id = random.randrange(random.randint(0, 1), 10, step=2)
    id_number = id_number + str(sex_id)
    check_out = get_validate_check_out(id_number)
    id_number = id_number + str(check_out)
    return id_number


def create_name():
    """
    随机生成人名
    """
    first_name = random.choice(mydata.first_name)
    midlle_name = random.choice(mydata.other_name)
    last_name = random.choice(mydata.other_name)
    return first_name+midlle_name+last_name


def main():
    print('姓名为: %s' % create_name())
    print('出生日期: %s' % create_birthday())
    print('用户名为: %s' % create_string())
    print('密码为: %s' % create_string())
    print('手机号为: %s' % create_phone_number())
    print('身份证号码为: %s' % create_id_number())

if __name__ == '__main__':
    for i in range(100):
        main()