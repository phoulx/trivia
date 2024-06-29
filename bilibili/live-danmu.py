"""
对某一直播间的弹幕进行监听，将弹幕内容写入文件，并将其转为语音播放
"""

import json
import queue
import tempfile
from threading import Thread

from gtts import gTTS
from ws_client import ws
from pydub import AudioSegment
from pydub.playback import play


CONFIG_FILE = 'config.json'

def play_sound(danmu):
    username, danmu_text = danmu[0], danmu[1]
    text = f'{username[0]}说：{danmu_text}'
    tts = gTTS(text, lang='zh-cn')
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
        tts.save(fp.name)
        sound = AudioSegment.from_mp3(fp.name)
        play(sound)


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
                f.write('JSON parse error' + '\n' + item + '\n')

            queue.task_done()


def main():
    with open(CONFIG_FILE) as f:
        config = json.load(f)

    try:
        q = queue.Queue()
        cli = ws.BiliClient(
            roomId = config['roomId'],
            queue = q
        )

        t = Thread(target=process_queue, args=(q,))
        t.start()

        with cli:
            cli.run()

    except Exception as e:
        print("err", e)


if __name__ == '__main__':
    main()