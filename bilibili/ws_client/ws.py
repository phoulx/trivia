import asyncio
import json

import requests
import websockets

from . import proto


# 基于B站官方demo修改：https://open-live.bilibili.com/document/849b924b-b421-8586-3e5e-765a72ec3840
# 目前仅支持匿名用户，所以用户名无法完全获取，且弹幕可能丢失
# 未来计划支持自定义Cookie登录，以及直播开放平台


class BiliClient:
    def __init__(self, roomId, queue):
        self.roomId = roomId
        self.host = 'https://api.live.bilibili.com'
        self.queue = queue


    # 事件循环
    def run(self):
        loop = asyncio.get_event_loop()
        # 建立连接
        print("[BiliClient] run connect...")
        try:
            websocket = loop.run_until_complete(self.connect())
        except Exception as e:
            print(f"连接失败: {e}")
        print("[BiliClient] connect success")
        tasks = [
            # 读取信息
            asyncio.ensure_future(self.recvLoop(websocket)),
            # 发送心跳
            asyncio.ensure_future(self.heartBeat(websocket)),
        ]
        loop.run_until_complete(asyncio.gather(*tasks))


    # 获取长连信息
    def getWebsocketInfo(self):
        # 开启应用
        url = self.host + f"/xlive/web-room/v1/index/getDanmuInfo?id={self.roomId}"
        # headerMap = self.sign(params)
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        r = requests.get(url, headers=headers)
        content = json.loads(r.content)
        ws_host = content.get('data').get('host_list')[0]
        token = content.get('data').get('token')

        return ws_host, token


    # 发送鉴权信息
    async def auth(self, websocket, authBody):
        req = proto.Proto()
        req.body = authBody
        req.op = 7
        await websocket.send(req.pack())
        buf = await websocket.recv()
        resp = proto.Proto()
        resp.unpack(buf)
        respBody = json.loads(resp.body)
        if respBody["code"] != 0:
            print("auth 失败")
        else:
            print("auth 成功")


    # 发送心跳
    async def heartBeat(self, websocket):
        while True:
            await asyncio.ensure_future(asyncio.sleep(20))
            req = proto.Proto()
            req.op = 2
            await websocket.send(req.pack())


    def danmu_print(self, item):
        # try:
        #     m = json.loads(item)
        #     print(m.get('cmd'))
        #     if m.get('cmd') == 'DANMU_MSG':
        #         print(f"{m['info'][2][1]}: {m['info'][1]}\n")
        # except json.JSONDecodeError:
        #     pass
        pass


    # 读取信息
    async def recvLoop(self, websocket):
        print("[BiliClient] run recv...")
        while True:
            recvBuf = await websocket.recv()
            resp = proto.Proto()
            print("\n\ngetting proto ------>")
            result = resp.unpack(recvBuf)
            if result:
                loop = asyncio.get_running_loop()
                if isinstance(result, list):
                    print(f"result is list of {len(result)} items")
                    for item in result:
                        self.danmu_print(item)
                        await loop.run_in_executor(None, self.queue.put, item)
                else:
                    print("result is single item")
                    self.danmu_print(result)
                    await loop.run_in_executor(None, self.queue.put, result)            


    # 建立连接
    async def connect(self):
        ws_host, token = self.getWebsocketInfo()
        addr = f"wss://{ws_host['host']}:{ws_host['wss_port']}/sub"
        print(addr)
        headers = {
            "User-Agent": "Mozilla/5.0",
        } # 必须带上header，否则仅会收到很少量包

        websocket = await websockets.connect(addr, extra_headers=headers)

        # 鉴权
        authBody = {
            "uid": 0,
            "roomid": self.roomId,
            "protover": 3,
            "platform": "web",
            "type": 2,
            "key": token,
        }
        await self.auth(websocket, json.dumps(authBody))
        return websocket


    def __enter__(self):
        print("[BiliClient] enter")


    def __exit__(self, type, value, trace):
        # 关闭应用
        # headerMap = self.sign(params)
                        #   data=params, verify=False)
        print("[BiliClient] end app success?")

