import sys

def generate_segments(content_list):
    Ndx0 = 0
    Ndx1 = 0
    Nstr0 = ""
    Nstr1 = ""
    str0="                  '06:55:embedded message': \n                    {\n                      '02:00:string': '整数列表_1',\n                      '03:01:Varint': 8,\n                      '04:02:embedded message': \n                        {\n                          '01:00:Varint': 10002,\n                          '02:01:Varint': 1,\n                          '04:02:embedded message': \n                            {\n                              '01:00:Varint': 1,\n                              '100:01:embedded message': \n                                {\n                                  '01:00:Varint': 8\n                                }\n\n                            },\n                          '109:03:embedded message': \n                            {\n"
    str1 = "                              '01:"
    str2 = ":embedded message': \n                                {\n                                  '01:00:Varint': 2,\n                                  '02:01:Varint': 1,\n                                  '04:02:embedded message': \n                                    {\n                                      '01:00:Varint': 1,\n                                      '100:01:embedded message': \n                                        {\n                                          '01:00:Varint': 3\n                                        }\n                                    },\n                                  '102:03:embedded message': \n                                    {\n                                      '01:00:Varint': "
    str3 = "\n                                    }\n                                }"

    str4="\n                            }\n                        },\n                      '07:03:Varint': 6,\n                      '08:04:Varint': 6\n                    },"
    segments = []
    
    for i, content in enumerate(content_list):
        index = f"{i:02d}"  # 00, 01, 02...
        n = int(content) # 整数字符串转整数
        if n < 0:
            result = n & 0xFFFFFFFFFFFFFFFF          # 64位无符号解释
            segment = str1 + index + str2 + str(result) + str3
        else:
            segment = str1 + index + str2 + content + str3
        if i == len(content_list) - 1:  # 最后一条
            segments.append(segment + "\n")
        else:
            segments.append(segment + ",\n")

    segments.insert(0, str0)   # 最前面
    segments.append(str4)      # 最后面

    return segments


def process_files(input_file, output_file):
    # 1读取输入文件（保留空行）
    with open(input_file, 'r', encoding='utf-8') as f:
        # 只去掉行尾换行符，保留空行（空行变成空字符串 ''）
        content_list = [line.rstrip('\n') for line in f]
    
    print(f"读取到 {len(content_list)} 条内容（含空行）")
    
    # 生成数据段
    segments = generate_segments(content_list)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments):
            f.write(seg)
            # f.write('\n\n')  # 每段之间加空行分隔
    
    print(f"生成 {len(segments)-2} 段数据，输出到：{output_file}")


def main():
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        print("示例: python script.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_files(input_file , output_file )



# 程序入口
if __name__ == "__main__":
    main()