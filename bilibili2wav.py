import os
import re
import json
import requests
from time import sleep

# Colorama for colored console output
from colorama import init, Fore, Back
init(autoreset=True)

# Configuration Constants
PROXY = ""
PROXY_USED_TIMES = 0
RATE = "128k"
REMOVE_ORIGINAL = True
USE_PROXY = False
GLOBAL_SLEEP_TIME = 60 * 5

# HTTP Headers for requests
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"),
    "Referer": "https://www.bilibili.com/",
    "Origin": "https://www.bilibili.com/",
    "Sec-Ch-Ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    "Cache-Control": "max-age=0"
}

# Function to sanitize file name
def getPathTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # Invalid characters
    return re.sub(rstr, "_", title)

# Create directory if it doesn't exist
def mkdir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

# Bilibili ID Conversion
table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {table[i]: i for i in range(58)}
s = [11, 10, 3, 8, 4, 6]
XOR = 177451812
ADD = 8728348608

def toAid(x):
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - ADD) ^ XOR

def toBvid(x):
    x = (x ^ XOR) + ADD
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58 ** i % 58]
    return ''.join(r)

# Convert seconds to LRC format time
def toLrcTime(time):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d.%02d" % (m, s, h)

# Manage JSON to LRC conversion
def manage_bili_json_to_lrc(json_str):
    json_str = json.loads(json_str)["body"]
    lrc = ""
    for i in json_str:
        lrc += "[" + toLrcTime(i["from"]) + "]" + i["content"] + "\n"
    return lrc

# Convert to WAV format
def toWav(file_path):
    if file_path.endswith(".m4a"):
        os.system("ffmpeg -i " + '"' + file_path + '"' + " -ab " + RATE + " -f wav -acodec pcm_s16le -loglevel \"quiet\" -y " + '"' + file_path[:-4] + '"' + ".wav")
        if REMOVE_ORIGINAL:
            try:
                os.remove(file_path)
            except:
                pass
        return file_path[:-4] + ".wav"
    else:
        return file_path

# Get a proxy
def get_proxy():
    return requests.get("http://demo.spiderpy.cn/get/?type=https").json()

# Make a request until successful
def getUntillSuccess(URL):
    global PROXY, PROXY_USED_TIMES
    if USE_PROXY:
        if PROXY != "" and PROXY_USED_TIMES <= 10:
            pass
        else:
            PROXY = get_proxy().get("proxy")
            PROXY_USED_TIMES = 0
        while True:
            try:
                PROXY_USED_TIMES += 1
                res = requests.get(URL, headers=HEADERS, proxies={"https": PROXY}).text
                if json.loads(res)["code"] == 0:
                    return res
            except:
                PROXY = get_proxy().get("proxy")
                PROXY_USED_TIMES = 0
    else:
        while True:
            try:
                res = requests.get(URL, headers=HEADERS).text
                try:
                    json.loads(res)["code"]
                except:
                    return res
                if json.loads(res)["code"] == 0:
                    return res
                else:
                    print(Back.RED + "Error: ", res)
                    if json.loads(res)["code"] == -404:
                        print("Skipping")
                        return "[SKIP]"
                    elif json.loads(res)["code"] == 62002:
                        print("Skipping")
                        return "[SKIP]"
                    else:
                        sleep(GLOBAL_SLEEP_TIME)
            except Exception as e:
                print(Back.RED + "Error: ", "网络错误，检查网络环境", "\n", e)
                exit(1)

# Function to download audio
def downloadAudio(URL, local_filename):
    if os.path.exists(local_filename):
        return
    response = requests.get(URL, headers=HEADERS)
    with open(local_filename, 'wb') as f:
        f.write(response.content)

# Main function to download and convert Bilibili video to WAV
def bilibili2wav(URL, output_path, index, page=1):
    # Logic for bilibili2wav
    if URL.find("bv") != -1 or URL.find("BV") != -1 or URL.find("Bv") != -1 or URL.find("bV") != -1 :
        bvid = re.search(r'/BV(\w+)/*', URL , re.IGNORECASE).group(1)
        bvid = "BV" + bvid
        aid = toAid(bvid)
    else:
        aid = re.search(r'/av(\d+)/*', URL , re.IGNORECASE).group(1)

    res_raw = getUntillSuccess("https://api.bilibili.com/x/web-interface/view?aid={aid}".format(aid=aid))
    if res_raw == "[SKIP]":
        return
    res=json.loads(res_raw)
    cidList = res["data"]["pages"]
    for idx,cidArry in enumerate(cidList):
        if cidArry["page"] != page:
            continue
        cid=cidArry["cid"]
        title=cidArry["part"]
        video_api_link="https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&fnval=80"
        video_resp_txt = getUntillSuccess(video_api_link.format(avid=aid,cid=cid))
        video_resp_obj=json.loads(video_resp_txt)
        audio_url=video_resp_obj["data"]["dash"]["audio"][-1]["baseUrl"]
        m4a_path = output_path +'/' + str(index) + ".m4a"
        downloadAudio(audio_url, m4a_path)
        toWav(file_path=m4a_path)

# Main Execution
if __name__ == "__main__":
    bilibili2wav("https://www.bilibili.com/video/BV1ja4y147Wr?p=8","", 2, 8)
