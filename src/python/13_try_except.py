#!/usr/bin/env python
def my_calculator(x):
    return x-1

try:
    user_input = float(input("输入一个数字："))
    result = my_calculator(user_input) + 1
except ValueError:
    print("输入错误，请输入数字！")
except:
    print("发生未知错误！")
else:
    print("你输入的数字为：" + str(result))
finally:
    print("结果应为你输入的数字。")

