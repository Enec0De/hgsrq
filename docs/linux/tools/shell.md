---
title: 基本语法
---

基本语法 { #basic }
========

简而言之，就是基本操作的简单示例。这是我们的第一个脚本：Hello World!

``` bash title="hello.sh"
--8<-- "shell/hello.sh"
```

---

变量 { #var }
-------------

**直接定义声明**，或通过 `declare` 声明：

-   `+/-`: 取消/设置变量的属性
-   `-f`: 显示函数体
-   `-p`: 显示所有变量
-   `-r`: 只读
-   `-x`: 设置为环境变量，与 `export` 相同
-   `-i`: 整数（integer）

``` bash title="var.sh"
--8<-- "shell/var.sh"
```

当前脚本的系统变量：

-   `$0`: 脚本名
-   `$n`: 第 n 个参数
-   `$*`: 所有参数 `"$*" = "$1 $2 ... $n"`
-   `$@`: 所有参数 `"$@" = "$1" "$2" ... "$n"`
-   `$#`: 所有参数个数
-   `$?`: 返回值
-   `$$`: 进程 PID

---

语句 { #statement }  
-------------------

括号类型：

-   ` ( ... ) `: 在子 shell 中使用命令
-   `(( ... ))`: 数值运算
-   ` [ ... ] `: 等价与 `test`，`...` **前后必须保留空格**
-   `[[ ... ]]`: `bash` 扩展测试
-   ` { ... } `: `...` **前**必须保留空格或换行，`...` **后**必须保留 `;` 或换行

!!! tip

    -   `(( ... ))` 用于循环语句时，固定为三段式 `(( expr1; expr2; expr3 ))`。
    -   `[ ... ]` 和 `[[ ... ]]` 中的比较运算左右必须也要空格。
    -   Bash 中，使用花括号扩展生成序列时，前后不需要括号。花括号扩展先于通配符扩展解析。

关于判断的使用：

<div class="grid cards" markdown>

-   判断逻辑运算符

    ---
    
    - `&&`: 与
    - `||`: 或
    - `!`: 非
    - `-f`: 判断文件
    - `-d`: 判断目录
    
-   以下只能用于整数判断
    
    ---

    - `-eq`: 等于 
    - `-ne`: 不等于
    - `-lt`: 小于
    - `-gt`: 大于
    - `-le`: 小于等于
    - `-ge`: 大于等于

</div>

!!! info

    传统的 `test` 命令中，不支持 `&&`、`||` 的使用，字符串的比较只能用 `=` 和 `!=`。

    在 **Bash** 扩展测试中，支持 `&&`、`||` 的使用，同时可以用 `=~` 正则匹配字符串。

    进行整数判断的时候，更推荐使用数值运算。

语句示例：

``` bash
# if 语句
if `list`; then `list`; fi
if `list`; then `list`; [ elif `list`; then `list`; ] [ else `list`; ] fi 

# for 语句
for var in word ...; do `list`; done
for (( i = 0; i < 10; i++ )); do `list`; done

# while 和 until 语句
while `list`; do `list`; done
until `list`; do `list`; done

# case 语句
case var in  pattern) `list`;; esac
case var in  pattern) `list`;; [ pattern) `list`;; ] esac

# select 语句
PS3=" ... "
select var in word ...; do `list`; done
select var in word ...; do `list` [break] ; done
```

---

函数 { #func }
--------------

[语句][statment]可以构成复合命令（Compound Command），并作为函数体使用：

  [statment]: #statement

``` bash
# 函数的定义
function fname() `compound-command`

# POSIX 标准
fname() `compound-command`

# 函数的使用
fname arg1 arg2 ...
```

推荐用 `{ ... }` 将函数体包裹，明确函数边界，增强可读性。需要隔离环境时可用 `( ... )`。

!!! note "关于 `()`"
    
    默认不将参数传入函数定义时的 `()` 内。

    在 Bash 扩展中，函数的定义可以省略 `()`。在 POSIX 标准中，函数的定义不可以省略 `()`。

!!! warning "定义方式的选择"

    在脚本中，推荐用 POSIX 标准的方式定义和使用函数，保证最大的兼容性。
