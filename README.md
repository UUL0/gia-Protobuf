# gia-Protobuf
基于Protobuf的千星GIA实体变量解析
-
---------------核心myProtobuf.py
————从protobuf二进制文件解码：ParseProto
————从base64编码的protobuf二进制数据解码：ParseProtoFromBase64
————protobuf二进制解码：Decode

————编码核心：ReEncode
修改未知错误（可能是版本）
使字节流判断逻辑能正确解析文本、字节、数值类型

————解码核心：ParseData

---------------一键解/编码
-
安装Python 3.14.5
-

1_[拖放]gia反序列proto.cmd
-
（按标准修改proto可读文本格式后）

2_[拖放]poto封装gia.cmd
-
---------------解码说明
-
此方案只用于protobuf的反序列化，不一定适用于GIA文件
-
只是把protobuf二进制数据进行解析为可读的proto格式文本
GIA版本6.5，封装文件头/文件尾请手动修改，在合 并封装流程.py 文件里，文件头/文件尾需用hex编辑器打开原文件查看

根据现有6.5版本GIA数据，修改解析数组时的逻辑，使其输出是正确的string或repeated
基于数据内变量类型关键修改repeated类型的解/编码逻辑

字典、结构体没有做完整数据解析，嵌套很多，数据类型没有正确显示，虽然能正常解编码，但不建议用，修改很复杂


基于此代码修改：
-
https://blog.csdn.net/qq_35921430/article/details/141998502

