import requests
import logging
from pathlib import Path

DIR = Path(__file__).resolve().parent

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
    filename=DIR / 'app.log',  # 设置日志文件名
    filemode='a'  # 设置日志文件写入模式
)

def live_checkin():
    CHECKIN_URL = 'https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign'

    with open(DIR / 'cookie.txt', 'r') as f:
        cookie_string = f.read()
    headers = {
        'Cookie': cookie_string,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
        }
    r = requests.get(CHECKIN_URL, headers=headers)

    logging.info(r.text)

if __name__ == '__main__':
    live_checkin()