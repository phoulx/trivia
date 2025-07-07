#!/usr/bin/env python3
"""
python3 removing_raw_files.py /path/to/folder -o /path/to/output
将文件夹中的.RAF文件移动到输出文件夹中，如果有对应的JPG文件，则移动JPG文件
"""

import argparse
from pathlib import Path

def extracting(source_path: Path, output_path: Path):
    for file in source_path.iterdir():
        if file.is_dir():
            extracting(file, output_path)
        elif file.suffix == '.RAF':
            jpeg_file = file.with_suffix('.JPG')
            if jpeg_file.exists():
                file = jpeg_file
            # 将file复制到output_path
            output_file = output_path / file.name
            file.replace(output_file)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="图片所在文件夹", type=str)
    parser.add_argument("-o", "--output", help="输出文件夹路径", type=str)
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output) if args.output else Path('.') / (source_path.stem + "_adjusted")
    if not source_path.exists():
        print("source path not exists")
        exit(1)
    output_path.mkdir(exist_ok=True)

    extracting(source_path, output_path)

