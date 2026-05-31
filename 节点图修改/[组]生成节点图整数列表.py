import sys
Nx = 0 # 一个变量封装计数

def generate_segments(content_list):
    global Nx  # 声明要修改全局变量
    Nstr0 = "                  '06:"
    Ndx0 = 30
    Nstr1 = ":embedded message': \n                    {\n                      '02:00:string': '拼接字段长度_"
    Ndx1 = 0
    str0="',\n                      '03:01:Varint': 8,\n                      '04:02:embedded message': \n                        {\n                          '01:00:Varint': 10002,\n                          '02:01:Varint': 1,\n                          '04:02:embedded message': \n                            {\n                              '01:00:Varint': 1,\n                              '100:01:embedded message': \n                                {\n                                  '01:00:Varint': 8\n                                }\n\n                            },\n                          '109:03:embedded message': \n                            {\n"
    str1 = "                              '01:"
    str2 = ":embedded message': \n                                {\n                                  '01:00:Varint': 2,\n                                  '02:01:Varint': 1,\n                                  '04:02:embedded message': \n                                    {\n                                      '01:00:Varint': 1,\n                                      '100:01:embedded message': \n                                        {\n                                          '01:00:Varint': 3\n                                        }\n                                    },\n                                  '102:03:embedded message': \n                                    {\n                                      '01:00:Varint': "
    str3 = "\n                                    }\n                                }"

    str4="\n                            }\n                        },\n                      '07:03:Varint': 6,\n                      '08:04:Varint': 6\n                    },\n"
    segments = []
    
    Ct = 0 # 每100条（99）时封装为一个变量
    LRes = [] # 每100条数据容器
    for i, content in enumerate(content_list):
        index = f"{Ct:02d}"  # 00, 01, 02...
        n = int(content) # 整数字符串转整数
        if n < 0:
            result = n & 0xFFFFFFFFFFFFFFFF          # 64位无符号解释
            cRes = str1 + index + str2 + str(result) + str3
        else:
            cRes = str1 + index + str2 + content + str3

        if i == len(content_list) - 1:  # 最后一条
            LRes.append(cRes + "\n")
        elif Ct == 99:
            LRes.append(cRes + "\n") # 否则是变量的第100条
        else:
            LRes.append(cRes + ",\n")
        Ct += 1
        if Ct > 99: # 100时封装一次

            LRes.insert(0, Nstr0 + f"{Ndx0:02d}" + Nstr1 + str(Ndx1) + str0)   # 最前面
            LRes.append(str4)      # 最后面
            # segments.append(LRes) # 直接追加，但是嵌套
            segments.extend(LRes) # +=，展开拼接
            LRes = [] # 清空列表
            Ct = 0 
            Ndx0 += 1 # 变量号++
            Ndx1 += 1 # 变量名++
            Nx += 1

    if Ct !=0: # 如果上次循环没有到100条数据
        LRes.insert(0, Nstr0 + f"{Ndx0:02d}" + Nstr1 + str(Ndx1) + str0)   # 最前面
        LRes.append(str4)      # 最后面
        # segments.append(LRes) # 直接追加，但是嵌套
        segments.extend(LRes) # +=，展开拼接
        LRes = [] # 清空列表
        Ct = 0 
        Ndx0 += 1 # 变量号++
        Ndx1 += 1 # 变量名++
        Nx += 1

    return segments


def process_files(input_file, output_file):
    # 1读取输入文件（保留空行）
    with open(input_file, 'r', encoding='utf-8') as f:
        content_list = [line for line in f] # 每行数据
    
    print(f"读取到 {len(content_list)} 条内容（含空行）")
    
    # 生成数据段
    segments = generate_segments(content_list)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments):
            f.write(seg)
            # f.write('\n\n')  # 每段之间加空行分隔
    
    print(f"生成 {Nx} 个列表变量，输出到：{output_file}")


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