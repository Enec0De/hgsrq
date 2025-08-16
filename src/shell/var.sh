#!/usr/bin/env bash
# 声明变量
           MY_VAR="Enana"
declare -i NUM="6"
declare -i WITH_I=NUM+4
           NO_I=NUM+4

# 使用和打印变量属性
echo "My variable is ${MY_VAR}. Following the declare -p."
declare -p MY_VAR NUM 

# 对比和打印变量属性
echo -e "\nDifferent from \`declare -i WITH_I=NUM+4\` and \`NO_I=NUM+4\`:"
declare -p WITH_I NO_I
