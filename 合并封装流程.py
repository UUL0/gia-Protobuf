import sys
import myProtobuf as pbparser
from typing import Dict
import struct
import ast

def main():
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        print("示例: python script.py input.proto output.gia")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print("1、读取proto文本")
    with open(input_file , "r", encoding="utf-8") as f:  
        # dict = eval(f.read()) # '\'遇到这种字符时会错误
        dict =ast.literal_eval(f.read())

    print("2、转为protobuf hex")
    output = list()
    pbparser.ReEncode(dict, output)

    print("3、封装 protobuf")

    hex_data = bytearray(output)

    data_size = len(hex_data)
    header_size = 20  # 5段 × 4字节
    
    # ===== 2. 封装文件头 =====
    header = struct.pack('>IIIII',
                        header_size + data_size,  # 第1段：头大小+数据大小
                        0x00000001,               # 第2段
                        0x00000326,               # 第3段
                        0x00000003,               # 第4段
                        data_size)                # 第5段：数据大小
    # ===== 3. 封装文件尾 =====
    footer = struct.pack('>I', 0x00000679)
    # ===== 4. 拼接并输出 =====
    result = header + hex_data + footer
    
    with open(output_file, 'wb') as f:
        f.write(result)
    print(f"-------封装完成！-------")
    print(f"   原始数据: {data_size} 字节")
    print(f"   文件头:   {header_size} 字节")
    print(f"   文件尾:   4 字节")
    print(f"   输出大小:   {len(result)} 字节")
    print(f"   输出到:   {output_file}")


# 程序入口
if __name__ == "__main__":
    main()