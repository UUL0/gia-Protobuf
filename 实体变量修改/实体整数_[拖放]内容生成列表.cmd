@echo off
echo 正在处理：%1

py 生成实体整数列表.py %1 %~n1_实体列表整数组.txt

pause