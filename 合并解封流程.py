#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import myProtobuf as pbparser
from typing import Dict


# gia->protobuf->proto message->格式化展开
def main():
    # 1、取gia中protobuf hex
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        print("示例: python script.py input.gia output.proto")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print("解析文件：",input_file)

    print("1、取protobuf hex")
    binary = process_file(input_file)

    if binary:  
        print("2、protobuf反序列化")
        dict =  pbparser.Decode(binary)
    else:
        print("文件错误")
        return 0

    print("3、proto message")

    print("4、输出到文件：",output_file )
    with open(output_file, 'w', encoding='utf-8') as output_file:
        print_dict(dict, 0, output_file)


# 1、取protobuf序列化数据
def process_file(input_file):
    try:
        # 读取原始二进制数据
        with open(input_file, 'rb') as f:
            data = f.read()
        
        # 检查文件大小
        if len(data) < 24:  # 20 + 4
            print(f"❌ 文件太小！需要至少24字节，实际只有 {len(data)} 字节")
            return False
        
        # 丢弃前20字节和后4字节
        trimmed_data = data[20:-4]
         
        print(f"protobufHEX提取完成！")
        print(f"   原始大小: {len(data)} 字节")
        print(f"   输出大小: {len(trimmed_data)} 字节")
        print(f"   丢弃前20字节 + 后4字节")
        
        return trimmed_data
        
    except FileNotFoundError:
        print(f"❌ 文件不存在: {input_file}")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

# 4、格式化proto可读文本
def print_dict(dictionary, indent_level=0, output_file=None):
    output_file.write(' ' * indent_level + '{\n')
    items_list = list(dictionary.items())
    
    for index, (key, value) in enumerate(items_list):
        output_file.write(' ' * (indent_level + 2) + "'" + key + "'" + ': ')
        
        if isinstance(value, dict):
            output_file.write('\n')
            print_dict(value, indent_level + 4, output_file)
        else:
            output_file.write(repr(value))
        
        if index < len(items_list) - 1:
            output_file.write(',\n')
        else:
            output_file.write('\n')
    
    output_file.write(' ' * indent_level + '}\n')


# 程序入口
if __name__ == "__main__":
    main()