#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import os
from pathlib import Path
import chardet

def detect_encoding(file_path):
    """
    检测文件编码
    
    Args:
        file_path: 文件路径
    
    Returns:
        检测到的编码
    """
    with open(file_path, 'rb') as file:
        # 读取文件开头的部分来检测编码
        raw_data = file.read(4096)
        result = chardet.detect(raw_data)
        # 如果检测到的置信度太低,尝试读取更多内容
        if result['confidence'] < 0.9:
            file.seek(0)
            raw_data = file.read()
            result = chardet.detect(raw_data)
        return result['encoding']

def read_csv_file(file_path, encoding):
    """
    读取CSV文件
    
    Args:
        file_path: CSV文件路径
        encoding: 文件编码
    
    Returns:
        包含所有行的列表
    """
    rows = []
    try:
        with open(file_path, 'r', encoding=encoding) as csvfile:
            csvreader = csv.reader(csvfile, delimiter='\t')
            next(csvreader)  # 跳过标题行
            for row in csvreader:
                if len(row) >= 4:
                    rows.append(row)
        return rows
    except UnicodeDecodeError:
        return None

def convert_csv_to_json(csv_file_path, json_file_path):
    """
    将CSV文件转换为JSON格式
    
    Args:
        csv_file_path: CSV文件路径
        json_file_path: 输出JSON文件路径
    """
    # 首先尝试检测编码
    detected_encoding = detect_encoding(csv_file_path)
    print(f"检测到文件编码: {detected_encoding}")
    
    # 尝试使用检测到的编码读取
    rows = read_csv_file(csv_file_path, detected_encoding)
    
    # 如果失败,尝试其他常见编码
    if not rows:
        print("使用检测到的编码读取失败,尝试其他编码...")
        encodings = ['utf-16', 'utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']
        for enc in encodings:
            print(f"尝试使用 {enc} 编码...")
            rows = read_csv_file(csv_file_path, enc)
            if rows:
                print(f"成功使用 {enc} 编码读取文件")
                break
    
    if not rows:
        raise Exception("无法读取CSV文件,请检查文件编码")
    
    # 转换为JSON格式
    stocks = []
    for row in rows:
        stock = {
            "序号": row[0],
            "代码": row[1],
            "名称": row[2],
            "所属行业": row[3]
        }
        stocks.append(stock)
    
    # 创建JSON对象
    json_data = {
        "stocks": stocks
    }
    
    # 写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)
        print(f"成功写入 {len(stocks)} 条记录")

def main():
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    
    # 设置输入输出文件路径
    csv_file = root_dir / "us-stock-market" / "rawdata" / "futu-us-marketlist-output-20250114.csv"
    json_file = root_dir / "us-stock-market" / "rawdata" / "futu-us-marketlist-output-20250114.json"
    
    # 执行转换
    convert_csv_to_json(csv_file, json_file)
    print(f"转换完成: {json_file}")

if __name__ == "__main__":
    main() 