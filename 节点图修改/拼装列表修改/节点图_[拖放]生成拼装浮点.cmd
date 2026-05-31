@echo off
::启用延迟展开？
setlocal enabledelayedexpansion
::注意此脚本只能处理多个文件每个文件100行内的
::拼装ID和内部ID，起始值
set TID=2
set CID1=1
::设置基础坐标
set CX=0
set CY=0
::坐标增量
set Xstp=500
set Ystp=100


for %%f in (%*) do (
    echo 正在处理: %%f
    echo ID: !TID! !CID1! !CX! !CY!
    py 生成节点图拼装浮点.py %%f %%~nf_节点拼装浮点.txt !TID! !CID1! !CX! !CY! %%~nf
    set /a TID+=1
    set /a CID1+=1
    set /a CX+=Xstp
    set /a CY+=Ystp
)


pause