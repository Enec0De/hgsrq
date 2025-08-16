#!/usr/bin/env python
# r = read, w = write, a = append.
# a 和 w 模式下，文件不存在会创建文件，前者为追加，后者为覆写
with open("./12_file.txt", "w", encoding = "utf-8") as f:
    f.write("This is line 1.\n")
    f.write("This is line 2.\n")
    f.write("THIS IS LINE 3.\n")
    f.write("This is line 4.\n")
    f.write("This is line 5.\n")
    f.write("This is line 6.\n")
    f.write("This is line 7.\n")
    f.write("This is line 8.\n")
    f.write("This is line 9.\n")

r = open("./12_file.txt", "r", encoding = "utf-8")

# readline 按行读，读到结尾返回空字符串
# readlines 读取全部内容，以行为组，返回一个字符串列表
print("以下是 readline 和 readlines ：")
print(r.readline())
print(r.readline())
print(r.readlines())
r.close


r = open("./12_file.txt", "r", encoding = "utf-8")

# read 有指针，会记录读到了哪里
print("以下是 read")
content = r.read(2)
content_r = r.read()
print(content)
print(content_r)
r.close()

with open("./12_file.txt", "w", encoding = "utf-8") as f:
    f.write("This is line 1.\n")
    f.write("This is line 2.\n")
    f.write("This is line 3.")



