@echo off
echo 正在处理：%1

py [组]生成节点图整数列表.py %1 %~n1_节点整数组变量.txt

pause