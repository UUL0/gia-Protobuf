@echo off
echo 正在处理：%1

py 生成字符串项.py %1 %~n1_实体字符项.txt

pause