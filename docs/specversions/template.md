---
title: Markdown 语法规范
---

Markdown 语法规范 { id=“template” }
===================================

> 创建于：2025-08-11 :octicons-chevron-right-16: 最后更新：2025-09-13

---

简介说明 { id="introduction" }
------------------------------

本页列出的 Markdown 语法已涵盖本手册所有页面的构建需求。原则上，未提及的语法特性与元素构建方式，均不在手册编写范围内[^1]，以此确保文档结构的简洁性。

!!! danger "警告"

    遇到任何非预期的渲染结果时，建议直接从本页面复制相应代码使用，生产环境中请不要尝试任何未定义的行为。

---

快速开始 { id="quickstart" }
----------------------------

以下模板快速地实现了一个文档的基本结构：

``` markdown title="template.md" linenums="1"
# Page title

> Created：2025-01-01 | Last update：2025-01-01

## Section 1

Content...

## Section 2

Content...
```

---

通用 Markdown 语法 { id="common-markdown" }
-------------------------------------------

下方代码块所展示元素的创建方式均符合 [CommonMark][commonmark] 核心规范。各元素嵌套使用时，缩进决定层级[^2]，空行决定边界。

<div class="grid" markdown>

``` markdown linenums="1"
*Italic*
**Bold**
***Italic and Bold***
```

``` markdown linenums="1"
> Blockquote
>
> > Nested Blockquotes
```

``` markdown 
[Link][1]
...
[1]: https://example.com "title"
```

``` markdown
![Image][1]
...
[1]: https://example.com "title"
```

``` markdown linenums="1"
-   List
-   List
-   Escape using `\-`
```

``` markdown linenums="1"
-   List
<!-- -->
-   List
```

``` markdown linenums="1"
1.  One
1.  Two
1.  Escape using `1\.`
```

``` markdown linenums="1"
<!-- Horizontal rule: -->

---
```

``` markdown linenums="1"
`Inline code`
<!-- Example with backticks: -->
`` `foo` `bar` ``
```

```` markdown linenums="1"
```
print '3 backticks or indent 4 spaces'
```
````

``` markdown
<span id="anchor" aria-hidden="true"></span>
...
[Link](#anchor)
```

</div>

---

扩展 Markdown 语法 { id="python-markdown" }
-------------------------------------------

### 1. 通用语法扩展 { id="general-syntax-extension" }

参考[附录](#appendix)内 Python Markdown 相关链接，可以对通用 Markdown 语法的功能进行扩展。

-   标题语法扩展： 
    -   本手册采用 Setext 风格的方式来创建标题[^3]，从而增加源码的可读性。
    -   建议通过 `{ }` 包裹的 `id` 和 `data-toc-label` 标签来分别修改锚点和目录。

-   代码块语法扩展：
    -   可以指定语言进行高亮，支持语言参考[该页面][lexers]。
    -   代码块额外提供的选项还有：`title`、`linenums`、`hl_lines`。

### 2. 新增元素扩展 { id="new-element-extension" }

下方代码块所展示元素的创建方式均**不属于** [CommonMark][commonmark] 核心规范。各元素嵌套使用时，缩进决定层级[^2]，空行决定边界。

-   Metadata 元素可以参考[该页面][metadata]
-   Admonition 元素可以参考[该页面][admonition]
-   Key 元素可以参考[该页面][keys]。

<div class="grid" markdown>

``` markdown title="Footnotes" 
Content[^1]
...
[^1]: Footnote.
```

``` markdown title="Abbreviation"
[Hover me]
...
*[Hover me]: Abbreviation
```

``` markdown title="Task Lists" linenums="1"
- [x] Finished
- [ ] Unfinished
- [ ] ...
```

``` markdown title="Definition Lists" linenums="1"
Term to be defined

:   Definition text
```

``` markdown title="Metadata" linenums="1"
---
title: Page title
---
```

``` markdown title="Admonition" linenums="1"
!!! example "Example"

    Keep It Simple, Stupid.
```

``` markdown title="Keys"
++ctrl+alt+del++
++ctrl+alt+"My Special Key"++
++cmd+alt+"&Uuml;"++
```

``` markdown title="Caret"
<!-- This is better than Italic -->

^^Insert me^^
```

</div>

### 3. 其他复杂元素 { id="other-complex-element" }

该部分内容不作详细介绍，仅使用下方代码块内所展示的用法，不依赖除此以外的任何高级特性。细节注意高亮代码示意即可。

<div class="grid" markdown>

```` markdown title="Single Line Embedding" hl_lines="4 5"
``` py
;--8<-- "filename.py:1:3,5:6"
;--8<-- "filename.py:2:"
;--8<-- "; skip.py"
;;--8<-- "skip.py"
```
````

```` markdown title="Block Format Embedding" hl_lines="4"
``` py
;--8<--
filename.py
; skip.py
;--8<--
```
````

``` html title="Card Grid" linenums="1" hl_lines="5-9 11-15"
<div class="grid cards" markdown>

-   Card grid 1.
-   Card grid 2.
-   Card grid 3.

    ---

    :octicons-file-code-16: Title

-   Card grid 4.

    ---

    :octicons-arrow-right-16: More

</div>
```

```` html title="Generic Crid" linenums="1" hl_lines="3 4 6 8-11 13-15"
<div class="grid" markdown>

Card grid content.
{ .card }

> Blockquote

=== "Content tab"

    1. One
    1. Two

``` title="Code block"
Any code ...
```

</div>
````

</div>

### 4. 数学公式元素 { id="math" }

用如下 HTML 元素包裹代码块，可以展示其渲染结果。效果如 KaTeX 代码块下半部分所示。

``` html
<div class="result" markdown> Any markdown code ... </div>
```

``` markdown title="KaTeX" linenums="1"
Fourier Transform:

\\[
\mathcal{F} \{f(t)\} (\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt.
\\]
```

<div class="result" markdown> 

Fourier Transform:

\\[
\mathcal{F} \{f(t)\} (\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt.
\\]

</div>

---

手册规范 { id="specification" }
-------------------------------

总结上述所有内容，在本手册中，最终确定的文档基本结构模板如下方代码块所示。在任何情况下，你都可以复制这 13 行代码作为文档的开头，略作修改后开始内容的产出[^4]。

``` markdown title="new-template.md" linenums="1"
---
title: Page title
---

Page title { id="New-title" }
=============================

> 创建于：2025-01-01 | 最后更新：2025-01-01

---

Section 1 { id="New-section" }
------------------------------
...
```

### 其他细则 { id="others" }

<!-- 以下内容有待补充... -->

1.  本规范对文档结构与层次的约定如下：
    -   通过 `---` 生成水平分割线，划分各二级标题的所属内容。
    -   尽量减少三级标题的使用，且不使用四级标题[^5]。
    -   尽量减少或避免使用嵌套内容，嵌套层级过多易导致不必要的复杂化[^6]。

1.  本规范未提及的其他元素与细节说明如下：
    -   插入图片时，如需保证排版效果，可通过嵌入 HTML 标签灵活调整图片样式。
    -   本规范未提供表格相关元素的规定，如需使用表格，可引入 HTML 表格实现。

---

附录：相关链接 { id="appendix" }
--------------------------------

-   通用 Markdown 规范：[CommonMark][commonmark]
-   Python Markdown 扩展：[Python Markdown][python-markdown]、[Python Markdown Extensions][pymdown-extensions]
-   数学公式渲染：[KaTeX][katex]
-   代码高亮实现：[Python syntax highlighter][pygments]

[commonmark]: https://commonmark.org/ "CommonMark"
[lexers]: https://pygments.org/docs/lexers/ "Available lexers - Pygments"
[metadata]: https://squidfunk.github.io/mkdocs-material/reference/ "Reference - Material for MkDocs"
[admonition]: https://squidfunk.github.io/mkdocs-material/reference/admonitions/ "Admonitions - Material for MkDocs"
[keys]: https://facelessuser.github.io/pymdown-extensions/extensions/keys/ "Keys - PyMdown Extensions"
[python-markdown]: https://python-markdown.github.io/ "Python - Markdown"
[pymdown-extensions]: https://facelessuser.github.io/pymdown-extensions/ "Pymdown Extensions"
[katex]: https://katex.org/ "KaTeX"
[pygments]: https://pygments.org/ "Pygments"

[^1]: 例外情况请添加 `<!-- comment -->` 注释说明。
[^2]: 通常以每层缩进 4 空格为规则。
[^3]: 考虑到 Setext 风格创建语法在某些解析器上的表现不佳，因此这一条不放在通用 Markdown 语法的部分。
[^4]: 考虑到网页字体渲染的实际表现，区分日期的竖线会改为使用 `:octicons-chevron-right-16:`。
[^5]: 你可以使用 `**...**` 来加粗字体，从而强调小节标题。
[^6]: 此时有可能会导致非预期的渲染结果。
