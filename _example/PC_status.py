import requests
import time
import win32gui

white_list = ["QQ", "微信"]  # 显示进程白名单

output_set = set()
windows_list = []
win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), windows_list)

def get_desktop():
    output_set.clear()
    for window in windows_list:
        title = win32gui.GetWindowText(window)
        if title in white_list and title not in output_set:
            output_set.add(title)

def seed():
    url = "https://domain/pc_status" # 你的服务器地址
    secret = "123456" # 你的secret
    pc_status = "0"

    get_desktop()
    pc_app_name = list(output_set)

    print(f"Current apps: {pc_app_name}")

    params = {
        "secret": secret,
        "pc_status": pc_status,
    }

    for app in pc_app_name:
        params.setdefault("pc_app_name", []).append(app)

    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("信息发送成功:", response.text)
    else:
        print("信息发送失败")

while True:
    seed()
    time.sleep(10)
