import sys

# 拼装列表生成
# 批量生成、文件名写入注释
# 每个文件生成一个获取节点图变量
# 每个文件生成所有拼接浮点列表以及对应的拼接列表
# 每个文件的拼接列表引脚连线
# 并返回拼接ID与下一个文件拼接列表节点进行连接



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

# 添加：获取节点图变量，排序ID，内部ID，变量名，X，Y浮点坐标
def ADD_获取节点图变量(TID = 0, ID = 0, Name = "", X = 0.0, Y = 0.0):
    # 节点类型ID
    BID1 = 337
    BID2 = 346

    str1="                  '03:"
    # TID
    str2=":embedded message': \n                    {\n                      '01:00:Varint': "
    # ID
    str3=",\n                      '02:01:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    # BID1
    str4="\n                        },\n                      '03:02:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    # BID2
    str5="\n                        },\n                      '04:03:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 5,\n                              '02:01:Varint': 1,\n                              '04:02:embedded message': \n                                {\n                                  '01:00:Varint': 1,\n                                  '100:01:embedded message': \n                                    {\n                                      '01:00:Varint': 6\n                                    }\n                                },\n                              '105:03:embedded message': \n                                {\n                                  '01:00:string': '"
    # Name
    str6="'\n                                }\n                            },\n                          '04:03:Varint': 6\n                        },\n                      '04:04:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 4\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 4\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 9,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 10002,\n                                      '04:01:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 10\n                                            }\n                                        },\n                                      '109:02:embedded message': \n                                        {\n                                        }\n                                    }\n                                }\n                            },\n                          '04:03:Varint': 10\n                        },\n                      '05:05:32-bit': "
    # X
    str7=",\n                      '06:06:32-bit': "
    # Y
    str8="\n                    },\n"
    # return str1+str(f"{TID:02d}")+str2+str(ID)+str3+str(BID1)+str4+str(BID2)+str5+ escape_content(Name) +str6+str(X)+str7+str(Y)+str8

    return f"{str1}{TID:02d}{str2}{ID}{str3}{BID1}{str4}{BID2}{str5}{escape_content(Name)}{str6}{X}{str7}{Y}{str8}"



# 添加：拼接列表，排序ID，内部唯一ID，输出流连接ID，接入目标列表ID，接入列表ID，X，Y坐标
def ADD_拼接列表(TID = 0, ID = 0, P0 = 0, P1 = 0, P2 = 0, X = 0.0, Y = 0.0):
    # 节点类型ID
    BID1 = 100
    BID2 = 104
    
    # 输出流类型？
    CID1 = 2
    CID2 = 2
    # 输入流接入类型？
    DID1 = 1
    DID2 = 1
    # 引脚1接入类型？
    EID1 = 4
    EID2 = 4
    # 引脚2接入类型？
    FID1 = 4
    FID2 = 4
    str1 = "                  '03:"
    # TID
    str2 = ":embedded message': \n                    {\n                      '01:00:Varint': "
    # ID
    str3 = ",\n                      '02:01:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    # BID1
    str4 = "\n                        },\n                      '03:02:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    # BID2
    str5 = "\n                        },\n                      '04:03:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': "
    # CID1 
    str6 = "\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': "
    # CID2 
    str7 = "\n                            },\n                          '05:02:embedded message': \n                            {\n                              '01:00:Varint': "
    # P0
    str8 = ",\n                              '02:01:embedded message': \n                                {\n                                  '01:00:Varint': "
    # DID1
    str9 = "\n                                },\n                              '03:02:embedded message': \n                                {\n                                  '01:00:Varint': "
    # DID2
    str10 = "\n                                }\n                            }\n                        },\n                      '04:04:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 4,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 10002,\n                                      '04:01:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 10\n                                            }\n                                        },\n                                      '109:02:embedded message': \n                                        {\n                                        }\n                                    }\n                                }\n                            },\n                          '04:03:Varint': 10,\n                          '05:04:embedded message': \n                            {\n                              '01:00:Varint': "
    # P1
    str11 = ",\n                              '02:01:embedded message': \n                                {\n                                  '01:00:Varint': "
    # EID1 
    str12 = "\n                                },\n                              '03:02:embedded message': \n                                {\n                                  '01:00:Varint': "
    # EID2 
    str13 = "\n                                }\n                            }\n                        },\n                      '04:05:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 3,\n                              '02:01:Varint': 1\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 3,\n                              '02:01:Varint': 1\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 4,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 10002,\n                                      '04:01:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 10\n                                            }\n                                        },\n                                      '109:02:embedded message': \n                                        {\n                                        }\n                                    }\n                                }\n                            },\n                          '04:03:Varint': 10,\n                          '05:04:embedded message': \n                            {\n                              '01:00:Varint': "
    # P2
    str14 = ",\n                              '02:01:embedded message': \n                                {\n                                  '01:00:Varint': "
    # FID1
    str15 = "\n                                },\n                              '03:02:embedded message': \n                                {\n                                  '01:00:Varint': "
    # FID2
    str16 = "\n                                }\n                            }\n                        },\n                      '05:05:32-bit': "
    # X
    str17 = ",\n                      '06:06:32-bit': "
    # Y
    str18 = "\n                    },\n"

    return f"{str1}{TID:02d}{str2}{ID}{str3}{BID1}{str4}{BID2}{str5}{CID1}{str6}{CID2}{str7}{P0}{str8}{DID1}{str9}{DID2}{str10}{P1}{str11}{EID1}{str12}{EID2}{str13}{P2}{str14}{FID1}{str15}{FID2}{str16}{X}{str17}{Y}{str18}"


# 添加：拼装浮点数列表，浮点数<=100个，排序ID，内部唯一ID，X，Y坐标，注释文本
def ADD_拼装浮点数列表(content_list,TID=0,ID=0,CX=0.0,CY=0.0,ZShi=""):
    # 每个拼装ID起始
    # TID = 2 # 拼装ID起始
    # ID = 1 # 内部唯一索引ID起始

    # 固定不变
    BID1 = 169 # 未知内部ID1
    BID2 = 173 # 未知内部ID2

    # 项ID起始
    AID = 4 # 项的计数号

    IDX = 1 # 拼装列表的项，每一个列表都是1到100，但只有有效数据时才算一个项
    # CX = 0.0 # 列表在节点图中的坐标X，32bit浮点数
    # CY = 0.0 # 列表在节点图中的坐标Y，32bit浮点数
    
    Ln = 0 # 列表项数（无论写入多少，这个不改变就不会显示出来写入的数据（列表长度值））
    
    str00 = "                  '03:"
    str0 = ":embedded message': \n                    {\n                      '01:00:Varint': "
    str1 = ",\n                      '02:01:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    str2 = "\n                        },\n                      '03:02:embedded message': \n                        {\n                          '01:00:Varint': 10001,\n                          '02:01:Varint': 20000,\n                          '03:02:Varint': 22000,\n                          '05:03:Varint': "
    str30 = "\n                        },\n                      '04:03:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 3\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 2,\n                              '02:01:Varint': 1,\n                              '04:02:embedded message': \n                                {\n                                  '01:00:Varint': 1,\n                                  '100:01:embedded message': \n                                    {\n                                      '01:00:Varint': 3\n                                    }\n\n                                },\n                              '102:03:embedded message': \n                                {\n                                  '01:00:Varint': "
    str31 = "\n                                }\n\n                            },\n                          '04:03:Varint': 3\n                        },"
    str3 = ""

    str40 = "\n                      '04:"
    str4 = ""
    str41 = ":embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 3,\n                              '02:01:Varint': "
    str5 = "\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 3,\n                              '02:01:Varint': "
    str60 = "\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 4,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 4,\n                                      '02:01:Varint': 1,\n                                      '04:02:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 5\n                                            }\n                                        },\n                                      '104:03:embedded message': \n                                        {"
    str61 = "\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 4,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 4,\n                                      '04:01:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 5\n                                            }\n                                        },\n                                      '104:02:embedded message': \n                                        {"
    str6 = ""

    str7 = "\n                                          '01:00:32-bit': "
    str8 = "\n                                        }\n\n                                    }\n\n                                }\n\n                            },\n                          '04:03:Varint': 5\n                        },\n"

    str9 = "\n                      '04:104:embedded message': \n                        {\n                          '01:00:embedded message': \n                            {\n                              '01:00:Varint': 4\n                            },\n                          '02:01:embedded message': \n                            {\n                              '01:00:Varint': 4\n                            },\n                          '03:02:embedded message': \n                            {\n                              '01:00:Varint': 10000,\n                              '02:01:Varint': 1,\n                              '110:02:embedded message': \n                                {\n                                  '01:00:Varint': 4,\n                                  '02:01:embedded message': \n                                    {\n                                      '01:00:Varint': 10002,\n                                      '04:01:embedded message': \n                                        {\n                                          '01:00:Varint': 1,\n                                          '100:01:embedded message': \n                                            {\n                                              '01:00:Varint': 10\n                                            }\n                                        },\n                                      '109:02:embedded message': \n                                        {\n                                        }\n                                    }\n                                }\n                            },\n                          '04:03:Varint': 10\n                        },\n"
    str10 = "                      '05:105:32-bit': "
    str11 = ",\n                      '06:106:32-bit': "

    str120 = ",\n                      '07:107:embedded message': \n                        {\n                          '01:00:string': '"
    str121 = "'\n                        }\n                    },\n\n"
    str12 = ""

    str3 = str30 + str(Ln) + str31
    MK0 = str00 + str(f"{TID:02d}") + str0 + str(ID) + str1 + str(BID1) + str2 + str(BID2) + str3 # 拼装列表头部
    # str4 = str40 + str(AID) + str41
    # str6 = str60 # str61是空项时
    # MK1 = str4 + str(IDX) + str5 + str(IDX) + str6 # 项头
    # MK2 = str7 + 值 # 有内容时再加入内容，否则不加入视为列表上限
    MK3 = str8 # 项尾

    str12 = str120 + ZShi + str121
    MK4 = str9 + str10 + str(CX) + str11 + str(CY) + str12 # 拼装列表尾

    segments = [] # 列表存储容器

    # segments.append(MK0) # 写入拼装列表头部
    str6 = str60 # 有数据

    for i, content in enumerate(content_list):
        Ln += 1 # 项计数
        str4 = str40 + str(f"{AID:02d}") + str41
        MK1 = str4 + str(IDX) + str5 + str(IDX) + str6 # 项头
        MK2 = str7 + str(float(content))
        segments.append(MK1 + MK2 + MK3) # 写入拼装列表项
        IDX += 1 # 项ID
        AID += 1 # 项号码
        if IDX > 100: # 
            break

    # 上次++后是100，100也要写入
    str6 = str61 # 项无数据
    while IDX <=100: # 写满100项内容，从上次结束后填为空
        str4 = str40 + str(f"{AID:02d}") + str41
        MK1 = str4 + str(IDX) + str5 + str(IDX) + str6 # 项头
        segments.append(MK1 + MK3) # 写入拼装列表空项
        IDX += 1 # 项ID
        AID += 1 # 项号码

    str3 = str30 + str(Ln) + str31
    MK0 = str00 + str(f"{TID:02d}") + str0 + str(ID) + str1 + str(BID1) + str2 + str(BID2) + str3 # 拼装列表头部
    segments.insert(0,MK0) # 写入拼装头
    segments.append(MK4) # 写入拼装列表尾
    # segments.insert(0, str0)   # 最前面
    # segments.append(str4)      # 最后面

    return segments


# 切分100，逐个生成
def process_files(input_file, output_file,TID=0,ID=0,CX=0.0,CY=0.0,ZShi="",Name = ""):
    # 基础参数
    # TID = 2 # 拼装ID起始
    # ID = 1 # 节点内部ID索引起始
    # CX = 0.0 # 位置X起始
    # CY = 0.0 # 位置Y起始
    
    Xstp = 200.0 # X坐标增量
    Ystp = 0.0 # Y坐标增量

    # 1读取输入文件（保留空行）
    with open(input_file, 'r', encoding='utf-8') as f:
        # 只去掉行尾换行符，保留空行（空行变成空字符串 ''）
        content_list = [line.rstrip('\n') for line in f]
    
    print(f"读取到 {len(content_list)} 条内容（含空行）", file=sys.stderr)
   
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # for i, seg in enumerate(segments):
        #     f.write(seg)
        # 每个文件一个获取节点图变量
        f.write(ADD_获取节点图变量(TID, ID, str(Name), CX-350.0, CY-100.0)) # 节点图变量名使用数值自增
        获取变量ID = ID # 用于连接引脚
        TID += 1 # 顺序ID唯一
        ID += 1 # 唯一ID

        for i in range(0, len(content_list), 100):
            Lpt = content_list[i:i+100] # 分100行
            # 生成数据段

            segments=[]
            segments = ADD_拼装浮点数列表(Lpt,TID,ID,CX,CY,ZShi)
            f.writelines(segments) # 写数据
            TID += 1
            ID += 1
            # stderr输出信息
            print(f"生成 {len(segments)-2} 段数据，输出到：{output_file}", file=sys.stderr)
            # 生成一个拼接列表节点，ID自增，输出流与下一个输出流连接
            # 下一个ID：拼装列表ID=>拼接列表ID，所以是+2
            # 当循环结束，下一个ID：获取节点图变量ID=>拼装列表ID=>拼接列表ID，所以是+3
            if i + 100 >= len(content_list): # 最后一个
                f.write(ADD_拼接列表(TID, ID, ID+3, 获取变量ID, ID-1, CX, CY-300.0))
            else:
                f.write(ADD_拼接列表(TID, ID, ID+2, 获取变量ID, ID-1, CX, CY-300.0))
            TID += 1
            ID += 1
            CX += Xstp
            CY += Ystp


            
            # 连接引脚
    # 向控制台传字符串数值，用于下个文件的ID起点
    # stdout数据输出（CMD for /f 能读到）
    print(str(TID)+"|"+str(ID)+"|"+str(int(CX)))

def main():
    if len(sys.argv) != 9:
        print("用法: python script.py <输入文件> <输出文件> 拼装ID 内部ID X Y 注释 变量名", file=sys.stderr)
        print("示例: python script.py input.txt output.txt 2 1 0.0 0.0 这是注释 节点图变量1", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    TID = int(sys.argv[3])
    ID = int(sys.argv[4])
    CX = float(sys.argv[5])
    CY = float(sys.argv[6])
    ZShi = escape_content(sys.argv[7]) # 合法化注释
    Name = sys.argv[8] # 获取节点图变量的变量名

    process_files(input_file , output_file,TID,ID,CX,CY,ZShi,Name)



# 程序入口
if __name__ == "__main__":
    main()