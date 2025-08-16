---
title: 认证和访问控制
---

认证和访问控制
==============

当用户（或程序）需要访问系统时，需要进行认证，确认身份是受信任。

!!! danger "警告"

    PAM 的配置错误可能会锁住你的系统。你必须有一个准备好的救援 CD，或者设立一个替代的 boot 分区。为了恢复系统，你需要使用它们启动系统并纠正错误。

---

1. 一般的 Unix 认证
-------------------

一般的 Unix 认证由 PAM（Pluggable Authentication Modules，即可插入的验证模块）下的 `pam_unix(8)` 模块提供。

-   `pam_unix(8)` 模块使用的三个重要文件：

    -   `/etc/passwd` 参见 `passwd(5)`
    -   `/etc/shadow` 参见 `shadow(5)`
    -   `/etc/group` 参见 `group(5)`

!!! note "注意"

    -   `/etc/gshadow` 为 `/etc/group` 提供了与 `/etc/shadow` 相似的功能，但没有被真正地使用。
    -   在文件 `/etc/pam.d/common-auth` 中添加内容为 `auth optional pam_group.so` 的一行，然后配置 `/etc/security/group.conf`，使得在身份验证过程动态添加用户到组。参见 `pam_group(8)`。
    -   `base-passwd` 软件包包含了一份用户和组的官方文档：`/usr/share/doc/base-passwd/users-and-groups.html`。

---

2. 管理账号和密码信息
---------------------

下面是一些管理账号信息的重要命令。

-   `getent passwd user_name`
-   `getent shadow user_name`
-   `getent group group_name`
-   `passwd`
-   `passwd -e`
-   `chage`

密码和数据的加密参见 `crypt(3)`。

这里介绍两个用于生成加盐的加密密码的独立工具：`whois`，`openssl`。

!!! note "注意"

    在设置了 PAM 和 NSS 的系统上，本地的 `/etc/passwd`、`/etc/group` 和 `/etc/shadow` 可能不会被系统激活使用。上述的命令即使处于这种环境下依旧是有效的。

---

3. PAM 和 NSS
-------------

PAM 是一个独立的认证框架；NSS 是 GNU C 库 (glibc) 的一部分，用于用户/组的名称解析。

-   `libpam-doc` 中 “The System Administrators' Guide” 是了解 PAM 配置的必要文档。

    -   配置文件位置为 `/etc/pam.d/`
    -   特定模块配置文件位置为 `/etc/security/`
    -   还有 `/etc/securetty`、`/etc/nologin` 和 `/etc/environment`

-   `glibc-doc-reference` 中 “System Databases and Name Service Switch” 是了解 NSS 配置的重要文档。

    -   配置文件为 `/etc/nsswitch.conf`

-   在 `systemd` 下，`libpam-systemd` 软件包被安装用来管理用户登录，通过 `systemd-logind` 服务跟踪会话，并为其在 `systemd` 控制组（cgroup）层级中注册用户会话来实现。

    -   参见 `systemd-logind(8)`、`logind.conf(5)` 和 `pam_systemd(8)`。

密码选择的限制是通过 PAM 模块 `pam_unix(8)` 和 `pam_cracklib(8)` 来实现的。它们可以通过各自的参数进行配置。

!!! tip "注意"

    -   Debian 系统中当前的 `su` 命令使用了 PAM，这样当在 `/etc/pam.d/su` 中启用了带有 `pam_wheel.so` 的行后，就能够限制非 **wheel** 组的用户 `su` 到 **root** 组的能力。

    -   安装 `libpam-cracklib` 软件包你能够强制使用严格的密码规则。

---

4. 现代的集中式系统管理
-----------------------

现代的集中式系统管理可以使用集中式的轻量目录访问协议（LDAP）服务器进行部署，从而通过网络管理许多类 Unix 和 非类 Unix 系统。轻量目录访问协议的开源实现是 OpenLDAP 软件。

-   LDAP 服务器使用带有 PAM 和 NSS 的 `libpam-ldap` 和 `libnss-ldap` 软件包为 Debian 系统提供账号信息。
-   参见由 `libpam-doc` 软件包提供的 `pam_ldap.conf(5)` 中的文档和 `/usr/share/doc/libpam-doc/html/`，以及 `glibc-doc` 软件包提供的 `info libc 'Name Service Switch'`。

---

5. 安全认证
-----------

-   熟记一些安全与不安全的服务端口。
-   提供额外安全方式的工具列表：

    -   `knockd`
    -   `fail2ban`
    -   `libpam-shield`

-   关于 **root** 密码安全：建议编辑 `/etc/passwd` 文件，使 **root** 账户条目的第二段为空。

!!! danger "注意"

    一旦某人拥有 **root** shell 访问权限，他能够访问任何内容，并可以重设系统上的任何密码。此外，他可以使用 `john` 和 `crack` 等软件包的暴力破解工具来获取所有用户的密码。被破解的密码，还可能会用来登陆其它系统。
    
    为避免这些相关问题，仅有的理论上的软件解决方案是使用 `dm-crypt` 和 `initramfs` 加密 `/` 分区（或 `/etc` 分区）。这样的话，你总是需要密码来启动系统。

---

6. 其他的访问控制
-----------------

-   访问控制列表（ACLs）
    
    -   更多信息参见 "POSIX Access Control Lists on Linux"、`acl(5)`、`getfacl(1)` 和 `setfacl(1)`
    
-   `sudo(8)`
    
    -   参见 `/usr/share/doc/sudo/examples/sudoers`
    
-   PolicyKit
    
    -   参见 `polkit(8)`

-   许多程序，比如说 `sshd(8)`，使用基于 PAM 的访问控制。也还有许多方式来限制访问一些服务端的程序：

    -   配置文件: `/etc/default/program_name`
    -   后台守护进程（daemon）的 Systemd 服务单元配置
    -   PAM (Pluggable Authentication Modules)
    -   super-server 使用 `/etc/inetd.conf`
    -   TCP wrapper 使用 `/etc/hosts.deny` 和 `/etc/hosts.allow`，`tcpd(8)`
    -   Sun RPC 使用 `/etc/rpc.conf`
    -   `atd(8)` 使用 `/etc/at.allow` 和 `/etc/at.deny`
    -   `crontab(1)` 使用 `/etc/cron.allow` 和 `/etc/cron.deny`
    -   Network firewall 或 netfilter 框架

!!! note "提示"

    -   NFS 和其它基于 RPC 的程序，需要激活 Sun RPC 服务。
    -   如果你远程访问最新的 Debian 系统有问题，看下在 `/etc/hosts.deny` 里是否存在 `ALL: PARANOID` 这样讨厌的配置，请把它注释掉。

---

7. Linux 安全特性
-----------------

-   Linux 支持 扩展属性，扩展了传统的 UNIX 属性 (参见 xattr(7))。
-   Linux 把传统的超级用户相关的特权分开到不同的单元，被称为 capabilities(7)，它能够独立的启用和禁用。从 2.2 版本内核开始，Capabilities 是一个线程独立的属性。
-   Linux Security Module (LSM) 安全模块框架 提供了一个多方面的安全检查机制，和新的内核扩展关联。例如：

    -   AppArmor
    -   Security-Enhanced Linux (SELinux)
    -   Smack (Simplified Mandatory Access Control Kernel)
    -   Tomoyo Linux

!!! tip "提示"

    这些扩展紧缩的权力模型比普通的类 Unix 安全模型策略更加严格，甚至 **root** 的权力也被限制。建议你阅读 [kernel.org][kernel] 上的 Linux 安全模块（LSM）框架文档。

-   从内核 5.6 版本起，有 8 种 namespaces（参见 `namespaces(7)`，`unshare(1)`，`nsenter(1)`）。
-   Debian 使用 unified cgroup hierarchy（统一 cgroup 层级架构，亦称为 cgroups-v2）。
-   namespaces 同 cgroups 一起来隔离它们的进程，允许资源控制的使用示例是：

    -   Systemd
    -   沙盒环境
    -   Linux 容器，比如 Docker、LXC

这些高级话题大部分超出了本介绍文档的范围，建议你自己去找资料了解。

  [kernel]: https://kernel.org/
