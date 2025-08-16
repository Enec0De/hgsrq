#!/usr/bin/env python
print("这是一个求平均值的程序。")
total = 0
count = 0
user_char = input("请输入数字进行计算，输入q结束：")
while user_char != "q":
    num = float(user_char)
    total += num
    count += 1
    user_char = input("请输入数字进行计算，输入q结束：")
if count == 0:
    print("平均值为0")
else:
    result = total / count
    print("结果为：" + str(result))
