排除列表 = [
    "任务栏",
    "NVIDIA GeForce Overlay DT",
    "NVIDIA GeForce Overlay",
    "Program Manager",
    "任务切换程序",
    "Shattered?的Redmi K60 Pro",
]
服务器地址 = "https://onlsy.shattered.top/pc_status"
secret = "ilovesy"

import requests
import time
from pywinauto import Desktop
while True:
    try:
        windows = Desktop(backend="uia").windows()
        o = []
        for w in windows:
            t = w.window_text().split("-")[-1].strip()
            if t not in 排除列表 and t not in o and t:
                o.append(t)
        print(o)
        if len(o) > 0:
            requests.get(
                服务器地址,
                params={
                    "pc_status": 0,
                    "pc_app_name": " | ".join(o),
                    "secret": secret,
                },
            )
        else:
            requests.get(
                服务器地址, params={"pc_status": 1, "pc_app_name": "", "secret": secret}
            )
        time.sleep(10)
    except Exception as e:
        if str(e) == "KeyboardInterrupt":
            break