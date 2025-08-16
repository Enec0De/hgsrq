---
title: 代码块
---

代码块以及内容选项卡 { #code-blocks }
============================================

:octicons-file-code-24: 代码相关的内容。

---

基本用法 { #basic }
-------------------

这里同时使用了两个内容格式：**代码块**和**内容选项卡**。

``` markdown linenums="1" title="Content tabs with code blocks"
=== "Bash"

    ``` bash
    $ printf "%s\n" "Hello world"
    ```

=== "Python"

    ``` python
    >>> print("Hello World")
    ```
```

<div class="result" markdown>

=== "Bash"

    ``` bash
    $ printf "%s\n" "Hello world"
    ```

=== "Python"

    ``` py
    >>> print("Hello World")
    ```

</div>

<span id="anchor" aria-hidden="true"></span>
展示其渲染结果，[效果如上][out]，用如下代码包裹：

  [out]: #basic

``` markdown 
<div class="result" markdown> ... </div>
```

使用标题、行号、高亮：

=== "Title"

    ```` markdown linenums="1" hl_lines="1" title="Code block with title"
    ``` py title="Python"
    ...
    ```
    ````

=== "Line numbers"    

    ```` markdown linenums="1" hl_lines="1" title="Code block with line numbers"
    ``` py linenums="1"
    ...
    ```
    ````

=== "Lines"    

    ```` markdown linenums="1" hl_lines="1 3" title="Code block with highlighted lines"
    ``` py hl_lines="1 3"
    ...
    ```
    ````

=== "Line ranges"    

    ```` markdown linenums="1" hl_lines="1-3" title="Code block with highlighted line range"
    ``` py hl_lines="1-3"
    ...
    ```
    ````

---

嵌入外部文件 { #embedding-external-files } 
------------------------------------------

可执行文件的源代码可以导入，后面的两个冒号紧接数字[^1]，分别代表起始行和结束行[^2]。

[^1]: 两个冒号可选，如果不加冒号则导入整个文件。单个文件和多个文件的这些行为相同。
[^2]: 可以省略其中一个冒号后的数字，省略前者代表从头开始，省略后者代表读到末尾。

<div class="grid" markdown>

```` markdown title="单个文件导入"

``` py
;--8<-- "test.py::6"
;--8<-- "test.py:4:"
;--8<-- "test.py:4:6"
```
````

```` markdown title="多个文件导入"
``` py
;--8<--
test.py
;--8<--
```
````

</div>

!!! tip "提示"
    
    内容表格同样可以与其他内容连用，如[列表元素][list]。

  [list]: lists.md/#list-and-tab

符号 `--8<--` 可以通过添加一个 `;` 的方式转义，文件也可以以同样的方式跳过，如下：

<div class="grid" markdown>

``` markdown
;;--8<--
```

``` markdown
;--8<-- "; skip.md"
```

</div>
