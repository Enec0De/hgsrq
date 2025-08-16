#!/usr/bin/env python
# 创建类
class CuteCat:
    def __init__(self, cat_name, cat_age, cat_color):
        self.name = cat_name
        self.age = cat_age
        self.color = cat_color
        self.isking = False

    def miao(self):
        print("miao!" * self.age)

cat_1 = CuteCat("Jojo", 2, "yellow")
print(f"cat's name is: {cat_1.name}")
print(f"cat's age is: {cat_1.age}")
print(f"cat's color is: {cat_1.color}")

cat_1.miao()

# 类的继承，继承了 __init__  方法
class CuteLion(CuteCat):
    def __init__(self, lion_name, lion_age, lion_color):
        super().__init__(lion_name, lion_age, lion_color)
        self.isking = True

    def ao(self):
        print("ao!" * self.age)

    def miao(self):
        print("I am king. I would not miao!")

lion_1 = CuteLion("Dio", 5, "gold")
print(f"lion's name is: {lion_1.name}")
print(f"lion's age is: {lion_1.age}")
print(f"lion's color is: {lion_1.color}")
# 猫！哈哈！

lion_1.ao()
lion_1.miao()
