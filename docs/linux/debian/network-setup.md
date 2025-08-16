---
title: 网络设置
---

网络设置
========

-   关于 Debian 专属的网络手册，请查看 [Debian 管理员手册—网络配置][net]。
-   `systemd` 环境下，可以用 `networkd` 来配置网络。请参考 `systemd-networkd(8)`。

  [net]: https://debian-handbook.info/browse/stable/basic-configuration.html

---

1. 基本网络架构
---------------

给出一些网络配置工具：

-   网络管理：`network-manager`、`network-manager-gnome`、`ifupdown`
-   DHCP/WiFi：`isc-dhcp-client`、`wpasupplicant`、`wireless-tools`
-   诊断工具：`iw`、`iproute2`、`iptables`、`nftables`
-   测试工具：`iputils-ping`、`ethtool`、`nmap`、`tcpdump`
-   高级工具：`wireshark`、`dnsutils`

主机名的解析流程为：

1.  `/etc/nsswitch.conf` 文件里的 `hosts: files dns` 这段规定主机名解析顺序。（代替 `/etc/host.conf` 文件里的 `order` 这段原有的功能。）
1.  `files` 方式首先被调用。在 `/etc/hosts` 文件里面寻找主机名。（`/etc/host.conf` 文件包含 `multi on`。)
1.  `dns` 方式被调用。查询 `/etc/resolv.conf` 文件里面写的互联网域名系统（Domain Name System，DNS）。

下面则是一些其他配置：

-   如果有永久 IP 地址，文件 `/etc/hosts` 内应该有一行如下：

    ```
    93.184.216.34 hostname.example.com hostname
    ```

-   如果 `resolvconf` 软件包没有安装，`/etc/resolv.conf` 是一个静态文件。
-   对于典型 adhoc 局域网环境下的 PC 工作站，除了基本的 `files` 和 `dns` 方式之外，主机名还能够通过 Multicast DNS（mDNS）进行解析。

    -   `libnss-mdns` 插件包提供 mDNS 的主机名解析，GNU C 库（glibc）的 GNU 名字服务转换 Name Service Switch（NSS）功能支持 mDNS。
    -   此时 `/etc/nsswitch.conf` 文件应当有像 `hosts: files mdns4_minimal [NOTFOUND=return] dns` 这样的一段（其它配置参见 `/usr/share/doc/libnss-mdns/README.Debian`）。

-   可以使用 `systemd` 提供的 NSS (Name Service Switch) 模块来替代传统的网络主机名解析方式。

    -   可以联合的模块：`libnss-resolve`、`libnss-myhostname`、`libnss-mymachines`
    -   更多信息参见 `nss-resolve(8)`、`systemd-resolved(8)`、`nss-myhostname(8)` 和 `nss-mymachines(8)`

-   `systemd` 使用 `enp0s25` 之类的“可预测网络接口名称”。
-   私有网络地址范围：`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`

---

2. 现代的桌面网络配置
---------------------

对于使用 `systemd` 的现代 Debian 桌面系统，网络接口通常由两个服务进行初始化：`lo` 接口通常在 `networking.service` 处理，而其它接口则由 `NetworkManager.service` 处理。

-   Debian 可以通过 daemon 管理软件来管理网络连接，例如 `network-manager` 和相关软件包。

    !!! tip "注意（只在 Dibian 系操作系统上）"

        不要在服务器上使用自动网络配置工具。它们主要针对于笔记本电脑上的移动桌面用户。

传统 `ifupdown` 软件包的配置文件位于 `/etc/network/interfaces`。

### 2.1. 图形界面的网络配置工具

Debian 系统 NM 的官方文档位于 `/usr/share/doc/network-manager/README.Debian`。

如下操作即可完成桌面环境的网络配置：

1.  使桌面用户 foo 归属 “netdev” 组（GNOME 和 KDE 这样的现代桌面环境会通过 D-bus 自动完成该操作）

    ``` bash
    sudo usermod -a -G foo netdev
    ```

1.  使 `/etc/network/interfaces` 的配置保持简洁

    ```
    auto lo
    iface lo inet loopback
    ```

1.  重启 NM 后，用图形界面配置网络

!!! note "注意"

    只有**不**列在 `/etc/network/interfaces` 中的接口会被 NM 管理，以避免与 `ifupdown` 的冲突。

!!! tip "提示"

    如果你想扩展 NM 的网络配置功能，请寻找适当的插件模块和补充软件包，例如 `network-manager-openconnect`、`network-manager-openvpn-gnome`、`network-manager-pptp-gnome`、`mobile-broadband-provider-info`、`gnome-bluetooth` 等等。

### 2.2. 没有图形界面的网络配置

使用 `systemd` 的系统中，可以在 `/etc/systemd/network/` 里配置网络。参见 `systemd-resolved(8)`、`resolved.conf(5)` 和 `systemd-networkd(8)`。

-   DHCP 客户端（静态网络）的配置可以通过创建 `/etc/systemd/network/dhcp.network`（`.../static.network`）文件来进行设置

    === ":octicons-file-code-16: /etc/systemd/network/dhcp.network"
    
        ```
        [Match]
        Name=en*
        
        [Network]
        DHCP=yes
        ```
    
    === ":octicons-file-code-16: /etc/systemd/network/static.network"
    
        ```
        [Match]
        Name=en*
        
        [Network]
        Address=192.168.0.15/24
        Gateway=192.168.0.1
        ```

### 2.3. 现代云网络配置

云的现代网络配置可以使用 `cloud-init` 和 `netplan.io` 软件包。

-   参见：`netplan(5)`，`netplan-generate(8)` 和 `netplan-apply(8)`。
-   也可以参见 [Cloud-init documentation][cloudinit]（特别是围绕 "Configuration sources" 和 "Netplan Passthrough"）了解 `cloud-init` 是怎样能够集成替代的数据源到 `netplan.io` 配置。

  [cloudinit]: https://cloudinit.readthedocs.io/en/latest/index.html

---

3. 底层网络配置
---------------

在 Linux 上的底层网络配置，使用 `iproute2` 程序（`ip(8)`）。

### 3.1. `iproute2` 命令

-   从旧的 net-tools 命令集到新的 iproute2 命令集转换表：

    | 旧的 `net-tools` | 新的 `iproute2` |
    | :--------------: | :-------------: |
    |`ifconfig(8)`     | `ip addr`       |
    |`route(8)`        | `ip route`      |
    |`arp(8)`	       | `ip neigh`      |
    |`ipmaddr`         | `ip maddr`      |
    |`iptunnel `       | `ip tunnel`     |
    |`nameif(8)`       | `ifrename(8)`   |
    |`mii-tool(8)`     | `ethtool(8)`    |

参见 `ip(8)` 和 [Linux 高级路由和流量控制（Linux Advanced Routing & Traffic Control）][lartc]

  [lartc]: https://lartc.org/

### 3.2. 底层网络命令列表

你可以按下面的方式安全的使用底层网络命令，这些命令不会改变网络配置。

-   网络接口和地址管理：`ip addr show`、`ip route show`、`route -n`
-   ARP缓存管理：`arp`、`ip neigh`
-   网络连接测试：`ping yahoo.com`、`traceroute yahoo.com`、`tracepath yahoo.com`、`mtr yahoo.com`
-   DNS查询：`dig [@dns-server.com] example.com [{a|mx|any}]`、`whois yahoo.com`、`dlint example.com`
-   网络连接和端口监控：`netstat -a`、`netstat -l --inet`、`netstat -ln --tcp`
-   防火墙管理：`iptables -L -n`
-   PPP连接管理：`plog`

---

4. 网络优化
-----------

通用的网络优化超出了本文的范围。仅提及消费等级连接相关的主题。

-   **网络优化工具列表**

    -   详细分析单个连接：`iftop`
    -   需要测试最大带宽：`iperf`
    -   需要长期监控：`bmon` 或 `bwm-ng`
    -   快速检查状态：`ifstat`

-   找出最佳 MUT
    -   路径 MTU (PMTU) 发现的测试命令：

        ``` bash
        ping -4 -c 1 -s $((1500-28)) -M do www.debian.org
        ping -6 -c 1 -s $((1500-48)) -M do www.debian.org
        ```

    -   `tracepath(8)` 能自动完成 PMTU 发现机制
    -   最大分片大小 (MSS) 是另外一种衡量包大小的方法

!!! tip "注意"

    基于 `iptables(8)` 的优化，能够通过 MSS 来压缩包大小，路由器会用到 MMS 。参见 `iptables(8)` 中的“TCPMSS”。

5. Netfilter 网络过滤框架
-------------------------

Netfilter 是 Linux 内核模块提供的网络包过滤框架，提供*状态防火墙*和*网络地址转换（NAT）*功能。
