---
title: 其他元素
---

其他元素 { #others }
====================

:octicons-dependabot-24: 一些比较简单的东西，凑在一页。

---

警告框 { #admonitions }
-----------------------

警告框的常用类型为：`note`，`info`，`tip`，`warning`。

其他可选：`abstract`，`success`，`question`，`failure`，`danger`，`bug`，`example`，`quote`。

``` markdown title="Admonitions"
!!! warning "Warning"

    尽量保证简洁，不乱用警告框。
```

<div class="result" markdown>

!!! warning "Warning"

    尽量保证简洁，不乱用警告框。

</div>

---

快捷键 { #shortcuts }
---------------------

``` markdown title="Keyboard keys"
++ctrl+alt+del++
```

<div class="result" markdown>

++ctrl+alt+del++

</div>

!!! info "提示"
    
    更多的快捷键可以在[官方文档][shortcuts]处指引的[扩展文档][extensions]内查询。

  [shortcuts]: https://squidfunk.github.io/mkdocs-material/reference/formatting/#adding-keyboard-keys
  [extensions]: https://facelessuser.github.io/pymdown-extensions/extensions/keys/#extendingmodifying-key-map-index

---

数学公式 { #math }
------------------

用的是 [KaTeX][katex] 。

``` markdown title="KaTeX math typesetting"
**Fourier Transform:**
$$
\mathcal{F} \{f(t)\} (\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt.
$$
```

<div class="result" markdown>

**Fourier Transform:**
$$
\mathcal{F} \{f(t)\} (\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt.
$$

</div>

  [katex]: https://katex.org/
