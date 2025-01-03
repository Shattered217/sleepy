import requests
import time
import win32gui

# 显示进程白名单
white_list = [  
    "QQ",
    "微信",
    "TelegramDesktop",
    "Steam"
]

output_set = set()
windows_list = []
win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), windows_list)

def get_desktop():
    output_set.clear()  # 每次调用前清空 output_set
    for window in windows_list:
        title = win32gui.GetWindowText(window)
        if title in white_list and title not in output_set:
            output_set.add(title)

def seed():
    url = "http://127.0.0.1/pc_status"
    secret = "123456"
    pc_status = "0"

    get_desktop()  # 获取当前进程
    pc_app_name = list(output_set)  # 将 output_set 转换为列表

    params = {
        "secret": secret,
        "pc_status": pc_status,
    }

    # 对每个应用程序，使用相同的键（pcapp_name）传递多个值
    for app in pc_app_name:
        params.setdefault("pc_app_name", []).append(app)

    # 发送请求
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("信息发送成功:", response.text)
    else:
        print("信息发送失败")

while True:
    seed()
    time.sleep(10)
