import sys

Nx = 0 # 一个变量封装计数
# 以输入文件每行为一个列表变量
# 格式：变量名：列表数组内容
# 52：[62, 64]

def ShuZhuFS(str0): # 处理整数数组中的负数值
    arr = []
    arr.append("[")
    items=str0.strip('\n').strip('[]').split(',')
    for i,x in enumerate(items):
        n=int(x.strip())
        if n < 0:
            arr.append(str(n & 0xFFFFFFFFFFFFFFFF))
        else:
            arr.append(str(n))
        if i == len(items)-1: # 最后一个元素
            pass # 跳过
        else:
            arr.append(", ")
    arr.append("]")
    return "".join(arr)

def generate_segments(content_list):
    global Nx  # 声明要修改全局变量
    N0 = 14 # 变量的排序ID起始值

    str0="                      '01:"
    str1=":embedded message': \n                        {\n                          '02:00:string': '"
    str2="',\n                          '03:01:Varint': 8,\n                          '04:02:embedded message': \n                            {\n                              '01:00:Varint': 8,\n                              '02:01:embedded message': \n                                {\n                                  '01:00:Varint': 8,\n                                  '02:01:embedded message': \n                                    {\n                                    }\n\n                                },\n                              '18:02:embedded message': \n                                {"
    str3="\n                                  '01:00:repeated': "
    str4="\n                                }\n\n                            },\n                          '05:03:Varint': 1,\n                          '06:04:embedded message': \n                            {\n                              '01:00:Varint': 8,\n                              '02:01:embedded message': \n                                {\n                                }\n\n                            }\n\n                        },\n"
    str5=""
    # 变量=str0+N0+str1+名+str2+str3+ShuZhuFS(数组内容)+ str4
    segments = []
    
    LRes = [] # 每100条数据容器
    for i, content in enumerate(content_list):
        # f"{Ct:02d}"  # 00, 01, 02...
        instr1=""
        instr2=""
        instr1, instr2 = content.split('：', 1) # 分割第一个冒号两边数据
        segments.append(str0+str(f"{N0:02d}")+str1+instr1+str2+str3+ShuZhuFS(instr2)+ str4) # 直接写入一个变量
        N0 +=1 # 变量ID
        Nx +=1 # 变量计数
        # LRes.insert(0, "")   # 最前面
        # LRes.append("")      # 最后面
        # segments.append([]) # 直接追加，但是嵌套
        # segments.extend([]) # +=，展开拼接

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