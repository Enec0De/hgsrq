---
title: 参考引用
---

参考引用 { #reference }
=======================

:octicons-pencil-24: 一些比较零碎的内容。

---

-   中文间不可以穿插术语，但是可以这样：术语，或者**术语**。
    
    *[术语]: abbr.
    
    ``` markdown 
    内容间不可以穿插术语，但是可以这样：术语，或者**术语**。
    
    *[术语]: abbr.
    ```
    
    ---
    
-   使用[链接][Hover me]，文件使用相对路径，注意对齐缩进。
    
      [Hover me]: https://example.com "网站：example.com"
    
    ``` markdown 
    使用[链接][Hover me]，注意对齐缩进。
    
      [Hover me]: https://example.com "网站：example.com"
    ```
    
    ---
    
-   引用图片不做演示，直接提供代码，和上述的链接类似。同时注意缩进。
    
    ``` markdown 
    ![图片][image]
    
      [image]: ../assets/images/jellyfish-outline.svg
    ```
    
    ---
    
-   单行脚注[^1]，多行脚注[^2]。
    
    [^1]: a single line.
    [^2]:
        Paragraphs can be written on the next line
        and must be indented by four spaces.
    
    ``` markdown
    单行脚注[^1]，多行脚注[^2]。
    
    [^1]: a single line.
    [^2]:
        Paragraphs can be written on the next line
        and must be indented by four spaces.
    ```
   
    ---

-   [快速跳转][link]的锚点放在目标位置上面，单独一行。
 
      [link]: code-blocks.md#anchor

    === ":octicons-file-code-16: code-blocks.md"
    
        ``` markdown linenums="44" hl_lines="2"
        ...
        <span id="anchor" aria-hidden="true"></span>
        展示其渲染结果，[效果如上][out]，用如下代码包裹：
        ...
        ```

    ``` markdown 
    [快速跳转][link]
      
      [link]: #anchor
    ```
