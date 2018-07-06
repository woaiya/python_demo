#!usr/bin/env python
# _*_ coding:utf-8 _*_

import json
import requests
import datetime

from time import sleep

# 用来去掉https请求警告  在请求中需要加上  verify=False
requests.packages.urllib3.disable_warnings()
interface = "https://api.qianmishenghuo.com/lord/boxList?"

headers = {
    'content-type': 'application/json',
    "Accept - Encoding": "gzip",
	"cid": "97587b361e9862fd260ad5a6807501f2",
    "X-TOKEN": "1h1b7gff0d71hr4p40tn3l4k1o",
    "User-Agent": "com.qmsh.hbq/1.2.8 (Linux; U; Android 5.1; zh-cn) (vivo; 10208)",
}

grid = {
    "url": "",
    "is_continue": True,
    "is_fist_time": "",
}


def detection(func):
    def write(*args, **kwargs):
        global func_log
        new_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            func_data = func(*args, **kwargs)
            if func_data["code"] == 200:
                gird_data = func_data["data"]["items"][0]
                if gird_data["index"] != args[1]:
                    print("格子数据不一致,监控失败")
                    grid["is_continue"] = False
                else:
                    if gird_data["ad"] is None:
                        func_log = "%s : %s" % (new_time, "格子已下架,监控结束")
                        grid["is_continue"] = False
                    else:
                        is_banned = gird_data["ad"]["isBanned"]
                        banned_text = gird_data["ad"]["bannedText"]
                        if is_banned is True:
                            func_log = "%s: %s" % (new_time, banned_text)
                        else:
                            if grid["is_fist_time"] == "":
                                grid["is_fist_time"] = new_time
                                func_log = "%s: 当前格子已通过审核" % new_time
                            else:
                                func_log = "%s: 当前格子已展示" % new_time
            elif func_data["code"] == 401:
                func_log = "%s : %s  %s" % (new_time, grid["url"], func_data["message"])
            else:
                func_log = "%s : %s  %s" % (new_time, grid["url"], func_data["code"])
        except Exception as e:
            func_log = "%s : %s  %s" % (new_time, grid["url"], e)
        print(func_log)
        return func_log
    return write


@detection
def re_data(area_code, index):
    url = interface + "areaCode=%s&next=%s" % (area_code, index)
    interface_data = json.loads(requests.get(url, headers=headers, verify=False, timeout=5).content)
    grid["url"] = url
    return interface_data


if __name__ == "__main__":
    txt_name = "grid_test.txt"
    while grid["is_continue"] is True:
        up = re_data("440305", "245")
        with open(txt_name, "a+", encoding='utf8') as f:
            f.write(up + "\n")
        sleep(300)