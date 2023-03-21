import socket
import requests
import schedule
import time
import sys
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
import ctypes

# 告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 获取屏幕的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)/100*1.5


def get_host_ip():
    """
    查询本机ip地址
    :return: ip地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_np():
    """
    用户输入用户名和密码
    :return: 用户名，密码
    """
    root = tk.Tk()
    root.title("校园网自动登录")
    root.tk.call('tk', 'scaling', ScaleFactor)      # 设置程序缩放
    root.iconbitmap(get_resource_path("./AutoLogin.ico"))      # 设置窗口图标
    root.resizable(0, 0)    # 禁止缩放

    label1 = ttk.Label(root, anchor='e', width=6, text="用户名:")
    label1.grid(row=0, column=0, pady=10, padx=10)
    label2 = ttk.Label(root, anchor='e', width=6, text="密码:")
    label2.grid(row=1, column=0, pady=10, padx=10)

    entry1 = ttk.Entry(root, width=20)
    entry1.grid(row=0, column=1, pady=10, padx=20)
    entry2 = ttk.Entry(root, width=20, show='*')        # 密码用符号替代
    entry2.grid(row=1, column=1, pady=10, padx=20)

    def _get_entry():
        global uname, passw
        uname = entry1.get()
        passw = entry2.get()
        root.destroy()

    button = ttk.Button(root, text="确认", command=_get_entry)
    button.grid(row=2, column=1, pady=10, padx=20, ipady=10, ipadx=20)

    root.mainloop()


def throw_error():
    tk.Tk().withdraw()  # 隐藏主窗口
    mbox.showerror(title='出错了！', message=f'从IP {get_host_ip()} 自动登录失败！')


def login():
    """
    自动登录
    :return:
    """
    if len(uname) == 0 or len(passw) == 0:
        schedule.CancelJob()
        sys.exit(0)

    response1 = requests.post(url_get_permits, data_gp)
    response2 = requests.post(url_auth_action, data_aa)

    res1_text = response1.content.decode('utf-8')
    res2_text = response2.content.decode('utf-8')
    print(f'{res1_text}\n{res2_text}')

    if response1.status_code != 200 or response2.status_code != 200 or "login_ok" not in res2_text:
        throw_error()
        schedule.CancelJob()
        sys.exit(0)


if __name__ == "__main__":
    # 用于复旦大学校园网络认证平台，只需要输入用户名和密码
    uname, passw = ['', '']
    get_np()
    ip = get_host_ip()

    # 下面的这些要根据你自己的浏览器中的 data(数据)修改
    url_get_permits = 'http://10.108.255.249/get_permits.php'  # 请求网址
    url_auth_action = 'http://10.108.255.249/include/auth_action.php'  # 请求网址
    data_gp = {
        "username": uname,
    }
    data_aa = {
        "action": 'login',
        "username": uname,
        "password": passw,
        "ac_id": '1',
        "user_ip": ip,
        "nas_ip": '',
        "user_mac": '',
        "save_me": '0',
        "ajax": '1',
    }

    # 首次运行立即登录
    login()
    # 利用schedule实现定时任务
    schedule.every().day.at("03:01").do(login)
    while True:
        schedule.run_pending()
        time.sleep(30)




