import win32com.client
import win32api
import win32gui
import win32con
import time

# 注册大漠插件
DM = win32com.client.Dispatch('dm.dmsoft')
# 设置大漠字库文件
DM.SetDict(0, 'dict.txt')


def show_window(hwnds):
    counter = 0
    for each in hwnds:
        print(counter)
        print(each)
        print(win32gui.GetWindowText(each))
        print(win32gui.GetClassName(each))
        counter += 1
        print('='*99)


def run_app(app_dir):
    win32api.ShellExecute(0, 'open', app_dir, '', '', 1)
    time.sleep(1.5)


def enum_child_window(parent):
    child_window_list = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), child_window_list)
    return child_window_list


def click_child_window(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)


def send_string(hwnd, string):
    win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, string)


def mouse(x, y, order='leftclick'):
    """
    鼠标相关指令
    """
    order_dict = {'leftclick': DM.LeftClick,
                  'rightclick': DM.RightClick,
                  'leftdown': DM.LeftDown,
                  'leftup': DM.LeftUp,
                  'leftdoubleclick': DM.LeftDoubleClick}
    DM.MoveTo(x, y)
    time.sleep(0.05)
    order_dict[order]()

if __name__ == '__main__':
    pass
