---
title: GUI 系统
---

GUI 系统
========

---

1. 桌面用户环境
---------------

Deiban 操作系统有很多的 GUI 桌面环境，这里推荐 `task-gnome-desktop`。

-   X Windows 和 Wayland 的部分区别可以通过工具 `xeyes` 来观察。大部分情况下推荐更现代的 Wayland

    !!! tip "注意"
    
        旧的 X 服务端配置文件 `/etc/X11/xorg.conf`，现在不应该存在。其相关配置现在由内核自动管理，应该移除它避免冲突。

-   GNOME 会自动安装很多著名的 GUI 架构软件包

    -   其中 `gnome-tweaks` 能强制调整声音和修改键位映射

-   用户目录（如 `~/Documents`）的名字，默认使用的是设置的语言。可以通过 `xdg-user-dirs-update(1)` 工具强制设置为英文：

    ``` bash
    LANGUAGE=C xdg-user-dirs-update --force
    ```

    -   其核心功能是管理 `~/.config/user-dirs.dirs` 文件

---

2. 字体
-------

Debian 有很多基础字体，你可能需要了解什么是 metric compatibility 和字重等重要概念。

-   Debian 用 FreeType 来栅格化字体，Fontconfig 来选择和配置字体。

    -   可以用 `fc-match(1)` 来查看默认字体
    -   可以用 `fc-list(1)` 来查看所有可用字体
    -   还有一种琐碎的方式：查看 `fonts.conf(5)` 文件

---

3. 沙盒
-------

为了安全考虑，应始终通过沙盒运行第三方二进制

-   一些沙盒：

    -   AppImage
    -   FLATHUB
    -   snapcraft

-   优先选择自动配置隔离的后两个，AppImage 需要手动配置隔离
-   `xdg-desktop-portal` 为沙盒应用提供一个统一的桌面 API

---

4. 远程桌面
-----------

你应该了解的概念有：

-   SSH 协议

    -   纯文本

-   VNC 协议和 RDP 协议

    -   后者主要用于 Windows

-   SPICE 协议

    -   用于 KVM/QUMU 虚拟机，在云服务上可以提供接近本地 PC 的体验

---

5. X 服务端连接
---------------

连接本地 X 服务通常不需要特别指定，其用到的环境变量通常会被自动设置。远程访问则由 X11 转发特性支持。

若要在 `chroot` 环境使用 X，由于无法访问授权文件的位置 `$XAUTHORITY`，需要 `xhost` 命令临时放宽权限。
