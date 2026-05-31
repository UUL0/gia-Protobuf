import sys

# 拼装列表生成
def escape_content(content):
    # 把 content 转为安全的转义格式
    result = []
    for char in content:
        ord_val = ord(char)
        
        # 普通可打印 ASCII（不需要转义）
        if 32 <= ord_val <= 126 and char not in "'\\\"":
            result.append(char)
        # 特殊字符（用 \xXX 格式）
        elif ord_val<32 or 126<ord_val<256 or char in "'\\\"": # 包含转义符或无效字符
            result.append(f"\\x{ord_val:02x}")
        else: # 否则正常输出
            result.append(char)
    
    return ''.join(result)


def generate_segments(content_list):
    CID1 = 33 # 内部唯一索引ID？
    BID1 = 169 # 未知内部ID1
    BID2 = 170 # 未知内部ID2
    AID = 4 # 项的计数号

    IDX = 1 # 拼装列表的项，每一个列表都是1到100，但只有有效数据时才算一个项
    CX = 20.0000000001 # 列表在节点图中的坐标X，32bit浮点数
    CY = 0.0 # 列表在节点图中的坐标Y，32bit浮点数
    
    Ln = 0 # 列表项数（无论写入多少，这个不改变就不会显示出来写入的数据（列表长度值））

    str0 = "                  '03:34:embedded message': \n                    {\n                      '01:00:Varint': "
    str1 = ",\n                      '02:01:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    str2 = "\n                        },\n                      '03:02:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    str30 = "\n                        },\n                      '04:03:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 2,\n                              '02:01:Varint': 1,\n                              '04:02:embedded message': \n                                {\n                                  '01:00:Varint': 1,\n                                  '100:01:embedded message': \n                                    {\n                                      '01:00:Varint': 3\n                                    }\n\n                                },\n                              '102:03:embedded message': \n                                {\n                                  '01:00:Varint': "
    str31 = "\n                                }\n\n                            },\n                          '04:03:Varint': 3\n                        },"
    str3 = ""

    str40 = "\n                      '04:"
    str4 = ""
    str41 = ":embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 3,\n                              '02:01:Varint': "
    str5 = "\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 3,\n                              '02:01:Varint': "
    str60 = "\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 1,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 5,\n                                      '02:01:Varint': 1,\n                                      '04:02:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 6\n                                            }\n\n                                        },\n                                      '105:03:embedded message': \n                                        {"
    str61 = "\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 1,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 5,\n                                      '04:01:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 6\n                                            }\n\n                                        },\n                                      '105:02:embedded message': \n                                        {"
    str6 = ""

    str7 = "\n                                          '01:00:string': '"
    str8 = "\n                                        }\n\n                                    }\n\n                                }\n\n                            },\n                          '04:03:Varint': 6\n                        },"

    str9 = "\n                      '04:104:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 4\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 4\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 1,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 10002,\n                                      '04:01:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 11\n                                            }\n\n                                        },\n                                      '109:02:embedded message': \n                                        {\n                                        }\n\n                                    }\n\n                                }\n\n                            },\n                          '04:03:Varint': 11\n                        },\n"
    str10 = "                      '05:105:32-bit': "
    str11 = ",\n                      '06:106:32-bit': "
    str12 = "\n                    },"

    str3 = str30 + str(Ln) + str31
    MK0 = str0 + str(CID1) + str1 + str(BID1) + str2 + str(BID2) + str3 # 拼装列表头部
    # str4 = str40 + str(AID) + str41
    # str6 = str60 # str61是空项时
    # MK1 = str4 + str(IDX) + str5 + str(IDX) + str6 # 项头
    # MK2 = str7 + 值 + "'"# 有内容时再加入内容，否则不加入视为列表上限
    MK3 = str8 # 项尾
    MK4 = str9 + str10 + str(CX) + str11 + str(CY) + str12 # 拼装列表尾

    segments = [] # 列表存储容器

    # segments.append(MK0) # 写入拼装列表头部
    str6 = str60 # 有数据

    for i, content in enumerate(content_list):
        Ln += 1 # 项计数
        str4 = str40 + str(f"{AID:02d}") + str41
        MK1 = str4 + str(IDX) + str5 + str(IDX) + str6 # 项头
        MK2 = str7 + escape_content(content) + "'"
        segments.append(MK1 + MK2 + MK3) # 写入拼装列表项
        IDX += 1 # 项ID
        AID += 1 # 项号码

    # 上次++后是100，100也要写入
    str6 = str61 # 项无数据
    while IDX <=100: # 写满100项内容，从上次结束后填为空
        str4 = str40 + str(f"{AID:02d}") + str41
        MK1 = str4 + str(IDX) + str5 + str(IDX) + str6 # 项头
        segments.append(MK1 + MK3) # 写入拼装列表空项
        IDX += 1 # 项ID
        AID += 1 # 项号码

    str3 = str30 + str(Ln) + str31
    MK0 = str0 + str(CID1) + str1 + str(BID1) + str2 + str(BID2) + str3 # 拼装列表头部
    segments.insert(0,MK0) # 写入拼装头
    segments.append(MK4) # 写入拼装列表尾
    # segments.insert(0, str0)   # 最前面
    # segments.append(str4)      # 最后面

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