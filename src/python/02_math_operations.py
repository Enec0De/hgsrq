#!/usr/bin/env python
import math
user_in = input("输个正整数：")
if user_in.isdigit():
    result=math.log2(int(user_in))
    begin = "log以2为底"+str(user_in)+"的对数是："
    print(begin + str(result) )
else:
    print("输入有误！")
    
