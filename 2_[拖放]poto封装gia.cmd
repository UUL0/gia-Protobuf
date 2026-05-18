@echo off
echo 正在封装：%1

py 合并封装流程.py %1 %~n1_封装.gia

pause