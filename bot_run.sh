#!/bin/bash

source "$(dirname "$0")/botnv/bin/activate"

cd "$(dirname "$0")"

#TOKEN="6473501966:AAF2ImCU5eM3hbxmVo-1ZFWuDfkMulsicvI"
#ADMINS="639266900,726946648"
export TOKEN="6473501966:AAF2ImCU5eM3hbxmVo-1ZFWuDfkMulsicvI"
export ADMINS="639266900,726946648"
# ADMINS="639266900"
# CHAT_ID="-4098213219"
export CHAT_ID="-1001613873527"

python run.py