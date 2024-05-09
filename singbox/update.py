#!/usr/bin/python3
"""
sing-box切换到指定的配置文件并更新
对某些配置需额外处理
"""

import argparse
import datetime
import json
import logging
import subprocess
from pathlib import Path

import requests


PROFILES_FILE = Path(__file__).parent / 'profiles.json'
DOWNLOAD_DIR = Path('/etc/sing-box/download')
CONFIG_FILE = Path('/etc/sing-box/config.json')

logging.basicConfig(level=logging.INFO)

def download_file(url, destination):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        exit(1)
    else:
        with open(destination, 'wb') as f:
            f.write(response.content)

def restart_service(service_name):
    command = ['systemctl', 'restart', service_name]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error restarting service: {e}")
        exit(1)

def modify(profile, data):
    if profile == 'glados':
        for rr in data['route']['rules']:
            if 'port' in rr and 22 in rr['port']:
                logging.info(rr)
                rr['outbound'] = 'direct'
                break
    return data


def main():
    with open(PROFILES_FILE, 'r') as f:
        PROFILES = json.load(f)
    
    parser = argparse.ArgumentParser(description='singbox切换到指定的配置文件并更新')
    parser.add_argument('profile', choices=PROFILES.keys(), help='配置文件名称')
    args = parser.parse_args()

    profile = args.profile
    url = PROFILES[profile]
    logging.info(f'正在下载 {profile} 配置文件...')

    # 下载配置文件
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    dest = DOWNLOAD_DIR / f'{profile}-{current_datetime}.json'
    download_file(url, dest)

    # 格式校验及处理
    try:
        with open(dest, 'r') as f:
            data = json.load(f)
            data = modify(profile, data)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, ensure_ascii=False)
    except json.JSONDecodeError:
        logging.error('配置文件格式错误')
        exit(1)

    logging.info(f'{profile} 更新完成')

    # 重启
    restart_service('sing-box')

if __name__ == '__main__':
    main()