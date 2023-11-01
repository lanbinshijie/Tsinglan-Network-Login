import time
import requests
import json
import tkinter as tk
from tkinter import messagebox
import subprocess

def generate_auth_tag():
    rckey = str(int(time.time() * 1000))
    pwd = do_encrypt_rc4("hzy123231", rckey)
    return pwd, rckey

def do_encrypt_rc4(src, passwd):
    src = src.strip()
    passwd = str(passwd)

    key = bytearray([0] * 256)
    sbox = bytearray([0] * 256)
    output = [""] * len(src)

    plen = len(passwd)
    size = len(src)

    for i in range(256):
        key[i] = ord(passwd[i % plen])
        sbox[i] = i
    j = 0
    for i in range(256):
        j = (j + sbox[i] + key[i]) % 256
        temp = sbox[i]
        sbox[i] = sbox[j]
        sbox[j] = temp

    a = 0
    b = 0
    for i in range(size):
        a = (a + 1) % 256
        b = (b + sbox[a]) % 256
        temp = sbox[a]
        sbox[a] = sbox[b]
        sbox[b] = temp
        c = (sbox[a] + sbox[b]) % 256
        temp = ord(src[i]) ^ sbox[c]
        temp = hex(temp)[2:].zfill(2)
        output[i] = temp

    return "".join(output)

def praseResponse(response):
    content = response.content.decode()  # 将返回的字节流转换为字符串
    content = content.replace("'", "\"")
    json_data = json.loads(content)
    return json_data

def authInternet():
    auth_tag, rckey = generate_auth_tag()

    url = "http://4.3.2.1/ac_portal/login.php"
    data = {
        "opr": "pwdLogin",
        "userName": "20270244",
        "pwd": auth_tag,
        "auth_tag": rckey,
        "rememberPwd": "0"
    }
    response = requests.post(url, data=data)
    json_data = praseResponse(response)

    if json_data["success"]: 
        return json_data
    else: return False

def getUsername():
    url = "http://4.3.2.1/homepage/info.php"
    data = {
        "opr": "list"
    }
    response = requests.post(url, data)
    json_data = praseResponse(response)

    showname, number = json_data["data"]["basic"].get("showname"), json_data["data"]["basic"].get("name")
    return showname, number


def get_current_ssid():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
        result = result.decode("utf-8", errors="replace")
        
        for line in result.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    ssid = get_current_ssid()
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    if ssid == "Tsinglan-School":
        res = authInternet()
        if not res:
            messagebox.showerror('错误', '自动登录校园网失败')
        else:
            showname, uid = getUsername()
            messagebox.showinfo('登录成功', f'校园网登录成功！欢迎“{showname}”！')
        root.destroy()

    elif ssid == "wz":
        messagebox.showinfo('连接成功', '家庭网络连接成功！')
    else:
        messagebox.showinfo('连接成功', f"连接网络“{ssid}”成功！")
    


