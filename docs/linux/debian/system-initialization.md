---
title: 系统初始化
---

系统初始化
==========

参考最新文档：

-   [Debian Linux 内核手册][kenerl]。
-   `bootup(7)` 介绍了基于 `systemd` 的系统启动流程 。
-   `boot(7)` 介绍了基于 UNIX System V Release 4 的系统启动流程。

  [kenerl]: https://kernel-team.pages.debian.net/kernel-handbook/index.html

---

1. 启动过程概述
---------------

### 第一阶段：UEFI

计算机打开电源时，由 UEFI 固件访问 ESP 分区，从而加载 boot loader。其默认行为由厂商设定。

### 第二阶段：Bootloader

由 UEFI 启动，boot loader 将**系统内核映像**和 **initrd 映像**加载到内存并将控制权交给它们。

-   **initrd 映像**是根文件系统映像, 以现在的技术看来，它其实应该叫 initramfs 映像（initial RAM filesystem）。对于 Debian 系统，其 boot loader 是 GRUB2。

-   UEFI 系统加载 GRUB2 后，GRUB2 再一次读取 ESP 分区，使用 `/boot/efi/EFI/debian/grub.cfg` 里面 `search.fs_uuid` 字段指定的 UUID 来确定 GRUB2 菜单配置文件 `/boot/grub/grub.cfg` 所在的分区。

-   更多细节参见 `info grub` 和 `grub-install(8)`。

### 第三阶段：内核初始化

在这里又可以称为迷你 Debian 系统阶段，`/init` 程序是根文件系统执行的第一个程序。这个程序在用户空间把内核初始化，并把控制权交给下一阶段。

-   如果 initramfs 是由 `initramfs-tools` 创建，则 `/init` 程序是一个 shell 脚本程序。

    -   迷你 Debian 系统中可用的命令是精简过的，且主要由一个称为 `busybox(1)` 的 GNU 工具提供。

-   如果 initramfs 是由 `dracut` 创建，则 `/init` 程序是一个二进制 `systemd` 程序。

    -   迷你 Debian 系统中可用的命令是一个精简过的 `systemd(1)` 环境。

!!! note "小心"

    当在一个只读的根文件系统上时，使用 `mount` 命令需要添加 -n 选项。

### 第四阶段：用户空间初始化

内核在此环境下继续运行。根文件系统将由内存切换到实际的硬盘文件系统上。

-   `init` 程序是系统执行的第一个程序（PID=1），它启动其它各种程序以完成主引导流程。`init` 程序的默认路径是 `/usr/sbin/init`，但可通过内核启动参数修改，例如 `init=/path/to/init_program`。在 Debian 系统，`/usr/sbin/init` 是一个到 `/lib/systemd/systemd` 的符号链接。

---

2. Systemd
----------

-   `systemd` 初始化进程基于单元配置文件来并行派生进程
    
    -   单元配置文件参见 `systemd,unit(5)`、`systemd.resource-control(5)`
    
    -   配置文件及其加载路径参阅 `systemd-system.conf(5)`
    
-   系统启动时，`systemd` 进程会尝试启动 `/lib/systemd/system/default.target`
    
    -   详细内容参阅 `systemd.special(7)`、`bootup(7)`
    
-   `systemd` 提供向后兼容的功能。在 '/etc/init.d/rc[0-6S].d/[KS]name' 里面 SysV 风格的启动脚本仍然会被分析；`telinit(8)` 会被转换为 `systemd` 的单元活动请求
    
-   当一个用户登陆到系统，其也会提供用户级别的 systemd 服务管理机制，在无需 **root** 权限的情况下管理自己的服务

---

3. 内核消息
-----------

在控制台上显示的内核错误消息，可以通过设置它们的阈值水平来配置，例如：`dmesg -n3`

---

4. 系统消息
-----------

在 `systemd` 下, 内核和系统的信息都通过日志服务 `systemd-journald.service`（或者叫 `journald`）来记录

-   放在 `/var/log/journal` 下（不变的二进制数据），或放在 `/run/log/journal/` 下（变化的二进制数据）

    -   可以通过 journalctl(1) 命令来访问。

-   一些典型的命令片段：

    -   `journalctl -b`
    -   `journalctl -b --system`
    -   `journalctl -b --user`
    -   `journalctl -b -u $unit`
    -   `journalctl -b -u $unit -f`

-   在 systemd 下，系统日志工具 rsyslogd(8) 的行为发生变化：

    -   传统的默认行为是从 `/dev/log` 读取日志
    -   改为从 `/run/systemd/journal/syslog` 读取二进制文件
    -   `/etc/default/rsyslog` 和 `/etc/rsyslog.conf` 能够自定义日志文件和屏幕显示
    -   参见 `rsyslogd(8)` 和 `rsyslog.conf(5)`

---

5. 系统管理
-----------

一些典型的 `systemctl(1)` 命令片段列表：

-   `systemctl list-units --type=help`
-   `systemctl list-timers` / `systemctl list-dependencies --all` / `systemctl list-unit-files`
-   `systemctl start $unit` / `systemctl stop $unit`
-   `systemctl reload $unit`
-   `systemctl restart $unit`
-   `systemctl isolate $unit` / `systemctl isolate graphical` / `systemctl isolate rescue`
-   `systemctl kill $unit`
-   `systemctl is-active $unit` / `systemctl is-failed $unit`
-   `systemctl status $unit|$PID|$device`
-   `systemctl show $unit|$job`
-   `systemctl reset-failed $unit`
-   `systemctl enable $unit` / `systemctl disable $unit`
-   `systemctl unmask $unit` / `systemctl mask $unit`
-   `systemctl get-default` / `systemctl set-default multi-user`
-   `systemctl show-environment` / `systemctl set-environment variable=value` / `systemctl unset-environment variable`
-   `systemctl daemon-reload`
-   `systemctl poweroff` / `systemctl reboot` / `systemctl suspend` / `systemctl hibernate`

!!! tip "提示"

    shell 式样的全局通配符"*", "?", "[]"，通过使用 `fnmatch(3)`，来匹配目前在内存中的所有单元的基本名称。

---

6. 其他系统监控
---------------

这里是 systemd 下其它零星的监控命令列表。请阅读包括 `cgroups(7)` 在内的相关的 man 手册页。

-   `systemd-analyze time`
-   `systemd-analyze blame`
-   `systemd-analyze verify $unit`
-   `loginctl user-status`
-   `loginctl session-status`
-   `systemd-cgls`
-   `ps xawf -eo pid,user,cgroup,args`
-   读取 `/sys/fs/cgroup/` 下的 `sysfs`

---

7. 系统配置
-----------

### 7.1. 主机名

内核在启动的时候，通过 `systemd-hostnamed.service` 启动的系统单位设置系统的主机名

-   此主机名保存在 `/etc/hostname`
-   不带参数运行 `hostname(1)` 命令可以打印出当前的主机名

### 7.2. 文件系统
    
-   硬盘和网络文件系统的挂载选项可以在 `/etc/fstab` 中设置，参见 `fstab(5)`
-   加密文件系统的配置设置在 `/etc/crypttab` 中,参见 `crypttab(5)`
-   软 RAID 的配置 `mdadm(8)` 设置在 `/etc/mdadm/mdadm.conf`，参见 `mdadm.conf(5)`

!!! warning "警告"

    每次启动的时候，在挂载了所有文件系统以后，`/tmp`, `/var/lock`, 和 `/var/run` 中的临时文件会被清空。

### 7.3. 网络接口初始化

对于使用 `systemd` 的现代 Debian 桌面系统，网络接口通常由两个服务进行初始化：`lo` 接口通常在 `networking.service` 处理，而其它接口则由 `NetworkManager.service` 处理。

### 7.4. 云系统初始化

主机名、文件系统、网络、语言环境、SSH 密钥、用户和组等个性化信息，可以使用 `cloud-init` 和 `netplan.io` 软件包提供的功能来配置，利用多个数据源，放在原始系统镜像里面的文件和在启动过程中提供的外部数据。这些软件包使用 YAML 数据来声明系统配置。

### 7.5 定制自己的 sshd 服务

传统 Unix 服务的按需套接字激活（on-demand socket activation）系统由 `inetd`（或 `xinetd`）超级服务来提供。在 `systemd` 下, 相同功能能够通过增加 `*.socket` 和 `*.service` 单元配置文件来启用：

1.  首先，禁用系统安装的服务单元

    ``` bash
    sudo systemctl stop sshd.service
    sudo systemctl mask sshd.service
    ```

1.  定义一个监听的套接字 `sshd.socket`，`sshd@.service` 作为其匹配的服务文件

    === ":octicons-file-code-16: sshd.socket"

        ``` systemd
        [Unit]
        Description=SSH Socket for Per-Connection Servers
        
        [Socket]
        ListenStream=22
        Accept=yes
        
        [Install]
        WantedBy=sockets.target
        ```

    === ":octicons-file-code-16: sshd@.service"

        ``` systemd
        [Unit]
        Description=SSH Per-Connection Server
        
        [Service]
        ExecStart=-/usr/sbin/sshd -i
        StandardInput=socket
        ```

1.  然后重新加载

    ``` bash
    sudo systemctl daemon-reload
    ```

---

8. `udev` 系统
--------------

从 Linux 内核 2.6 版开始，`udev` 系统提供了自动硬件发现和初始化机制。

-   在内核发现每个设备的基础上，`udev` 系统使用从 sysfs 文件系统的信息启动一个用户进程，使用 `modprobe(8)` 程序加载支持它所要求的内核模块, 创建相应的设备节点
-   参见 `udev(7)`

!!! tip "提示"

    如果由于某些理由，`/lib/modules/kernel-version/modules.dep` 没有被 `depmod(8)` 正常生成，模块可能不会被 `udev` 系统按期望的方式加载。执行 `depmod -a` 来修复它。

!!! danger "警告"

    不要尝试用 `udev` 规则里面的 RUN 长期运行程序，比如说备份脚本。请创建一个适当的 `systemd.service(5)` 文件并激活它来替代。

---

9. 内核模块初始化
-----------------

通过 `modprobe(8)` 程序添加和删除内核模块，使我们能够从用户进程来配置正在运行的 Linux 内核。

-   `udev` 系统自动化它对 `modprobe(8)` 的调用来帮助内核模块初始化。
-   下面的非硬件模块和特殊的硬件驱动模块，需要被预先加载，把它们在 `/etc/modules` 文件里列出（参见 `modules(5)`）

    -   TUN/TAP 模块提供虚拟的 Point-to-Point 网络设备（TUN）和虚拟的 Ethernet 以太网网络设备（TAP）
    -   netfilter 模块提供 netfilter 防火墙能力，参阅 `iptables(8)`
    -   watchdog timer 驱动模块

-   `modprobe(8)` 程序的配置文件是按 `modprobe.conf(5)` 的说明放在"/etc/modprobes.d/" 目录下

    -   如果你想避免自动加载某些内核模块，考虑把它们作为黑名单放在 `/etc/modprobes.d/blacklist` 文件里

-   `/lib/modules/version/modules.dep` 文件由 `depmod(8)` 程序生成，它描述了 `modprobe(8)` 程序使用的模块依赖性.

!!! note "注意"

    如果你在启动时出现模块加载问题，或者 `modprobe(8)` 时出现模块加载问题, `depmod -a` 可以通过重构 `modules.dep` 来解决这些问题。

-   `modinfo(8)` 程序显示 Linux 内核模块信息

-   `lsmod(8)` 程序以好看的格式展示 `/proc/modules` 的内容，显示当前内核加载了哪些模块
