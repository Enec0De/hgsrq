---
title: 表格
---

表格 { #table }
===============

考虑到 Markdown 表格在渲染中存在一些行为可控性方面的限制，建议降低表格元素的使用率[^1]。

[^1]: 更好的解决办法是插入引用图片。

---

=== ":material-format-align-left: Left"

    ``` markdown hl_lines="2" title="Data table, columns aligned to left"
    | :material-console: 命令/语法            | :material-check-all: 描述                | :material-contain-start: |
    | :-------------------------------------- | :--------------------------------------- | :----------------------- |
    | `grep -i "error" /var/log/syslog`       | 在系统日志中不区分大小写地搜索 "error"   | :material-text-search:   |
    | `awk -F: '{print $1,$6}' /etc/passwd`   | 打印 /etc/passwd 的用户名和家目录        | :material-printer:       |
    | `sed -i.bak 's/foo/bar/g' *.txt`        | 替换所有 .txt 文件中的 foo 为 bar 并备份 | :material-file-replace:  |
    | `echo "Today is $(date +%F)" > log.txt` | 将当前日期写入日志文件                   | :material-draw-pen:      |
    ```

    <div class="result" markdown>

    | :material-console: 命令/语法            | :material-check-all: 描述                | :material-contain-start: |
    | :-------------------------------------- | :--------------------------------------- | :----------------------- |
    | `grep -i "error" /var/log/syslog`       | 在系统日志中不区分大小写地搜索 "error"   | :material-text-search:   |
    | `awk -F: '{print $1,$6}' /etc/passwd`   | 打印 /etc/passwd 的用户名和家目录        | :material-printer:       |
    | `sed -i.bak 's/foo/bar/g' *.txt`        | 替换所有 .txt 文件中的 foo 为 bar 并备份 | :material-file-replace:  |
    | `echo "Today is $(date +%F)" > log.txt` | 将当前日期写入日志文件                   | :material-draw-pen:      |

    </div>

=== ":material-format-align-center: Center"

    ``` markdown hl_lines="2" title="Data table, columns centered"
    | :material-console: 命令/语法            | :material-check-all: 描述                | :material-contain-start: |
    | :-------------------------------------: | :--------------------------------------: | :----------------------: |
    | `grep -i "error" /var/log/syslog`       | 在系统日志中不区分大小写地搜索 "error"   | :material-text-search:   |
    | `awk -F: '{print $1,$6}' /etc/passwd`   | 打印 /etc/passwd 的用户名和家目录        | :material-printer:       |
    | `sed -i.bak 's/foo/bar/g' *.txt`        | 替换所有 .txt 文件中的 foo 为 bar 并备份 | :material-file-replace:  |
    | `echo "Today is $(date +%F)" > log.txt` | 将当前日期写入日志文件                   | :material-draw-pen:      |
    ```

    <div class="result" markdown>

    | :material-console: 命令/语法            | :material-check-all: 描述                | :material-contain-start: |
    | :-------------------------------------: | :--------------------------------------: | :----------------------: |
    | `grep -i "error" /var/log/syslog`       | 在系统日志中不区分大小写地搜索 "error"   | :material-text-search:   |
    | `awk -F: '{print $1,$6}' /etc/passwd`   | 打印 /etc/passwd 的用户名和家目录        | :material-printer:       |
    | `sed -i.bak 's/foo/bar/g' *.txt`        | 替换所有 .txt 文件中的 foo 为 bar 并备份 | :material-file-replace:  |
    | `echo "Today is $(date +%F)" > log.txt` | 将当前日期写入日志文件                   | :material-draw-pen:      |

    </div>

=== ":material-format-align-right: Right"

    ``` markdown hl_lines="2" title="Data table, columns aligned to right"
    | :material-console: 命令/语法            | :material-check-all: 描述                | :material-contain-start: |
    | --------------------------------------: | ---------------------------------------: | -----------------------: |
    | `grep -i "error" /var/log/syslog`       | 在系统日志中不区分大小写地搜索 "error"   | :material-text-search:   |
    | `awk -F: '{print $1,$6}' /etc/passwd`   | 打印 /etc/passwd 的用户名和家目录        | :material-printer:       |
    | `sed -i.bak 's/foo/bar/g' *.txt`        | 替换所有 .txt 文件中的 foo 为 bar 并备份 | :material-file-replace:  |
    | `echo "Today is $(date +%F)" > log.txt` | 将当前日期写入日志文件                   | :material-draw-pen:      |
    ```

    <div class="result" markdown>

    | :material-console: 命令/语法            | :material-check-all: 描述                | :material-contain-start: |
    | --------------------------------------: | ---------------------------------------: | -----------------------: |
    | `grep -i "error" /var/log/syslog`       | 在系统日志中不区分大小写地搜索 "error"   | :material-text-search:   |
    | `awk -F: '{print $1,$6}' /etc/passwd`   | 打印 /etc/passwd 的用户名和家目录        | :material-printer:       |
    | `sed -i.bak 's/foo/bar/g' *.txt`        | 替换所有 .txt 文件中的 foo 为 bar 并备份 | :material-file-replace:  |
    | `echo "Today is $(date +%F)" > log.txt` | 将当前日期写入日志文件                   | :material-draw-pen:      |

    </div>

-   三种写法可以在同一表格中实现。
-   超过 5 列或包含多行数据时，为保证可读性，建议改用 HTML 表格，这里不作详细展开。

!!! info "提示"

    上面关于图标和表情的应用可以从[这里][emojis]查阅。

  [emojis]: https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/
