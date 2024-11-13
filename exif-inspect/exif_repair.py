#!/usr/bin/env python3
"""
部分旧三星手机拍的照片，导入到苹果设备的Photos中，按时间排序，这些照片没有在正确的位置
原因是exif中的拍摄时间格式不规范，如"2019-12-31 23:59:59"，应为"2019:12:31 23:59:59"
此脚本用于批量修改这类照片的exif信息
"""

import argparse
from pathlib import Path
from exif import Image

# 可能格式不规范的手机型号（其实是同一个手机5660，不知道为什么exif中有不一样的）
models = {'GT-S5570', 'GT-S5660', 'GT-S5830'}
valid_suffix = {'.jpg', '.jpeg', '.JPG', '.JPEG'}
attrs = ['datetime_original', 'datetime_digitized', 'datetime']

valid_len = len('2011-10-22 02:24:33')
counter = 0

def do_modification(source_path: Path, output_path: Path):
    global counter
    for file in source_path.iterdir():
        if file.is_file() and file.suffix in valid_suffix:
            with open(file, 'rb') as f:
                img = Image(f)
                if not img.has_exif:
                    print(f"{file.name}: No exif data in file")
                    continue
                if img.get('Model') not in models:
                    continue

                for attr in attrs:
                    if v := img.get(attr):
                        img.set(attr, v.rstrip().replace('-', ':'))
                output_file = output_path / img.get('Model') / file.name
                with open(output_file, 'wb') as f:
                    f.write(img.get_file())
                counter += 1
        elif file.is_dir():
            do_modification(file, output_path)
        else:
            print(f"{file.name}: Not support file type")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="图片所在文件夹", type=str)
    parser.add_argument("-o", "--output", help="输出文件夹路径", type=str)
    args = parser.parse_args()

    source_path = Path(args.source)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path('.') / (source_path.stem + "_adjusted")

    
    if not source_path.exists():
        print("source path not exists")
        exit(1)
        
    output_path.mkdir(exist_ok=True)
    for m in models:
        (output_path / m).mkdir(exist_ok=True)


    do_modification(source_path, output_path)

    print(f"finished! total modified: {counter}")
