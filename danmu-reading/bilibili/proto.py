import struct

import brotli


class Proto:
    def __init__(self):
        self.packetLen = 0
        self.headerLen = 16
        self.ver = 0
        self.op = 0
        self.seq = 0
        self.body = ''
        self.maxBody = 20480 # demo中原来是2048

    def pack(self):
        self.packetLen = len(self.body) + self.headerLen
        buf = struct.pack('>i', self.packetLen)
        buf += struct.pack('>h', self.headerLen)
        buf += struct.pack('>h', self.ver)
        buf += struct.pack('>i', self.op)
        buf += struct.pack('>i', self.seq)
        buf += self.body.encode()
        return buf

    def unpack(self, buf):
        if len(buf) < self.headerLen:
            print("包头不够")
            return
        self.packetLen = struct.unpack('>i', buf[0:4])[0]
        self.headerLen = struct.unpack('>h', buf[4:6])[0]
        self.ver = struct.unpack('>h', buf[6:8])[0]
        self.op = struct.unpack('>i', buf[8:12])[0]
        self.seq = struct.unpack('>i', buf[12:16])[0]
        if self.packetLen < 0 or self.packetLen > self.maxBody:
            print("包体长不对", "self.packetLen:", self.packetLen,
                  " self.maxBody:", self.maxBody)
            return
        if self.headerLen != 16:
            print("包头长度不对")
            return
        bodyLen = self.packetLen - self.headerLen
        self.body = buf[16:self.packetLen]
        if bodyLen <= 0:
            return
        if self.ver == 0:
            # 直接decode
            return self.body.decode('utf-8')
        elif self.ver == 3:
            # brotli解压，结果需再分割
            data = brotli.decompress(self.body)
            res = []
            while(len(data) > 0):
                firstLen = struct.unpack('>i', data[0:4])[0]
                firstBuf = data[:firstLen]
                res.append(self.unpack(firstBuf))
                data = data[firstLen:]
            return res
        else:
            print("未知的数据格式")
            return
