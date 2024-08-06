#/usr/bin/bash
echo "- 开始编译"
g++ ./main.cpp -o ./out/main
g++ ./module/log.cpp -o ./out/module/log
# 更多的往这里填
echo "- 编译完毕"
