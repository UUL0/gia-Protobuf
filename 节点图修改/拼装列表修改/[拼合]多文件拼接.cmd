@echo off
set "out=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%_多文件拼合.txt"
set "out=%out: =0%"
set "out=%out::=%"

for %%f in (%*) do (
    echo 正在处理: %%f
    type "%%f" >> "%out%"
)

pause
