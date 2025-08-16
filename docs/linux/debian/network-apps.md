---
title: 网络应用
---

网络应用
========

建立网络连接后，你可以运行各种网络应用。

---

1. 网页浏览器
-------------

-   图形界面浏览器：`Firefox ESR`、`Chromium`
-   终端文本浏览器：`lynx`、`w3m`

### 1.1. 伪装用户代理字符串

为了访问一些过度限制的网站，你可能需要伪装网页浏览器程序返回的 User-Agent 字符串。

!!! note "小心"

    这部分内容主要面向需要测试网站兼容性或访问受限内容的开发者/高级用户，普通用户通常不需要修改这个设置。

### 1.2. 浏览器扩展

所有现代的 GUI（图形用户界面）浏览器支持基于 browser extension 的源代码，它在按 web extensions 变成标准化。

---

2. 邮件系统
-----------

### 2.1. 电子邮件基础

电子邮件由三个部分组成：消息的信封、邮件头以及邮件正文。

-   SMTP 用电子邮件信封上的 “To” 和 “From” 来投递邮件。信封上的 “From” 信息也被叫做*退回地址*。
-   电子邮件头也有 “To” 和 “From” 信息。
-   覆盖邮件头和正文数据的电子邮件消息格式被 MIME 扩展。

一些 MUA：`evolution`、`mutt`

### 2.2. 现代邮件服务限制

如果你需要自建邮件服务器，应：

-   使用商业 VPS（非家庭网络）并配置 SPF/DKIM/DMARC。
-   通过智能主机（如 Mailgun、SendGrid）中继邮件，避免端口封锁问题。
-   始终使用端口 587（Submission）而非端口 25（SMTP）发送邮件。

### 2.3. 历史邮件服务端期望

默认期望由 `/usr/sbin/sendmail` 命令发送邮件

-   若目的地为本机，`/usr/sbin/sendmail` 接口进行邮件的本地分发，将邮件投入 `/var/mail/$username`。
-   若目的地为远程主机，`/usr/sbin/sendmail` 接口使用 SMTP 查询 DNS MX 记录传输邮件到目标主机。

### 2.4. 邮件传输代理（MTA）

对于现代移动工作站:

1.  如果只用 GUI 邮件客户端: 完全不需要安装 MTA
1.  如果有程序需要 `sendmail`:

    -   安装 `exim4-daemon-light` 或 `postfix`
    -   配置为通过智能主机发送邮件
    -   确保 `/etc/aliases` 配置正确

### 2.5. 一些配置

-   配置 `exim4` 请阅读 `/usr/share/doc/exim4-base/README.Debian.gz` 官方指导和 `update-exim4.conf(8)`。
-   带有 SASL 的 postfix 配置，请阅读阅读 postfix 文档和关键的手册页。

    -   一些重要的手册：`postfix(1)`、`postconf(1)`、`postconf(5)`、`postmap(1)`、`postalias(1)`

-   这里有一些用于邮件传输、投递和用户代理的邮件地址配置文件

    -   `/etc/mailname`
    -   `/etc/email-addresses`
    -   `/etc/postfix/generic`
    -   `/etc/aliases`

### 2.6. 基础 MTA 操作

基础 MTA 操作列表：

| `exim` 命令	        | `postfix` 命令	                        |
| :-------------------: | :---------------------------------------: |
| `sendmail`	        | `sendmail`     	                        |
| `mailq`	            | `mailq`          	                        |
| `newaliases`	        | `newaliases`   	                        | 
| `exim4 -q`	        | `postqueue -f`	                        | 
| `exim4 -qf`	        | `postsuper -r ALL deferred; postqueue -f` | 
| `exim4 -qff`	        | `postsuper -r ALL; postqueue -f`          | 
| `exim4 -Mg queue_id`  | `postsuper -h queue_id`	                | 
| `exim4 -Mrm queue_id` | `postsuper -d queue_id`	                | 
| `N/A`	                | `postsuper -d ALL`

!!! tip "提示"

    往 `/etc/ppp/ip-up.d/*` 里写一个刷新所有邮件的脚本会是个不错的主意。

---

3. 服务器远程访问和工具（SSH）
------------------------------

请阅读 `/usr/share/doc/openssh-client/README.Debian.gz`、`ssh(1)`、`sshd(8)`、`ssh-agent(1)`、`ssh-keygen(1)`、`ssh-add(1)` 和 `ssh-agent(1)`。

配置文件相关请阅读 `ssh_config(5)`、`sshd_config(5)`。

!!! danger "警告"
 
    如果想要运行 OpenSSH 服务，`/etc/ssh/sshd_not_to_be_run` 必须不存在。

    不要打开基于 rhost 的认证（`/etc/ssh/sshd_config` 中的 HostbasedAuthentication）。

-   免密码远程连接

    ``` bash
    ssh-keygen -t rsa
    cat .ssh/id_rsa.pub | ssh user1@remote "cat - >>.ssh/authorized_keys"
    ```

-   以下命令参阅 `ssh-agent(1)` 和 `ssh-add(1)`

    ``` bash
    ssh-agent bash
    ssh-add ~/.ssh/id_rsa
    ```

-   从远程主机发邮件

    ``` bash
    ssh username@example.org /usr/sbin/sendmail -bm -ti -f "username@example.org" < mail_data.txt
    ```

-   SMTP/POP3 隧道的端口转发

    ``` bash
    ssh -q -L 4025:remote-server:25 4110:remote-server:110 username@remote-server
    ```

-   通过 SSH 关闭远程系统

    ```bash
    echo "shutdown -h now" | at now
    ```

---

4. 打印服务和工具
-----------------

CUPS 是 Linux 的标准打印系统，基于 IPP 协议和 PDF 格式，通过 `lpr`（需安装 cups-bsd 包）命令实现自动化的跨平台打印。

---

5. 其他网络应用服务
-------------------

其他网络应用服务：`telnetd`、`telnetd-ssl`、`nfs-kernel-server`、`samba`、`netatalk`、`proftpd-basic`、`apache2`、`squid`、`bind9`、`isc-dhcp-server`

!!! tip "提示"

    通用互联网文件系统协议（CIFS）和服务消息块（SMB）协议一样，被微软 Windows 广泛应用。

---

6. 其他网络应用客户端
---------------------

其他网络应用客户端：`netcat`、`openssl`、`stunnel4`、`telnet`、`telnet-ssl`、`nfs-common`、`smbclient`、`cifs-utils`、`ftp`、`lftp`、`ncftp`、`wget`、`curl`、`axel`、`aria2`、`bind9-host`、`dnsutils`、`isc-dhcp-client`、`ldap-utils`

---

7. 系统后台守护进程（daemon）诊断
---------------------------------

`telnet` 程序能够手工连接到系统后台守护进程（daemon），并进行诊断。

下面的 RFCs 提供每一个系统后台守护进程（daemon）所需要的知识。

-   常用 RFC 列表：

    | RFC  	            | 说明                        |
    | :---------------: | :-------------------------: |
    |rfc1939 和 rfc2449 | POP3 服务                   |
    |rfc3501	        | IMAP4 服务                  |
    |rfc2821 (rfc821)   | SMTP 服务                   |
    |rfc2822 (rfc822)   | 邮件文件格式                |
    |rfc2045	        | 多用途互联网邮件扩展（MIME）|
    |rfc819	            | DNS 服务                    |
    |rfc2616	        | HTTP 服务                   |
    |rfc2396	        | URI 定义                    |

-   在 `/etc/services` 里，描述了端口用途.


