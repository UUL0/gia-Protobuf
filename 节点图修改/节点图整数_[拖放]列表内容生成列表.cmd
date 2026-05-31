@echo off
echo 正在处理：%1

py 生成节点图整数列表项.py %1 %~n1_节点图整数列表.txt

pause