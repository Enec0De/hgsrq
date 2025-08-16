#!/usr/bin/env python
def calculate_sector(central_angle, radius):
    sector_area = central_angle / 360 * 3.14 * radius ** 2
    print(f"该扇形面积为：{sector_area}")
    return sector_area

central_angle = float(input("输入圆心角（单位：度）："))
radius = float(input("输入半径："))

area=calculate_sector(central_angle, radius)

# 函数可以作为高阶函数的参数引入
# 如果函数只使用一次，可以使用匿名函数，匿名函数只能有一个语句/表达式

area_2 = (lambda a, b: a / 360 * 3.14 * b ** 2)(central_angle, radius)

print(f"area = {area}")
print(f"area_2 = {area_2}")
