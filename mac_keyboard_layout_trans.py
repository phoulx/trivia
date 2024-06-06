#!/usr/bin/env python3
"""
macOS layout文件key code转换
从colemak-dh转换为colemak-dh wide，另外符号键有一些自定义
没有用Ukelele，因为其转换后的layout不直接支持常用修饰键映射（如emacs快捷键）
colemak-dh layout下载自：https://github.com/ColemakMods/mod-dh/tree/master/macOS
猜测是基于系统自带的layout文件修改的，但我目前无法找到原始文件
"""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


"""
macOS keycode见手册（Figure 2-10）：
https://developer.apple.com/library/archive/documentation/mac/pdf/MacintoshToolboxEssentials.pdf
下面MAP右边是原键，左边是要改为的键（因为改动的是key code而非output，这样较方便）
"""
KEYCODE_MAP = {
    # 第一行
    0x1E: 0x1A,
    0x18: 0x1C,
    0x1A: 0x19,
    0x1C: 0x1D,
    0x19: 0x1B,
    0x1D: 0x18,
    # 第二行
    0x21: 0x10,
    0x10: 0x20,
    0x20: 0x22,
    0x22: 0x1F,
    0x1F: 0x23,
    0x23: 0x21,
    0x27: 0x1E,
    0x2C: 0x2A,
    # 第三行
    0x2A: 0x04,
    0x04: 0x26,
    0x26: 0x28,
    0x28: 0x25,
    0x25: 0x29,
    0x29: 0x27,
    # 第四行
    0x1B: 0x2D,
    0x2D: 0x2E,
    0x2E: 0x2B,
    0x2B: 0x2F,
    0x2F: 0x2C,
}


def trans_layout(source_path: Path, output_path: Path):
    with open(source_path, 'r', encoding='utf-8') as sourf, \
         open(output_path, 'w', encoding='utf-8') as outf:
        meta_info = sourf.readline()
        meta_info += sourf.readline()
        outf.write(meta_info)
        
        # 部分&#x开头的字符无法解析，所以先替换为其他字符
        xmlstr = sourf.read()
        xmlstr = xmlstr.replace('&#x', 'ooooo')
        root = ET.fromstring(xmlstr)

        root.set("id", "-123") # 尚不明白id的作用
        root.set("name", "Colemak DH Wide")

        for key in root.iter("key"):
            key_code = int(key.attrib["code"], base=10)
            if key_code in KEYCODE_MAP:
                key.attrib["code"] = str(KEYCODE_MAP[key_code])
        xmlstr = ET.tostring(root, encoding='utf-8').decode('utf-8')
        xmlstr = xmlstr.replace('ooooo', '&#x')
        outf.write(xmlstr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="需要进行转换的源layout文件", type=str)
    parser.add_argument("-o", "--output", help="输出文件夹路径", type=str)
    args = parser.parse_args()

    source_path = Path(args.source)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path('.') / (source_path.stem + "_wide" + source_path.suffix)

    trans_layout(source_path, output_path)

    print("finished!")
