@echo off
echo 正在处理：%1

py 生成节点图拼装字符串.py %1 %~n1_节点图拼装字符.txt

pause