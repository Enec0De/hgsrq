---
title: 流量过滤与重定向
---

流量过滤与重定向 { id="nftables" }
==================================

> 创建于：2025-09-03 | 最后更新：2025-09-08

---

简介说明 { id="introduction" }
------------------------------

本页将使用 `nft` 工具实现两个目标：

1. 开放基础的 22 (ssh), 443 (https) 号端口；
1. 将 80 (http) 号端口的流量重定向到 8000 端口，用于测试。

---

前置条件 { id="prerequisites" }
-------------------------------

-   系统要求：Debian 12 (bookworm)
-   相关工具：`nftables 1.0.6`

---

安装与配置 { id="installation-and-configuration" }
--------------------------------------------------

下方提供了三个文件：

1.  `nftables.sh`：

    实现 `nftables` 配置的 shell 脚本，你可以跟着脚本手操。

1.  `/etc/nftables.conf`：

    实现 `nftables` 配置的配置文件，这种方式的实现，可以让其原子地生效。

1.  `/etc/nginx/sites-available/proxy`：

    额外提供使用 Nginx 在应用层实现流量重定向的方法，而非网络层（以 `nftables` 的方式）。

=== ":octicons-file-code-16: nftables.sh"

    ``` sh linenums="1"
    #!/usr/bin/env sh
    # Script Name: nftables.sh
    # Author: Aina
    # Data Created: 2025-09-03 | Data Modified: 2025-09-08
    
    # Exit immediately if a command exits with a non-zero status
    # Treat unset variables as an error and exit immediately
    set -eu
    
    # Check the permission
    if [ $(id -u) -ne 0 ]; then
        echo 'This script must be run with `sudo`.'
        exit 1
    fi
    
    # Flush the Ruleset
    nft flush ruleset
    
    # Add Tables
    nft add table inet filter
    nft add table inet nat
    
    # Register Hooks
    nft add chain inet filter input '{
        type filter hook input priority filter; policy drop;
        }'
    
    nft add chain inet filter forward '{
        type filter hook forward priority filter; policy drop;
        }'
    
    nft add chain inet filter output '{
        type filter hook output priority filter; policy accept;
        }'
    
    nft add chain inet nat prerouting '{
        type nat hook prerouting priority dstnat; policy accept;
        }'
    
    nft add chain inet nat postrouting '{
        type nat hook postrouting priority srcnat; policy accept
        }'
        
    # Add Rules in Input Hook
    nft add rule inet filter input ct state established,related accept
    nft add rule inet filter input iif lo accept
    nft add rule inet filter input tcp dport \{ 22, 443, 8000 \} accept

    # Log the dropped packets
    nft add rule inet filter input \
        log prefix \"nftables INPUT drop: \" limit rate 10/second
    
    # Add Rule in Prerouting Hook
    nft add rule inet nat prerouting tcp dport 80 redirect to :8000
    ```

=== ":octicons-file-code-16: /etc/nftables.conf"

    ``` sh linenums="1"
    #!/usr/sbin/nft -f
    # Script Name: nftables.conf
    # Author: Aina
    # Data Created: 2025-09-03 | Data Modified: 2025-09-08

    flush ruleset

    table inet filter {
            chain input {
                    type filter hook input priority filter; policy drop;
                    ct state established,related accept
                    iif "lo" accept
                    tcp dport { 22, 443, 8000 } accept
                    log prefix "nftables INPUT drop: " limit rate 10/second
            }
    
            chain forward {
                    type filter hook forward priority filter; policy drop;
            }
    
            chain output {
                    type filter hook output priority filter; policy accept;
            }
    }
    table inet nat {
            chain prerouting {
                    type nat hook prerouting priority dstnat; policy accept;
                    tcp dport 80 redirect to :8000
            }
    
            chain postrouting {
                    type nat hook postrouting priority srcnat; policy accept;
            }
    }
    ```

=== ":octicons-file-code-16: sites-available/proxy"

    ``` nginx
    server {
            listen 80;
    
            server_name example.com;
    
            location / {
                    proxy_pass http://localhost:8000;
                    proxy_set_header Host $host;
            }
    }
    ```

---

故障排查 { id="troubleshooting" }
---------------------------------

**1. 在仅开放 80 端口的情况下，无法正常访问服务**

-   **问题描述：**

    在 nftables 中配置好 PREROUTING 链中 80 端口到 8000 端口的重定向后，只开放 80 端口而不开放 8000 端口，此时无法正常访问服务，如 `curl http://192.168.1.2` 无回应。

-   **原因分析：**

    对于外部访问的流量，PREROUTING 链的处理先于 INPUT 链，所以流量从 80 端口到 8000 端口的重定向操作，比它进入 INPUT 链要早。当它进入 INPUT 链时，其目标端口已经重定向为 8000 了，此时在 INPUT 链中应匹配的是 8000 端口而非 80。

-   **解决方案：**

    保证在 INPUT 链中开放 8000 端口。


**2. 在 `tcpdump` 中只能看到 80 端口的流量。**

-   **问题描述：**

    在使用 `tcpdump` 工具抓包时，即便在 nftables 中配置好了 PREROUTING 链中 80 端口到 8000 端口的重定向，依然只能看到目标端口为 80 的流量。

-   **原因分析：**

    这是正常现象。对于来自外部的请求，`tcpdump` 先于 PREROUTING 链处理流量，因此“只能看到目标端口为 80 的流量”。在 PREROUTING 处理完流量后，所有的请求都重定向为 8000 端口，所以要在 INPUT 链中“开放 80 端口”。这两者并不矛盾。

-   **解决方案：**

    正常现象无需修改。

---

附录：参考与链接 { id="appendix" }
--------------------------------

-   官方文档：[`man 8 nft`][nft]、[nftables wiki Main Page][nftwiki]、[The netfilter.org project][netfilter]
-   外部参考：[nftables - ArchWiki][nftarch]

[nft]: https://manpages.debian.org/bookworm/nftables/nftables.8.en.html "NFT(8)"
[nftwiki]: https://wiki.nftables.org/wiki-nftables/index.php/Main_Page "nftables wiki"
[nftarch]: https://wiki.archlinux.org/title/Nftables "nftables - ArchWiki"
[netfilter]: https://www.netfilter.org/ "netfilter"
