@echo off

call %~dp0.venv\Scripts\activate

cd %~dp0

set TOKEN=6473501966:AAF2ImCU5eM3hbxmVo-1ZFWuDfkMulsicvI
set ADMINS=639266900,726946648
REM set ADMINS=639266900
REM set CHAT_ID=-4098213219
set CHAT_ID=-1001613873527

python run.py

pause