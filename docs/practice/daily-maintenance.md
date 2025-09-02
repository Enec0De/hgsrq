---
title: 日常运维工作
---

日常运维工作 { id="daily-maintenance" }
=======================================

> 创建于：2025-08-24 | 最后更新：2025-09-02

---

简介说明 { id="introduction" }
------------------------------

部署好 Nginx 服务之后，需要进行日常的维护工作，这一页会记录这些工作一般会干什么。

---

前置条件 { id="prerequisites" }
-------------------------------

-   系统要求：Debian 12 (bookworm)
-   相关工具：`top`、`ps`、`du`、`df`、`free`、`iostat`、`vmstat`、`sar`、`ss`

---

安装与配置 { id="installation-and-configuration" }
--------------------------------------------------

可以在执行脚本前，使用 `top` 命令，先后按下 ++p++ 和 ++m++ 排序观察系统 CPU、内存资源，或按下 ++l++ 快速锁定 `Nginx` 相关进程，速览服务器当前进程状况。

``` sh linenums="1"
#!/usr/bin/env sh
# Script Name: nginx_maintenance.sh
# Author: Aina
# Data Created: 2025-08-25 | Data Modified: 2025-09-02

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as an error and exit immediately
set -eu

# Define variables
log_dir="/var/log/nginx"
current_date="$(date -I)"
report_dir="${HOME}/maintenance_reports"
report_file="${report_dir}/log_${current_date}.log"
export website_dir="/var/www/html"

mkdir -p "${report_dir}"

print_head() {
    head_text="Outputs of the command \`${1}':"
    echo "${head_text}"
    printf "%0.s-" $(seq 1 $(expr length "${head_text}"))
    echo "\n\n\`\`\` sh"
}

command_exist() {
    command -v "${1}" > /dev/null 2>&1
    echo "${1} processing ..."
}

check_status() {
    if command_exist ${1}; then
        print_head "${1}" >> "${report_file}"
        /usr/bin/env sh -euc "${1}" >> "${report_file}"
        echo "\`\`\`\n" >> "${report_file}"
    else
        echo "Command \`${1}' not found." >> "${report_file}"
    fi
}

# Check system resources and disk usage
check_status 'uptime'
check_status 'free -h'
check_status 'dmesg | tail -n 20'
check_status 'vmstat 1 4'
check_status 'df -h'
check_status 'du -h -d 1 "${website_dir}" | sort -rh | head -n 10'

# Check process status
check_status 'ps aux | grep [n]ginx'
check_status 'ps aux --sort=%cpu | head -n 10'
check_status 'ps aux --sort=%mem | head -n 10'

# Check network status
check_status 'ss -s'
check_status 'ss -tunlp'

# Performance monitoring commands
# check_status 'iostat -x 1 3'
# check_status 'sar -u 1 3'
# check_status 'sar -r 1 3'

```

---

故障排查 { id="troubleshooting" }
---------------------------------

**1. 某些字段无法正常显示**

-   **问题描述：**

    在收集到的日志中，某些字段无法正常显示。如 `ss -tunlp` 的 **process** 字段为空。

-   **原因分析：**

    通常是权限不足或系统限制导致。

-   **解决方案：**

    优先通过 `sudo` 提升权限解决，如果无效，再排查 `AppArmor` / `SELinux`。

---

附录：参考与链接 { id="appendix" }
----------------------------------

-   基本系统资源相关：[`man 1 top`][top]、[`man 1 uptime`][uptime]、[`man 1 free`][free]、[`man 1 dmesg`][dmesg]、[`man 8 vmstat`][vmstat]
-   磁盘空间状态相关：[`man 1 du`][du][`man 1 df`][df]
-   进程与网络状态相关：[`man 1 ps`][ps]、[`man 8 ss`][ss]

[ss]: https://manpages.debian.org/bookworm/iproute2/ss.8.en.html
[vmstat]: https://manpages.debian.org/bookworm/procps/vmstat.8.en.html
[df]: https://manpages.debian.org/bookworm/coreutils/df.1.en.html
[du]: https://manpages.debian.org/bookworm/coreutils/du.1.en.html
[free]: https://manpages.debian.org/bookworm/procps/free.1.en.html
[top]: https://manpages.debian.org/bookworm/procps/top.1.en.html
[ps]: https://manpages.debian.org/bookworm/procps/ps.1.en.html
[uptime]: https://manpages.debian.org/bookworm/procps/uptime.1.en.html
[dmesg]: https://manpages.debian.org/bookworm/util-linux/dmesg.1.en.html
