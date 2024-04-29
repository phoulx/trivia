#!/usr/bin/env python3
"""
批量转换rime形码方案的码表文件（目标文件夹下所有.dict.yaml文件）
从qwerty布局转换为colemak-dh布局（分号未转换）
"""

import argparse
from pathlib import Path

# 仅转换分隔符之後的内容
SPLITTER = '...'

# Colemak-DH ANSI布局，参考：https://colemakmods.github.io/mod-dh/
LAYOUT_MAP = {
    'a': 'a',
    'b': 'z',
    'c': 'd',
    'd': 's',
    'e': 'f',
    'f': 't',
    'g': 'g',
    'h': 'm',
    'i': 'u',
    'j': 'n',
    'k': 'e',
    'l': 'i',
    'm': 'h',
    'n': 'k',
    'o': 'y',
    'p': 'o',
    'q': 'q',
    'r': 'p',
    's': 'r',
    't': 'b',
    'u': 'l',
    'v': 'v',
    'w': 'w',
    'x': 'c',
    'y': 'j',
    'z': 'x',
}

trans_rule = str.maketrans(LAYOUT_MAP)


def trans_dictfile(dict_file: Path, output_path: Path):
    print(f"translating：{dict_file.name}")
    with open(dict_file, 'r', encoding='utf-8') as sourf, \
         open(output_path / dict_file.name, 'w', encoding='utf-8') as outf:
        seen_splitter = False
        for line in sourf:
            new_line = line.translate(trans_rule) if seen_splitter else line
            outf.write(new_line)
            if not seen_splitter:
                seen_splitter = SPLITTER in line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="需要进行转换的源文件夹路径", type=str)
    parser.add_argument("-o", "--output", help="输出文件夹路径", type=str)
    args = parser.parse_args()

    source_path = Path(args.source)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path('.') / source_path.name
    Path.mkdir(output_path, parents=True, exist_ok=True)

    for file in source_path.iterdir():
        if file.name.endswith('.dict.yaml'):
            trans_dictfile(file, output_path)

    print("finished!")
