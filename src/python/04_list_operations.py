#!/usr/bin/env python
# 列表用方括号 `[]`，元组用圆括号 `()`
list1 = []
list1.append("第一个数据")
list1.append(2)
list1.remove("第一个数据")
list1.append(4)

print(list1)
print(len(list1))
print(list1[1])

price = [893, 14, 4325, 1024]
max_price = max(price)
print(max_price)
