@echo off
echo 正在处理：%1

py [组]生成节点图字符列表.py %1 %~n1_节点字符串组变量.txt

pause