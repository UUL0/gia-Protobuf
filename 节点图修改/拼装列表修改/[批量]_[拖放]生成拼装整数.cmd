@echo off
REM 启用延迟展开？
setlocal enabledelayedexpansion
REM 多文件批处理
REM 拼装ID和内部ID，起始值
set TID=2
set CID1=1
REM 设置基础坐标
set CX=0
set CY=0
REM 坐标增量
set Xstp=500
set Ystp=0

mkdir "拼装整数批量" 2>nul

for %%f in (%*) do (
    echo 正在处理: %%f
    echo 输入ID: !TID! !CID1! !CX! !CY!
    REM py [批量]生成节点拼装整数.py %%f 拼装整数批量\%%~nf_节点拼装整数.txt !TID! !CID1! !CX! !CY!
    REM 读取Python输出，覆盖旧值
    for /f "tokens=1-3 delims=|" %%a in ('py [批量]生成节点拼装整数.py %%f 拼装整数批量\%%~nf_节点拼装整数.txt !TID! !CID1! !CX! !CY! %%~nf') do (
        echo 输出ID: %%a %%b %%c
        set TID=%%a
        set CID1=%%b
        set CX=%%c
    )
    REM 返回的是计算好的ID，这里不自增处理
    REM set /a TID+=1
    REM set /a CID1+=1
    REM 这里坐标需要间隔
    set /a CX+=Xstp
    set /a CY+=Ystp
)


pause