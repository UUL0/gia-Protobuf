@echo off
REM 生成浮点列表组，每个文件对应一组浮点列表，每组列表用拼接列表引脚连接获取节点变量，并与下一个文件输入流连接

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
REM 获取节点图变量名
set Name=1001

mkdir "拼接浮点列表组" 2>nul

for %%f in (%*) do (
    echo 正在处理: %%f
    echo 输入ID: !TID! !CID1! !CX! !CY!
    REM py [拼接组]多文件拼接浮点列表组.py %%f 拼接浮点列表组\%%~nf_节点浮点拼接组.txt !TID! !CID1! !CX! !CY! %%~nf
    REM 读取Python输出，覆盖旧值
    for /f "tokens=1-3 delims=|" %%a in ('py [拼接组]多文件拼接浮点列表组.py %%f 拼接浮点列表组\%%~nf_节点浮点拼接组.txt !TID! !CID1! !CX! !CY! %%~nf !Name!') do (
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
    set /a Name+=1
)


pause