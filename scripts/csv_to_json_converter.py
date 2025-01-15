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
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def convert_csv_to_json(csv_file_path, json_file_path):
    """
    将CSV文件转换为JSON格式
    
    Args:
        csv_file_path: CSV文件路径
        json_file_path: 输出JSON文件路径
    """
    # 检测文件编码
    encoding = detect_encoding(csv_file_path)
    print(f"检测到文件编码: {encoding}")
    
    # 读取CSV文件
    stocks = []
    try:
        with open(csv_file_path, 'r', encoding=encoding) as csvfile:
            # 使用tab作为分隔符
            csvreader = csv.reader(csvfile, delimiter='\t')
            # 跳过标题行
            next(csvreader)
            
            # 读取每一行数据
            for row in csvreader:
                if len(row) >= 4:  # 确保行有足够的列
                    stock = {
                        "序号": row[0],
                        "代码": row[1],
                        "名称": row[2],
                        "所属行业": row[3]
                    }
                    stocks.append(stock)
    except UnicodeDecodeError as e:
        print(f"编码错误: {e}")
        print("尝试使用其他编码...")
        # 尝试其他常见编码
        for enc in ['gbk', 'gb2312', 'gb18030', 'big5']:
            try:
                with open(csv_file_path, 'r', encoding=enc) as csvfile:
                    csvreader = csv.reader(csvfile, delimiter='\t')
                    next(csvreader)
                    for row in csvreader:
                        if len(row) >= 4:
                            stock = {
                                "序号": row[0],
                                "代码": row[1],
                                "名称": row[2],
                                "所属行业": row[3]
                            }
                            stocks.append(stock)
                print(f"成功使用 {enc} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue
    
    if not stocks:
        raise Exception("无法读取CSV文件,请检查文件编码")
    
    # 创建JSON对象
    json_data = {
        "stocks": stocks
    }
    
    # 写入JSON文件
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, ensure_ascii=False, indent=2)

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