@echo off
echo 正在处理：%1

py 合并解封流程.py %1 %~n1_展开.proto

pause