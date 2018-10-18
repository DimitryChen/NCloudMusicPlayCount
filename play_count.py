import base64
import datetime
import json
import math

import requests

from Crypto.Cipher import AES

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Host": "music.163.com",
    "Origin": "https://music.163.com",
    "Referer": "https://music.163.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
}


def calc_play_count(json_data, f):
    length = len(json_data)
    if length == 0:
        f.write("no data\n")
        return
    count = [1] * length
    i = 0
    count[0] = math.floor(100 / json_data[-1]["score"])
    p = 100
    while True:
        for i in range(length):
            data = json_data[i]
            count[i] = max(1, int(data["score"] / 100 * count[0]))
            while True:
                # score 为 次数相除，向下取整。
                p = int(count[i] / count[0] * 100)
                if p == data["score"] or p > 100:
                    i += 1
                    break
                count[i] += 1
            if p > 100:
                break
        if p > 100:
            i = 0
            count[0] += 1
            continue
        if i == length:
            break
    song_name = [""] * length
    singer_name = [""] * length
    for i in range(length):
        data = json_data[i]
        song_name[i] = data["song"]["name"]
        singer_name[i] = data["song"]["ar"][0]["name"]
    for i in range(length):
        temp = "%02d: %03d times\t[%s - %s]\n" % (
            i, count[i], song_name[i], singer_name[i])
        f.write(temp)


def AES_encrypt(plain_text, key):
    '''本函数为以下js代码的python版本
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    js中返回的密文是实际AES加密后再经过base64编码的数据。
    '''
    key_data = key.encode("utf-8")
    IV = "0102030405060708".encode("utf-8")
    cryptor = AES.new(key_data, AES.MODE_CBC, IV)

    padding_len = 16 - (len(plain_text) & 0xf)
    plain_data = (plain_text + chr(padding_len) * padding_len).encode("utf-8")
    cipher_data = cryptor.encrypt(plain_data)
    return base64.b64encode(cipher_data).decode("utf-8")


def get_encrypted_data(raw_data):
    json_str = json.dumps(raw_data)
    g = "0CoJUm6Qyw8W8jud"
    i = "7Sqn81qnWueMIrue"

    h = {}
    h["encText"] = AES_encrypt(json_str, g)
    h["encText"] = AES_encrypt(h["encText"], i)
    h["encSecKey"] = "22f32d9a7de53e27c16de2c9d47ee1fc1f4a9781e7732443c31b994421521ac8756431c7b6605de714fe909c2ff4c3db32ad31fb1d46e957e64377f88fb37bb2bc02770c146f99d5bd76fa3039bb1aa30e22618eb3e4f29f1184f106c25f33aa6cc65c065231794d09ac011555628e55029eb3ce72c10e07c71aad126a921ed6"
    return h


def get_encrypted_post_data(raw_data):
    h = get_encrypted_data(raw_data)
    post_data = {
        "params": h["encText"],
        "encSecKey": h["encSecKey"]
    }
    return post_data


def get_record_data(user_id):
    record_url = "https://music.163.com/weapi/v1/play/record"
    raw_data = {
        "csrf_token": "",
        "limit": "1000",
        "offset": "0",
        "total": "true",
        "type": "-1",
        "uid": user_id,
    }
    post_data = get_encrypted_post_data(raw_data)

    r = requests.post(record_url, data=post_data, headers=headers)
    json_data = r.json()

    t = datetime.datetime.today()
    file_name_prefix = "%04d%02d%02d_%s" % (t.year, t.month, t.day, user_id)

    json_file_name = "%s.json" % (file_name_prefix)
    with open(json_file_name, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    txt_file_name = "%s.txt" % (file_name_prefix)
    with open(txt_file_name, "w", encoding="utf-8") as fout:
        fout.write("最近一周\n")
        calc_play_count(json_data["weekData"], fout)
        fout.write("==========\n")
        fout.write("所有时间\n")
        calc_play_count(json_data["allData"], fout)


def main():
    user_id = "556458"
    get_record_data(user_id)
    print("done")


if __name__ == "__main__":
    main()
