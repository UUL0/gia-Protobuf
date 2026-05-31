import sys
Nx = 0 # 一个变量封装计数

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
    global Nx  # 声明要修改全局变量
    Nstr0 = "                  '06:"
    Ndx0 = 35
    Nstr1 = ":embedded message': \n                    {\n                      '02:00:string': '字库_"
    Ndx1 = 0
    str0="',\n                      '03:01:Varint': 11,\n                      '04:02:embedded message': \n                        {\n                          '01:00:Varint': 10002,\n                          '02:01:Varint': 1,\n                          '04:02:embedded message': \n                            {\n                              '01:00:Varint': 1,\n                              '100:01:embedded message': \n                                {\n                                  '01:00:Varint': 11\n                                }\n\n                            },\n                          '109:03:embedded message': \n                            {\n"
    str1 = "                              '01:"
    str2 = ":embedded message': \n                                {\n                                  '01:00:Varint': 5,\n                                  '02:01:Varint': 1,\n                                  '04:02:embedded message': \n                                    {\n                                      '01:00:Varint': 1,\n                                      '100:01:embedded message': \n                                        {\n                                          '01:00:Varint': 6\n                                        }\n                                    },\n                                  '105:03:embedded message': \n                                    {\n                                      '01:00:string': '"
    str3 = "'\n                                    }\n                                }"

    str4="\n                            }\n                        },\n                      '07:03:Varint': 6,\n                      '08:04:Varint': 6\n                    },\n"
    segments = []
    
    Ct = 0 # 每100条（99）时封装为一个变量
    Cn = 0 # 记录上次的
    LRes = [] # 每100条数据容器
    for i, content in enumerate(content_list):
        index = f"{i:02d}"  # 00, 01, 02...
        cRes = str1 + index + str2 + escape_content(content) + str3

        if i == len(content_list) - 1:  # 最后一条
            LRes.append(cRes + "\n")
        elif Ct == 99:
            LRes.append(cRes + "\n") # 否则是变量的第100条
        else:
            LRes.append(cRes + ",\n")
        Ct += 1
        if Ct > 99: # 100时封装一次
            LRes.insert(0, Nstr0 + f"{Ndx0:02d}" + Nstr1 + str(Ndx1)  + str0)   # 最前面
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