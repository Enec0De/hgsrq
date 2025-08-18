---
title: 静态网络配置
---

静态 IP 配置实践 { id="network" }
=================================

> 创建于：2025-08-09 | 最后更新：2025-08-19

---

简介说明 { id="introduction" }
------------------------------

在局域网中，我需要给特定机器设定固定的 IP（例如：192.168.1.2），实现设备的稳定访问，便于维护和管理。在此过程中，我同时也会将默认的网络管理工具（在本节中是 `ifupdown` 工具集） 改为 `NetworkManager`。

!!! danger "警告"

    修改网络配置可能会导致网络连接中断，建议在本地控制台操作。

---

前置条件 { id="prerequisites" }
-------------------------------

-   系统要求：Debian 12 (bookworm)
-   相关工具：`NetworkManager 1.42.4`

---

安装与配置 { id="installation-and-configuration" }
--------------------------------------------------

你可以根据下面提供的脚本，在终端执行操作[^1]，或修改并使用脚本实现配置。脚本思路如下：

1.  安装 `NetworkManager` 工具集并进行基础配置。
    -   安装 `network-manager` 包，并启用 `NetworkManager.service` 服务。
    -   修改 `NetworkManager.conf` 配置文件，使其可以接管 `ifupdown` 配置文件中管理的网卡[^2]。

1.  添加 `nmcli` 连接配置，设定静态 IP、网关和 DNS[^3]。
1.  卸载 `ifupdown` 工具集，删除相关服务文件，避免与 `NetworkManager` 冲突。
1.  最后重启以应用修改。

``` sh linenums="1" hl_lines="24-27 29-30 40-49 51-52 54-57"
#!/usr/bin/env sh
# Script Name: switch_network_management.sh
# Author: Aina
# Date Created: 2025-08-13 | Date Modified: 2025-08-13

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as an error and exit immediately
set -eu

# Check the permission
if [ $(id -u) -ne 0 ]; then
    echo 'This script must be run with `sudo`.'
    exit 1
fi

# Define variables
# Please change the following values according to your network environment
nm_conf="/etc/NetworkManager/NetworkManager.conf"
ip_addresses="192.168.1.2/24"
gateway="192.168.1.1"
dns="192.168.1.1"
interface_name="ens33"
connection_name="connection-${interface_name}"

# Install and enable NetworkManager
apt-get update 
apt-get install network-manager -y
systemctl enable NetworkManager.service

# Configure NetworkManager
sed -i.bak -e 's/^\(managed=\)false/\1true/' "${nm_conf}"

# Check for connection naming conflicts
for name in $(nmcli con show | awk 'NF=1 {print}'); do
    if [ ${name} = ${connection_name} ]; then
        echo "There is the connection name conflict."
        exit 1
    fi
done

# Add an Ethernet connection configuration
nmcli con add \
    type ethernet \
    con-name "${connection_name}" \
    ifname "${interface_name}" \
    ipv4.addresses "${ip_addresses}" \
    ipv4.gateway "${gateway}" \
    ipv4.dns "${dns}" \
    ipv4.method "manual" \
    connection.autoconnect-priority 100

# Purge ifupdown
apt-get purge ifupdown -y

# Log the reboot action
echo "All actions done, system will now reboot to apply change in 10s."
sleep 10
systemctl reboot
```

---

故障排查 { id="troubleshooting" }
---------------------------------

**1. 无法接管网络接口**

-   **问题描述：**

    执行 `nmcli dev set ens33 managed yes` 命令后没有反应，无法正常接管 `ens33` 网卡。

-   **原因分析：**

    如果没有执行 `reboot`，则需要手动停止其他网络相关服务，并重启 `NetworkManager` 服务，读取修改后的配置。

-   **解决方案：**

    手动停止 `ifup@ens33`、`networking` 等相关服务与进程，然后重启 `NetworkManager` 服务。

**2. 未卸载 `ifupdown` 工具集**

-   **问题描述：**

    在不卸载 `ifupdown` 工具集的情况下，重启后 `ens33` 有多个 IP。

-   **原因分析：**

    `ifupdown` 工具集内的 `ifup@.service` 服务，在每次开机的时候都会执行相关命令，尝试管理 `/etc/network/interfaces` 配置文件内描述的网络接口。

-   **解决方案：**

    修改 `/etc/network/interfaces` 配置文件，注释或者删除与 `ens33` 有关的内容。

---

附录：参考与链接 { id="appendix" }
--------------------------------

-   工具参考：[`man 1 nmcli`][nmcli]
-   配置文件参考：[`man 5 NetworkManager.conf`][conf]

[nmcli]: https://manpages.debian.org/bookworm/network-manager/nmcli.1.en.html
[conf]: https://manpages.debian.org/bookworm/network-manager/NetworkManager.conf.5.en.html

[^1]: 主要思路体现在高亮行代码。
[^2]: 该实践环境中，对应的网络接口名称为 `esn33`。
[^3]: 这里预计设定的 IP 为 192.168.1.2/24，网关和 DNS 为 192.168.1.1，均为私有网络地址。
