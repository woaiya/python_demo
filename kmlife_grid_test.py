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
    "X-TOKEN": "5b3rq10iqnillqciijhvs4pcbc",
    "User-Agent": "com.qmsh.hbq/1.2.8 (Linux; U; Android 5.1; zh-cn) (vivo; 10208)",
}

gird_data = {
    "buy_gird_time": "2018-07-02 11:50:47",
    "areaCode": "440305",
    "index": "221",
    "is_fist_time": "",
    "is_continue": True,
}


def time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    return now_time


def dev_grid():
    try:
        new_time = time()
        url = interface + "areaCode=%s&next=%s" % (gird_data["areaCode"], gird_data["index"])
        data = json.loads(requests.get(url, headers=headers, verify=False, timeout=5).content)
        gird_index_data = data["data"]["items"][0]
        if gird_index_data["ad"] is None:
            gird_data["is_continue"] = False
            log_data = "%s: 格子下架,监控结束" % new_time
        else:
            is_banned = gird_index_data["ad"]["isBanned"]
            banned_text = gird_index_data["ad"]["bannedText"]
            if is_banned is True:
                log_data = "%s: %s" % (new_time, banned_text)
            else:
                if gird_data["is_fist_time"] == "":
                    gird_data["is_fist_time"] = new_time
                    log_data = "%s: 当前格子已通过审核" % new_time
                else:
                    log_data = "%s: 当前格子已展示" % new_time
        print(log_data)
        return log_data
    except KeyError as e:
        print(e)
        return e


if __name__ == "__main__":
    txt_name = "grid_test.txt"

    while gird_data["is_continue"] is True:
        log_test_data = dev_grid()
        with open(txt_name, "a+", encoding='utf8') as f:
            f.write(log_test_data + "\n")
        sleep(600)


