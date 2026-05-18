# -*- coding: utf-8 -*-
import sys
import codecs
import struct
import json
import base64

def GetDynamicWireFormat(data, start, end):
    wire_type = data[start] & 0x7
    firstByte = data[start]
    if (firstByte & 0x80) == 0:
        field_number = (firstByte >> 3)
        return (start+1, wire_type, field_number)
    else:
        byteList = []
        pos = 0
        while True:
            if start+pos >= end:
                return (None, None, None)
            oneByte = data[start+pos]
            byteList.append(oneByte & 0x7F)
            pos = pos + 1
            if oneByte & 0x80 == 0x0:
                break;

        newStart = start + pos

        index = len(byteList) - 1
        field_number = 0
        while index >= 0:
            field_number = (field_number << 0x7) + byteList[index]
            index = index - 1

        field_number = (field_number >> 3)
        return (newStart, wire_type, field_number)

def RetrieveInt(data, start, end):
    pos = 0
    byteList = []
    while True:
        if start+pos >= end:
            return (None, None, False)
        oneByte = data[start+pos]
        byteList.append(oneByte & 0x7F)
        pos = pos + 1
        if oneByte & 0x80 == 0x0:
            break

    newStart = start + pos

    index = len(byteList) - 1
    num = 0
    while index >= 0:
        num = (num << 0x7) + byteList[index]
        index = index - 1
    return (num, newStart, True)


def ParseRepeatedField(data, start, end, message, depth = 0):
    while start < end:
        (num, start, success) = RetrieveInt(data, start, end)
        if success == False:
            return False
        message.append(num)
    return True

# 浮点数组解析
def ParseRepeatedFloatField_32_OD1(data, start, end, message, depth=0):
    # 解析 32-bit 浮点数组wire_type=0x05
    while start + 4 <= end:
        if start + 4 > end:  # 失败处理
            return False     # 返回 False
        # 读取 32-bit float
        num = 0
        for i in range(4):
            num = (num << 8) + data[start + i]
        start += 4
        
        try:
            floatNum = struct.unpack('f', struct.pack('I', num))[0]
            message.append(floatNum)
        except:
            return False
    return True

def ParseRepeatedFloatField_32(data, start, end, message, depth=0):
    while start + 4 <= end:
        if start + 4 > end:
            return False
        
        # ⭐⭐⭐ 一步到位（小端序）
        try:
            floatNum = struct.unpack('<f', data[start:start+4])[0]
            message.append(floatNum)
        except:
            return False
        start += 4
    return True

def ParseRepeatedFloatField_32_OD3(data, start, end, message, depth=0):
    while start + 4 <= end:
        if start + 4 > end:
            return False
        
        # ⭐⭐⭐ 反向读取（小端序）
        num = 0
        for i in range(3, -1, -1):  # ⭐ i = 3, 2, 1, 0
            num = (num << 8) + data[start + i]
        
        start += 4
        
        try:
            floatNum = struct.unpack('f', struct.pack('I', num))[0]
            message.append(floatNum)
        except:
            return False
    return True


# V_Type用于变量类型存储，递归回归传值，区分出wire_type 0x02时的repeated判定
# ParseData会逐字判断类型直到结束
# 所以递归回归后会传值作为当前的messages是否有效
# 无效则会删除递归内messages的所有内容
# 也是拦截print的值看起来为什么是有效的，但没有输出
# 得出问题是递归的内容是messages内数据字节，这个内容可能是有效的messages也可能是数据值
# 所以会有概率和messages wire_type一模一样，但messages是无效的不合法的
# 解決了一部分冲突
# 浮点列表被解析为Varint
# 无法解析字典和结构体
# 浮点列表的解析：repeated，后面是长度，每4字节为一个32bit浮点数，无法判断是64bit，但GIA是32bit，足够了

def ParseData(data, start, end, messages, depth = 0,V_Type = None):
    if V_Type is None:
        V_Type = [0]
    CV_Type = 0 # 定义一个关键标记03:01:Varint
    B_Type = 0 # 判断类型执行标记
    BV_Type=0 # 解析标记
    strings = []
    ordinary = 0
    while start < end:
        (start, wire_type, field_number) = GetDynamicWireFormat(data, start, end)
        if start == None:
            return False

        if wire_type == 0x00:
            (num, start, success) = RetrieveInt(data, start, end)
            if success == False:
                return False
            if depth != 0:
                strings.append('\t'*depth)
            strings.append("(%d) Varint: %d\n" % (field_number, num))
            messages['%02d:%02d:Varint' % (field_number,ordinary)] = num

            # 判定当前是否等于'03:01:Varint'，是则改类型
            if field_number == 3 and ordinary == 1:
                V_Type[0] = num
                CV_Type = 1 # 当前层关键标记

            ordinary  = ordinary + 1

        elif wire_type == 0x01:#64-bit
            num = 0
            pos = 7
            while pos >= 0:
                if start+pos >= end:
                    return False
                num = (num << 8) + data[start+pos]
                pos = pos - 1
            start = start + 8
            try:
                floatNum = struct.unpack('d',struct.pack('q',int(hex(num),16)))
                floatNum = floatNum[0]
            except:
                floatNum = None
                
            if depth != 0:
                strings.append('\t'*depth)
            if floatNum != None:
                strings.append("(%d) 64-bit: 0x%x / %f\n" % (field_number, num, floatNum))
                messages['%02d:%02d:64-bit' % (field_number,ordinary)] = floatNum
            else:
                strings.append("(%d) 64-bit: 0x%x\n" % (field_number, num))
                messages['%02d:%02d:64-bit' % (field_number,ordinary)] = num


            ordinary = ordinary + 1

            
        elif wire_type == 0x02:
            curStrIndex = len(strings)
            (stringLen, start, success) = RetrieveInt(data, start, end)

            if success == False:
                return False

            if depth != 0:
                strings.append('\t'*depth)

            strings.append("(%d) embedded message:\n" % field_number)
            messages['%02d:%02d:embedded message' % (field_number, ordinary)] = {}

            if start+stringLen > end:
                del strings[curStrIndex + 1:]
                messages.pop('%02d:%02d:embedded message' % (field_number, ordinary), None)
                return False
            ret = ParseData(data, start, start+stringLen, messages['%02d:%02d:embedded message' % (field_number, ordinary)], depth+1,V_Type)
            # 数据集来看，只有两种类型string和repeated，无论是整数还是bool
            # 但有一个错误，浮点数被按照Varint编码了，同样的，所有数值类型的列表都是被按照Varint编码解码了
            # 需要针对'03:01:Varint'类型进行判定，重写解码编码
            # 整数列表：8，bool列表：9，浮点列表：10

            if ret == False: #返回的如果不是embedded message则删除之前的预存键？
                del strings[curStrIndex + 1:]
                messages.pop('%02d:%02d:embedded message' % (field_number, ordinary), None)

                B_Type = 0 # 判断类型执行标记
                BV_Type=0 # 解析标记
                try:
                    if V_Type[0] == 8 or V_Type[0] == 9: # 整数数组和布尔数组
                        B_Type = 1 # 分支处理标记
                        BV_Type=1 # 解析标记
                        if depth != 0:
                            strings.append('\t'*depth)

                        strings.append("(%d) repeated:\n" % field_number)
                        messages['%02d:%02d:repeated' % (field_number, ordinary)] = []
                        ret = ParseRepeatedField(data, start, start+stringLen, messages['%02d:%02d:repeated' % (field_number, ordinary)], depth+1)
                        if ret == False:
                            B_Type = 0 # 处理失败清标记
                            BV_Type=0 # 解析标记清除
                            del strings[curStrIndex + 1:]     #pop failed result
                            messages.pop('%02d:%02d:repeated' % (field_number, ordinary), None)
                except:
                    B_Type = 0 # 处理失败清标记
                    BV_Type=0 # 解析标记清除

                try:
                    if V_Type[0] == 10: # 浮点数组
                        B_Type = 1 # 分支处理标记
                        BV_Type=1 # 解析标记
                        if depth != 0:
                            strings.append('\t'*depth)

                        strings.append("(%d) repeated32bit:\n" % field_number)
                        messages['%02d:%02d:repeated32bit' % (field_number, ordinary)] = []
                        ret = ParseRepeatedFloatField_32(data, start, start+stringLen, messages['%02d:%02d:repeated32bit' % (field_number, ordinary)], depth+1)
                        if ret == False:
                            B_Type = 0 # 处理失败清标记
                            BV_Type=0 # 解析标记清除
                            del strings[curStrIndex + 1:]     #pop failed result
                            messages.pop('%02d:%02d:repeated32bit' % (field_number, ordinary), None)
                except:
                    B_Type = 0 # 处理失败清标记
                    BV_Type=0 # 解析标记清除
                if B_Type == 0: # 前面都没有执行
                    BV_Type=1 # 解析标记
                    try:
                        if depth != 0:
                            strings.append('\t'*depth)

                        strings.append("(%d) repeated:\n" % field_number)
                        data[start:start+stringLen].decode('utf-8')# .encode('utf-8')
                        strings.append("(%d) string: %s\n" % (field_number, data[start:start+stringLen]))
                        messages['%02d:%02d:string' % (field_number, ordinary)] = data[start:start+stringLen].decode('utf-8')
                    except:
                       if depth != 0:
                           strings.append('\t'*depth)

                       strings.append("(%d) repeated:\n" % field_number)
                       messages['%02d:%02d:repeated' % (field_number, ordinary)] = []
                       ret = ParseRepeatedField(data, start, start+stringLen, messages['%02d:%02d:repeated' % (field_number, ordinary)], depth+1)
                       if ret == False:
                           del strings[curStrIndex + 1:]     #pop failed result
                           messages.pop('%02d:%02d:repeated' % (field_number, ordinary), None)
                           hexStr = ['0x%x' % x for x in data[start:start+stringLen]]
                           hexStr = ':'.join(hexStr)
                           strings.append("(%d) bytes: %s\n" % (field_number, hexStr))
                           messages['%02d:%02d:bytes' % (field_number, ordinary)] = hexStr
 
            ordinary = ordinary + 1
            start = start+stringLen

        elif wire_type == 0x05:
            num = 0
            pos = 3
            while pos >= 0:
                if start+pos >= end:
                    return False
                num = (num << 8) + data[start+pos]
                pos = pos - 1

            start = start + 4
            try:
                floatNum = struct.unpack('f',struct.pack('i',int(hex(num),16)))
                floatNum = floatNum[0]
            except:
                floatNum = None

                
            if depth != 0:
                strings.append('\t'*depth)
            if floatNum != None:
                strings.append("(%d) 32-bit: 0x%x / %f\n" % (field_number, num, floatNum))
                messages['%02d:%02d:32-bit' % (field_number,ordinary)] = floatNum
            else:
                strings.append("(%d) 32-bit: 0x%x\n" % (field_number, num))
                messages['%02d:%02d:32-bit' % (field_number,ordinary)] = num 

            ordinary = ordinary + 1


        else:
            # BV_Type=0 # 如果当前层解析过数据，但不是embedded message则判断为无效的，V_Type[0]的值不作改变
            if CV_Type == 1: # 如果当前层是类型判定层，则重置
                CV_Type = 0
                V_Type[0]=0
            return False
    if BV_Type == 1:
        # BV_Type=0 # 如果当前解析过数据，embedded message有效，则重置解析
        V_Type[0]=0
    if CV_Type == 1: # 如果当前层是类型判定层，则重置
        CV_Type = 0
        V_Type[0]=0
    return True

def ParseProto(fileName):
    data = open(fileName, "rb").read()
    size = len(data)

    messages = {}
    ParseData(data, 0, size, messages,0,[0])

    return messages

def ParseProtoFromBase64(base64_content):
    data = base64.b64decode(base64_content)
    size = len(data)

    messages = {}
    ParseData(data, 0, size, messages,0,[0])

    return messages

def GenValueList(value):
    valueList = []
    while value >= 0:
        oneByte = (value & 0x7F)
        value = (value >> 0x7)
        if value > 0:
            oneByte |= 0x80
        valueList.append(oneByte)
        if value == 0:
            break
    
    return valueList


def WriteValue(value, output):
    byteWritten = 0
    while value >= 0:
        oneByte = (value & 0x7F)
        value = (value >> 0x7)
        if value > 0:
            oneByte |= 0x80
        output.append(oneByte)
        byteWritten += 1
        if value == 0:
            break
    
    return byteWritten

def WriteVarint(field_number, value, output):
    byteWritten = 0
    wireFormat = (field_number << 3) | 0x00
    byteWritten += WriteValue(wireFormat, output)
    while value >= 0:
        oneByte = (value & 0x7F)
        value = (value >> 0x7)
        if value > 0:
            oneByte |= 0x80
        output.append(oneByte)
        byteWritten += 1
        if value == 0:
            break
    
    return byteWritten

def Write64bitFloat(field_number, value, output):
    byteWritten = 0
    wireFormat = (field_number << 3) | 0x01
    byteWritten += WriteValue(wireFormat, output)
    
    # 传入的是bytes？没有.encode？
    # bytesStr = struct.pack('d', value).encode('hex')
    bytesStr = struct.pack('d', value).hex()
    n = 2
    bytesList = [bytesStr[i:i+n] for i in range(0, len(bytesStr), n)]
    for i in range(0,len(bytesList)):
        output.append(int(bytesList[i],16))
        byteWritten += 1

    return byteWritten

def Write64bit(field_number, value, output):
    byteWritten = 0
    wireFormat = (field_number << 3) | 0x01
    byteWritten += WriteValue(wireFormat, output) 
    for i in range(0,8):
        output.append(value & 0xFF)
        value = (value >> 8)
        byteWritten += 1

    return byteWritten

def Write32bitFloat(field_number, value, output):
    byteWritten = 0
    wireFormat = (field_number << 3) | 0x05
    byteWritten += WriteValue(wireFormat, output)
    
    # bytesStr = struct.pack('f', value).encode('hex')
    bytesStr = struct.pack('f', value).hex()
    n = 2
    bytesList = [bytesStr[i:i+n] for i in range(0, len(bytesStr), n)]
    for i in range(0,len(bytesList)):
        output.append(int(bytesList[i],16))
        byteWritten += 1


    return byteWritten

def Write32bit(field_number, value, output):
    byteWritten = 0
    wireFormat = (field_number << 3) | 0x05
    byteWritten += WriteValue(wireFormat, output)
    
    for i in range(0,4):
        output.append(value & 0xFF)
        value = (value >> 8)
        byteWritten += 1

    return byteWritten

def WriteRepeatedField(message, output):
    byteWritten = 0
    for v in message:
        byteWritten += WriteValue(v, output)
    return byteWritten


def Decode(binary):
    messages = {}
    ret = ParseData(binary, 0, len(binary), messages,0,[0])

    if ret == False:
        return False

    return messages


def ReEncode(messages, output):
    byteWritten = 0

    # for key in sorted(messages.iterkeys(), key= lambda x: int(x.split(':')[1])):
    for key in sorted(messages.keys(), key= lambda x: int(x.split(':')[1])):
        keyList = key.split(':')
        field_number = int(keyList[0])
        wire_type = keyList[2]
        value = messages[key]

        if wire_type == 'Varint':
            byteWritten += WriteVarint(field_number, value, output)
        elif wire_type == '32-bit':
            if type(value) == type(float(1.0)):
                byteWritten += Write32bitFloat(field_number, value, output)
            else:
                byteWritten += Write32bit(field_number, value, output)
        elif wire_type == '64-bit':
            if type(value) == type(float(1.0)):
                byteWritten += Write64bitFloat(field_number, value, output)
            elif isinstance(value, bytes):  # ← 新增：处理 bytes 类型
                # 把 bytes 转成 float 再编码
                floatVal = struct.unpack('d', value)[0]
                byteWritten += Write64bitFloat(field_number, floatVal, output)
            else:
                byteWritten += Write64bit(field_number, value, output)
        elif wire_type == 'embedded message':
            wireFormat = (field_number << 3) | 0x02 
            byteWritten += WriteValue(wireFormat, output)
            index = len(output)

            # 打印递归前状态
            # print(f"[ReEncode] 进入递归: field_number={field_number}, 子消息keys={list(messages[key].keys()) if messages[key] else '空'}")

            tmpByteWritten = ReEncode(messages[key], output)

            # 打印递归后结果
            # print(f"[ReEncode] 递归返回: tmpByteWritten={tmpByteWritten}")

            valueList = GenValueList(tmpByteWritten)
            listLen = len(valueList)
            for i in range(0,listLen):
                output.insert(index, valueList[i])
                index += 1
            byteWritten += tmpByteWritten + listLen
        elif wire_type == 'repeated':
            wireFormat = (field_number << 3) | 0x02
            byteWritten += WriteValue(wireFormat, output)
            index = len(output)
            tmpByteWritten = WriteRepeatedField(messages[key], output)
            valueList = GenValueList(tmpByteWritten)
            listLen = len(valueList)
            for i in range(0,listLen):
                output.insert(index, valueList[i])
                index += 1
            byteWritten += tmpByteWritten + listLen

        elif wire_type == 'repeated32bit':
            WireFormat = (field_number << 3) | 0x02
            byteWritten += WriteValue(WireFormat, output) # 写入repeated Tag，字节数++
            index = len(output) # Tag之后的位置
            # 浮点数组：每个 float 用 Write32bitFloat 编码
            for floatVal in messages[key]:
                bytes_data = struct.pack('<f', floatVal)  # 转32bit浮点字节！小端序
                output.extend(bytes_data)  # 追加4字节浮点数

            contentBytes = len(messages[key]) * 4 # Length长度浮点数量 * 4
            lengthBytes = []
            WriteValue(contentBytes, lengthBytes) # 把长度转为Varint编码数值
            output[index:index] = lengthBytes # lengthBytes插入到Tag后
            byteWritten += len(lengthBytes) + contentBytes # 总写入字节计数

        elif wire_type == 'string':
            wireFormat = (field_number << 3) | 0x02 
            byteWritten += WriteValue(wireFormat, output)

            # 可能是还原时导致值编成了其它类型？
            # bytesStr = [int(elem.encode("hex"),16) for elem in messages[key].encode('utf-8')]
            
            # value = messages[key]
            # 判断类型
            if isinstance(value, bytes):
                bytesStr = list(value) 
            elif isinstance(value, str):
                bytesStr = list(value.encode('utf-8'))
            elif isinstance(value, int):
                bytesStr = [int(x) for x in format(value, 'x')]
            else:
                bytesStr =list(str(value).encode('utf-8')) 

            byteWritten += WriteValue(len(bytesStr),output)

            output.extend(bytesStr)
            byteWritten += len(bytesStr)

        elif wire_type == 'bytes':
            wireFormat = (field_number << 3) | 0x02 
            byteWritten += WriteValue(wireFormat, output)

            # 可能是还原时导致值编成了其它类型？
            # bytesStr = [int(byte,16) for byte in messages[key].split(':')]

            # value = messages[key]
            # 判断类型
            if isinstance(value, bytes):
                bytesStr = list(value)
            elif isinstance(value, str):
                bytesStr = list(value.encode('utf-8'))
            elif isinstance(value, int):
                bytesStr = [int(x) for x in format(value, 'x')]
            else:
                bytesStr = list(str(value).encode('utf-8')) 

            byteWritten += WriteValue(len(bytesStr),output)

            output.extend(bytesStr)
            byteWritten += len(bytesStr)

    return byteWritten

   

def SaveModification(messages, fileName):
    output = list()
    ReEncode(messages, output)
    f = open(fileName, 'wb')
    f.write(bytearray(output))
    f.close()
    

