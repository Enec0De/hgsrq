---
title: 国际化和本地化
---

国际化和本地化
==============

一个应用软件的多语言化（Multilingualization，M17N）或本地语言支持，通过 2 个步骤完成。

-   Internationalization（I18N）：使一个软件能够处理多个语言环境。
-   Localization（L10N）：使一个软件处理一个特定的语言环境。

---

1. 语言环境
-----------

程序的语言环境通过配置环境变量 `$LANG` 来实现。其依赖 `libc` 库提供的特性，并要求安装 `locales`（或者 `locales-all`）软件包。

-   如果没有语言环境的支持，系统使用 US 英语消息，并按 ASCII 处理数据
-   这个行为和 `$LANG` 设置为空、`C` 或者是 `POSIX` 时相同
-   重设语言环境可以通过如下的方式配置：

    ``` bash
    dpkg-reconfigure locales
    ```
    
    然后用 `locales` 工具创建 `/etc/default/locale`

-   跨平台的挂载 `mount(8)` 需要明确选项来使用 UTF-8
-   通过安装 `manpages-LANG` 可以获得本地化的手册

    ``` bash
    LANG=it_IT.UTF-8 man programname
    ```

-   还可以通过 `$LANGUAGE` 环境变量设定语言翻译的优先级

    -   参见 `info gettext`

-   `$LANG` 环境变量的覆盖顺序可以从 `locale(7)` 里了解

    -   尽量只使用 `$LANG` 来配置一个 UTF-8 环境

---

2.  键盘输入
------------

Debian 可以通过 `keyboard-configuration` 和 `console-setup` 软件包配置多个国际化键盘布局。

-   `dpkg-reconfigure keyboard-configuration` 会重置 `/etc/default/keyboard`
-   `dpkg-reconfigure console-setup` 会重置 `/etc/default/console-setup`
-   前者主要负责 X Window 系统的键盘配置，后者主要负责控制台(终端)的键盘配置
-   Wayland 上推荐用 `ibus`
-   `im-config` 是一个输入法管理框架

---

3. 显示输出
-----------

Linux 控制台只能显示有限的字符，除非使用特殊的终端，如 `jfbterm`。
