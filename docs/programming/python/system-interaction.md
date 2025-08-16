---
title: 操作系统小玩具
---

操作系统小玩具
==============

---

主程序部分
----------

``` py title="hello.py"
--8<-- "python/mini_os/hello.py"
```

``` py title="proc.py"
--8<-- "python/mini_os/proc.py"
```

=== "Without Comments"    
    ``` py linenums="1"
    --8<-- "python/mini_os/os-model-without-comments.py"
    ```

=== "With comments"
    ``` py linenums="1"
    --8<-- "python/mini_os/os-model.py"
    ```

---

对程序的思考
------------

OS 对象：

- `OS.procs` 是一个对象
- `OS.buffer` 是一个空字符串
- `OS.run()` 是一个方法，匹配 `OS.procs` 中任意一个对象的 `OS.procs.step()` 方法返回值

Process 对象（也就是 `OS.procs` ）：

- `Process._func` 是一个生成器
- `Process.retval` 是返回值
- `Process.step()` 是一个方法，传送 `Process.retval` 参数的值后，重置 `Process.retval`
  参数，并返回 `yield` 后的 `sycall` 和 `args`。

!!! tip
 
    对于函数生成器 `gen`，首次 `send()` 必须是 `send(None)` 或 `next(gen)`


参数 `src` 被修改为以下内容后导入：

``` py
def Process(name):
    for _ in range(5):
        yield "write", (name)

def main():
    yield "spawn", (Process, 'A')
    yield "spawn", (Process, 'B')
```

``` py
def main():
    x = 0
    for _ in range(10):
        b = yield "read", ()
        x = x * 2 + b

    yield "write", (f'x = {x:010b}b')

```

