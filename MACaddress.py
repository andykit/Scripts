# -*- coding: utf-8 -*-
# @Author: Sword
# 2017-07-06

"""系统要求为 window7 简体中文版"""

import time
import re
import random
import platform
import winreg
import subprocess
import configparser
import os


# 一般MAC地址像这样的 00-00-00-00-00-00 或 00:00:00:00:00:00 或 000000000000
MAC_ADDRESS_RE = re.compile(r'''([0-9A-F]{1,2})[:-]?([0-9A-F]{1,2})[:-]?
                                ([0-9A-F]{1,2})[:-]?([0-9A-F]{1,2})[:-]?
                                ([0-9A-F]{1,2})[:-]?([0-9A-F]{1,2})''', re.I | re.VERBOSE)
WIN_REGISTRY_PATH = "SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"


def create_address():
    """
    创建新的mac网络物理地址
    在win7下从左往右第二个字符必须2,6,A,E其中之一
    """
    new_address = ''
    for i in range(1, 18):
        if i == 2:
            new_address += random.choice('26AE')
        elif i % 3 == 0:
            new_address += '-'
        else:
            new_address += random.choice('0123456789ABCDEF')
    return new_address


def choice_device(name_mac):
    """
    修改需要更改的网卡名称
    """
    for each in name_mac:
        print(str(each) + ' : ' + name_mac[each][0])
    result = int(input(u'请选择一个要更改的网卡序列号: '))
    return name_mac[result]


def get_device():
    """
    获取网络物理地址
    """
    # 读取配置里的网卡名称
    cf = configparser.ConfigParser()
    cf.read('Config.ini')
    address_name = cf.get('General', 'address')

    # 遍历计算机的网卡
    mac_info = subprocess.check_output('GETMAC /v /FO list', stderr=subprocess.STDOUT)

    # 获得字典[link name : MAC address]
    network_adapter = re.findall(b'\r\n\xcd\xf8\xc2\xe7\xca\xca\xc5\xe4\xc6\xf7:\s+(.+?)\r\n\xce\xef\xc0\xed\xb5\xd8\xd6\xb7',
                                 mac_info)
    mac_address = re.findall(b'\r\n\xce\xef\xc0\xed\xb5\xd8\xd6\xb7:\s+(.+?)\r\n\xb4\xab\xca\xe4\xc3\xfb\xb3\xc6',
                             mac_info)
    for i in range(len(network_adapter)):
        network_adapter[i] = network_adapter[i].decode('GBK')
        mac_address[i] = mac_address[i].decode('GBK')

    name_mac = zip(network_adapter, mac_address)

    # 检查配置网卡名称是否在包含在本机网卡里,如果不是选择网卡并存到配置里
    for each in name_mac:
        if each[0] == address_name:
            return each
    else:
        address_name = choice_device(name_mac)
        cf.set('General', 'address', address_name[0])
        cf.write(open('Config.ini', 'w'))
        return address_name


def restart_adapter(index):
    """
    重启网络设备
    """
    if platform.release() == 'XP':
        # description, adapter_name, address, current_address = find_interface(device)
        cmd = "devcon hwids =net"
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except FileNotFoundError:
            raise
        query = '(' + target_device + '\r\n\s*.*:\r\n\s*)PCI\\\\(([A-Z]|[0-9]|_|&)*)'
        query = query.encode('ascii')
        match = re.search(query, result)
        cmd = 'devcon restart "PCI\\' + str(match.group(2).decode('ascii')) + '"'
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    else:
        cmd = "wmic path win32_networkadapter where index=" + str(index) + " call disable"
        subprocess.check_output(cmd)
        time.sleep(1)
        cmd = "wmic path win32_networkadapter where index=" + str(index) + " call enable"
        subprocess.check_output(cmd)
        time.sleep(1)


def set_mac_address(new_mac, target_device):
    """
    更改注册表里的Address
    """
    reg_hdl = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    key = winreg.OpenKey(reg_hdl, WIN_REGISTRY_PATH)
    info = winreg.QueryInfoKey(key)

    # Find adapter key based on sub keys
    adapter_key = None
    adapter_path = None
    target_index = -1

    for index in range(info[0]):
        subkey = winreg.EnumKey(key, index)
        path = WIN_REGISTRY_PATH + "\\" + subkey

        if subkey == 'Properties':
            break

        # Check for adapter match for appropriate interface
        new_key = winreg.OpenKey(reg_hdl, path)
        try:
            adapterDesc = winreg.QueryValueEx(new_key, "DriverDesc")

            if adapterDesc[0] == target_device:
                adapter_path = path
                target_index = index
                break
            else:
                winreg.CloseKey(new_key)
        except (WindowsError) as err:
            if err.errno == 2:  # register value not found, ok to ignore
                pass
            else:
                raise err

    if adapter_path is None:
        print('Device not found.')
        winreg.CloseKey(key)
        winreg.CloseKey(reg_hdl)
        return

    # Registry path found update mac addr
    adapter_key = winreg.OpenKey(reg_hdl, adapter_path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(adapter_key, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
    winreg.CloseKey(adapter_key)
    winreg.CloseKey(key)
    winreg.CloseKey(reg_hdl)

    # Adapter must be restarted in order for change to take affect
    # print 'Now you should restart your netsh'
    restart_adapter(target_index)


def change_mac_address():
    target_device, mac_address = get_device()
    new_mac_address = create_address()
    while mac_address != new_mac_address:
        set_mac_address(new_mac_address, target_device)
        target_device, mac_address = get_device()
    time.sleep(3)


if __name__ == '__main__':
    print('更改前的物理网址: %s' % get_device()[1])
    change_mac_address()
    print('更改后的物理网址: %s' % get_device()[1])