---
title: 文档源代码结构
---

个人文档代码规范 { id="document-structure" }
============================================

:octicons-milestone-24: 产出内容时，应有一些基本框架。

---

基本结构 { id="structure" }
---------------------------

以下代码模版描述了一个文档的基本骨架：

``` markdown title="template.md" linenums="1" hl_lines="5 6 14 15 19"
---
title: 页面标题
---

一级标题 { id="New-H1" data-toc-label="New-H1" }
================================================

> 创建于：2025-07-11 | 最后更新：2025-07-11

<!-- 注释内容 -->

---

二级标题 { id="New-H2" data-toc-label="New H2" }
------------------------------------------------

`---` 为水平分隔线。*斜体*、**粗体**、***斜粗体***。

### 三级标题 { id="New-H3" data-toc-label="New H3" }

> 约定不使用四级及以上层级的标题。
>
> > 最多仅使用一层嵌套引用。
```

!!! warning "警告"

    高亮处花括号部分可选，同时，标题创建语法的选择仅为个人喜好[^1]。

[^1]:
    目的是在我的工作环境下兼顾源代码的可读性，很大程度上取决于我个人的风格偏好，在此处**并非最佳工程实践**。

---

元数据 { id="meta-data" }
-------------------------

元数据（metadata）在文档开头用两行 `---` 包裹：

``` markdown linenums="1" hl_lines="2"
---
title: Getting-started
---

Page title
==========
...
```

可用属性包括：`title`、`description`、`icon`、`status`、`subtitle`、`template`，参考[文档][ref]。

  [ref]: https://squidfunk.github.io/mkdocs-material/reference/
