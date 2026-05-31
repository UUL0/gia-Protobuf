import sys

Nx = 0 # 一个变量封装计数
# 以输入文件每行为一个字符串项

def generate_segments(content_list):
    global Nx  # 声明要修改全局变量
    N0 = 0 # 项的排序ID起始值

    str0="'01:"
    str1=":string': '"
    str2="'"

    # 项=str0+str(f"{N0:02d}")+str1+content+str2
    segments = []
    
    LRes = [] # 每100条数据容器
    for i, content in enumerate(content_list):
        # f"{Ct:02d}"  # 00, 01, 02...
        segments.append(str0+str(f"{N0:02d}")+str1+content.strip('\n')+str2) # 直接写入项
        if i == len(content_list)-1: # 最后一个元素
            # pass # 跳过
            segments.append("\n")
        else:
            segments.append(",\n")
        N0 +=1 # 项ID
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