---
title: 配置 Nginx
---

配置 Nginx { id="nginx" }
=============================

> 创建于：2025-08-16 | 最后更新：2025-08-23

---

简介说明 { id="introduction" }
------------------------------

配置 Nginx 服务，并获取 Let's Encrypt 证书。

---

前置条件 { id="prerequisites" }
-------------------------------

-   系统要求：Debian 12 (bookworm)
-   相关工具：`Nginx 1.22.1`、`certbot`、`crontab`、`systemd`
---

安装与配置 { id="installation-and-configuration" }
--------------------------------------------------

安装并获取 ssl 证书的步骤相对简单，执行下方脚本即可完成所有操作。同时，在脚本下方提供了 Nginx 的配置文件内容，分为*主要配置*和*可选配置*：

-   *主要配置*的服务块让 Nginx 通过 HTTPS 协议为 `example.com` 域名提供网页服务。
-   *可选配置*包含三个服务块，从上到下的行为分别是：
    1. 监听 HTTP 请求，通过 301 将其永久重定向到 HTTPS
    1. 对非匹配域名访问的 HTTPS 请求直接拒绝握手
    1. 对非匹配域名访问的 HTTP 请求直接关闭连接

*主要配置*保证了 Nginx 可以提供基础的网页服务，*可选配置*提高了访问的安全性。建议在实际生产环境中，添加使用全部配置。

``` sh linenums="1" hl_lines="16-17 19-24"
#!/usr/bin/env sh
# Script Name: set_the_letencrypt.sh
# Author: Aina
# Date Created: 2025-08-17 | Date Modified: 2025-08-19

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as an error and exit immediately
set -eu

# Check the permission
if [ $(id -u) -ne 0 ]; then
    echo 'This script must be run with `sudo`.'
    exit 1
fi

# Install the relavant package
apt-get install nginx certbot python3-certbot-nginx

# Check the PATH and create the Certificate
if command -v nginx > /dev/null; then
    certbot certonly --nginx -d example.com
else
    echo "There is no /sbin included in PATH."
fi


```

=== ":octicons-file-code-16: `/etc/nginx/sites-available/default`: 主要"

    ``` nginx linenums="1"
    # Date Created: 2025-08-17 | Date Modified: 2025-08-23

    # HTTPS server configuration
    #
    server {
        listen 443 ssl;
        listen [::]:443 ssl;
    
        # SSL configuration
        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
        # SSL optimal settings
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
        root /var/www/html;
        index index.html;
    
        server_name example.com;

        location / {
            try_files $uri $uri/ =404;
        }

        error_page 404 /404.html;

        location = /404.html {
            internal;
        }
    }
    ```

=== ":octicons-file-code-16: `/etc/nginx/sites-available/default`: 可选"

    ``` nginx linenums="32"
    # Date Created: 2025-08-17 | Date Modified: 2025-08-23

    server {
        listen 80;
        listen [::]:80;
    
        server_name example.com;
    
        # Examine the host example.com and redirect it to HTTPS
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
    
        server_name _;
    
        # Reject SSL/TLS handshake
        ssl_reject_handshake on;
    }    
    
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
    
        server_name _;
    
        # Close the connection immediately
        return 444;
    }
    ```

---

故障排查 { id="troubleshooting" }
---------------------------------

**1. 网页可以访问但无法正常渲染**

-   **问题描述：**

    通过域名访问网页，无法正常渲染（如样式丢失、脚本失效、图片不显示等）。

-   **原因分析：**

    可能是静态资源加载失败，或是 MIME 类型配置缺失。前者的原因是 Nginx 没有网页资源的读取权限，使得资源无法被访问；后者的原因是 Nginx 无法正确识别文件类型，将其当作默认的 `text/plain` 处理，无法解析（例如 CSS 不生效、JS 无法执行）。

-   **解决方案：**

    检查 `/var/log/nginx` 下的 `access.log` 和 `error.log` 日志文件，查看是否有权限报错。如果有，则需要设置相关文件的权限，使得 **www-data** 用户至少有读权限。进一步检查 Nginx 配置中是否包含 `include /etc/nginx/mime.types;` 内容，通常在 `/etc/nginx/nginx.conf` 内的 `http` 上下文当中。以上两个操作都需要重启 Nginx 服务以应用改动。

**2. 浏览器提示连接不安全**

-   **问题描述：**

    浏览器提示 "连接不安全"。

-   **原因分析：**

    正常情况下，这可能是证书过期或未生效，或者证书与域名不匹配。非正常情况，就是网站存在安全风险，可能有中间人篡改网页内容。

-   **解决方案：**

    `certbot` 一般都会通过 `crontab` 或者 `systemd.timer` 自动续期证书，相应配置在安装和获取证书时会自动安装，但是需要你手动重启 Nginx 服务重载证书。如果你不想手动重启 Nginx 服务，可以在自动续期的命令中加上 `--deploy-hook "systemctl reload nginx"` 选项。证书与域名不匹配的情况，可能是用户直接通过了 IP 来访问网页，建议只通过对应的域名访问网页。如果网页被中间人篡改了，请通知用户停止访问该网页的内容，并暂时关闭网页。

---

附录：参考与链接 { id="appendix" }
----------------------------------

-    快速开始：[Nginx - Beginner’s Guide][nginx]
-    证书相关：[Let's Encrypt][letsencrypt]
-    Certbot 官方文档：[Certbot Document][certbot]

[nginx]: https://nginx.org/en/docs/beginners_guide.html "Beginner's Guide"
[letsencrypt]: https://letsencrypt.org/docs/ "Documentation - Let's Encrypt"
[certbot]: https://eff-certbot.readthedocs.io/en/stable/ "Certbot documentation"
