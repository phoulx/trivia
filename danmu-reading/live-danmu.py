"""
对某一直播间的弹幕进行监听，将弹幕内容写入文件，并将其转为语音播放
"""

import asyncio
import json
import logging
import queue
import tempfile
from threading import Thread

from pydub import AudioSegment
from pydub.playback import play
from bilibili import ws
from xunfei import tts

# 初始化日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_FILE = 'config.json'

def load_config():
    """加载配置文件"""
    with open(CONFIG_FILE) as f:
        return json.load(f)

def play_sound(danmu):
    username, danmu_text = danmu
    text = f'{username[0]}说：{danmu_text}'
    config = load_config()
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
            xunfei_tts = tts.TTSClient(
                APIAuthInfo=config['xunfei'],
                Text=text,
                filename=fp.name
            )
            asyncio.run(xunfei_tts.work())
            sound = AudioSegment.from_mp3(fp.name)
            play(sound)
    except Exception as e:
        logging.error(f'播放失败：{e.__class__.__name__}, 信息：{e}')

def process_queue(queue):
    with open('../tmp/messages.txt', 'w', buffering=1) as f:
        while True:
            item = queue.get()
            try:
                m = json.loads(item)
                if m.get('cmd') == 'DANMU_MSG':
                    danmu = (m['info'][2][1], m['info'][1])
                    f.write(str(danmu) + '\n')
                    f.write(item + '\n')
                    play_sound(danmu)
            except json.JSONDecodeError:
                logging.error('JSON解析错误')
                f.write('JSON parse error' + '\n' + item + '\n')
            except Exception as e:
                logging.error(f"处理弹幕时发生错误: {e}")
                f.write("处理弹幕时发生错误: {e}" + '\n' + item + '\n')
            # finally:
            #     queue.task_done()


def main():
    config = load_config()
    q = queue.Queue()
    cli = ws.BiliClient(
        roomId = config['roomId'],
        queue = q
    )
    t = Thread(target=process_queue, args=(q,))
    t.start()

    try:
        with cli:
            cli.run()

    except Exception as e:
        logging.error(f"主程序错误: {e}")


if __name__ == '__main__':
    main()