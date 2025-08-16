---
title: 网格
---

网格 { #grid }
==============

:octicons-inbox-24: 使用带有 `grid` 类的 `div` 标签包裹一组区块，可以将任意区块元素排列成网格布局。

---

!!! info "提示"

    列表语法是卡片网格的快捷写法。

列表语法 {grid-cards}
---------------------

有两种写法：

=== ":octicons-file-code-16: `Card Grid`"
    ``` html linenums="1"
    <div class="grid cards" markdown>
    
    -   :fontawesome-brands-linux: **Linux** for me
    -   :fontawesome-brands-markdown: **Markdown** for this draft
    -   :fontawesome-brands-bilibili: **Bilibili** for animate
    -   :fontawesome-brands-python: **Python** for math
    
    </div>
    ```
    
=== ":octicons-file-code-16: `Generic Grid`"
    ``` html linenums="1"
    <div class="grid" markdown>
    
    :fontawesome-brands-linux: **Linux** for me
    { .card }
    
    :fontawesome-brands-markdown: **Markdown** for this draft
    { .card }
    
    :fontawesome-brands-bilibili: **Bilibili** for animate
    { .card }
    
    :fontawesome-brands-python: **Python** for math
    { .card }
    
    </div>
    ```

<div class="grid" markdown>

:fontawesome-brands-linux: **Linux** for me
{ .card }

:fontawesome-brands-markdown: **Markdown** for this draft
{ .card }

:fontawesome-brands-bilibili: **Bilibili** for animate
{ .card }

:fontawesome-brands-python: **Python** for math
{ .card }

</div>

!!! note "注意"

    两种写法等价，后者多用于组合不同类型的块。尽量不使用带有 `result` 类的 `div` 标签包裹网格元素。

每个卡片的内容可以不止一行：

``` html linenums="1"
<div class="grid cards" markdown>

-   :fontawesome-brands-linux: **Linux** for me
   
    ---
   
    [:octicons-arrow-right-24: Learn More](https://www.kernel.org/)

-   :fontawesome-brands-python: **Python** for math

    ---

    [:octicons-arrow-right-24: Learn More](https://www.python.org/)

</div>
```

<div class="grid cards" markdown>

-   :fontawesome-brands-linux: **Linux** for me
   
    ---
   
    [:octicons-arrow-right-24: Learn More](https://www.kernel.org/)

-   :fontawesome-brands-python: **Python** for math

    ---

    [:octicons-arrow-right-24: Learn More](https://www.python.org/)

</div>

---

通用网格 { #generic-grd }
-------------------------

```` html linenums="1"
<div class="grid" markdown>

**这是卡片内容块** 
{ .card }

> **这是引用内容块** 

=== ":octicons-file-code-16: `Content tab`"

    这是内容选项卡.

``` title="Code block"
这是代码块.
```

</div>
````

<div class="grid" markdown>

**这是卡片内容块** 
{ .card }

> **这是引用内容块** 

=== ":octicons-file-code-16: `Content tab`"

    这是内容选项卡.

``` title="Code block"
这是代码块.
```

</div>

!!! note "注意"

    尽量避免多层、不同块的嵌套[^1]。

[^1]: 过多层的嵌套容易导致无意义的复杂化，建议拆分。

!!! warning "警告"

    我们约定，通用网格内只使用：卡片、引用、代码块、内容选项卡。
    
*[卡片]: 非列表语法下 { .card } 结尾的块
*[引用]: 一个或多个 `>` 开头的块
