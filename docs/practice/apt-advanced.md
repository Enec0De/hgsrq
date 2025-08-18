---
title: 系统升级与紧急降级
---

系统升级与紧急降级 { id="apt-advanced" }
========================================

> 创建于：2025-08-14 | 最后更新：2025-08-19

---

简介说明 { id="introduction" }
------------------------------

刚好最近 Debian 13 (trixie)[^1]发布，我打算乘此机会实践一次系统的全面更新与紧急降级操作。

!!! danger "警告"

    本页面的操作只专注于全面更新与紧急降级的*操作本身*，不去考虑新发布系统的稳定性[^2]，是否使用请自行判断。

---

前置条件 { id="prerequisites" }
-------------------------------

-   系统要求：Debian 12 (bookworm)
-   相关工具：`dpkg`、`apt-get`、`apt-mark`、`apt-cache`、`apt`、`tmux`
-   使用的数据源：[中科大镜像软件源][debian]、[中科大镜像软件安全更新源][debian-security]

---

全面更新 { id="upgrade" }
-------------------------

如果是远程连接，建议在 `tmux` 中运行下方脚本，防止网络波动导致更新失败。脚本思路如下：

1.  **十分重要**的前期安全检查工作（建议来自 [Release Notes for Debian 13][release-notes]）：
    -   检查当前系统版本。
    -   使用 `tar` 和 `dpkg` 工具备份重要数据。
    -   使用 `find`、`dpkg` 和 `apt-mark` 工具进行前期检查。

1.  修改 APT 系统数据源。
1.  开始更新系统。
1.  最后重启系统。

??? danger "进行全面更新前后你需要做的事情"
    
    -   使用脚本前：手动执行 `apt list '?narrow(?installed, ?not(?origin(Debian)))'` 命令，处理可能会出问题的包。

    -   更新系统后：手动执行 `apt purge '~o'`、`apt purge '~c'` 和 `apt autoremove` 命令，清理多余的包和配置文件。

``` sh linenums="1" hl_lines="15-21 37-39 41-48 50-55 57-59 61-64"
#!/usr/bin/env sh
# Script Name: upgrading_the_system.sh
# Author: Aina
# Date Created: 2025-08-15 | Date Modified: 2025-08-15

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as an error and exit immediately
set -eu

# Check the permission
if [ $(id -u) -ne 0 ]; then
    echo 'This script must be run with `sudo`.'
    exit 1
fi

# Check the debian_version
if [ "$(awk -F '.' '{print $1}' /etc/debian_version)" -eq 12 ]; then
    echo "Your system will upgrade from Debian 12."
else
    echo "Check your debian_version!"
    exit 1
fi

# Define variables
folder_path="${HOME}/upgrade.bak"
backup_file="${folder_path}/etc_dpkg_apt.bak.tar.gz"
etc_file="/etc"
dpkg_file="/var/lib/dpkg"
apt_file="/var/lib/apt/extended_states"
pkglist_file="${folder_path}/packages.txt"
source_file="/etc/apt/sources.list.d/debian.sources"

# Check the existence of the directory
if [ ! -d "${folder_path}" ]; then
    mkdir -p "${folder_path}"
fi

# Any package installation operation must be run with superuser privileges
tar -czf "${backup_file}" "${etc_file}" "${dpkg_file}" "${apt_file}" 
dpkg --get-selections '*' > "${pkglist_file}"

# Removing leftover files from previous upgrades and check the packages status
lfiles=$(find /etc -name '*.dpkg-*' -o -name '*.ucf-*' -o -name '*.merge-error')
audit=$(dpkg --audit)
showhold=$(apt-mark showhold)
if [ -n "${lfiles}" -o -n "${audit}" -o -n "${showhold}" ]; then
    echo "Some problems need to be fixed."
    exit 1
fi

# Edit APT sources files
if [ ! -f "${source_file}" ]; then 
    echo "check the file ${source_file}"
    exit 1
fi
sed -i.bak -e 's/bookworm/trixie/g' "${source_file}"

# Upgrading the system
apt-get update
apt-get dist-upgrade -y

# Log the reboot action
echo "All actions done, system will now reboot to apply change in 10s."
sleep 10
systemctl reboot
```

紧急降级 { id="downgrade" }
---------------------------

如果你在生产环境中发现新版本 `pip3` 的特性有 bug，下面提供了一个具体实践用于紧急降级。请仔细阅读[文档][aptpinning]，并结合 `apt-cache` 和 `apt policy` 命令严谨地使用这个技术。

??? danger "实际使用这个技术之前你必须知道的事"

    降级在 Debian 设计上就不被官方支持。该操作只建议用于回退通过 `apt-pinning` 临时升级的*非核心*、*低依赖*软件。其他非常规、高风险的用法，极易产生系统依赖链的断裂，造成难以挽回的后果。

    对于重要系统，你应当在恢复操作后备份所有重要数据，并从零开始重新安装一个新的系统。

=== ":octicons-file-code-16: Latest version of pip3"

    ``` sh title="/etc/apt/preferences"
    Explanation: Date Created: 2025-08-14 | Date Modified: 2025-08-14

    Explanation: Install only the most recent trixie version of pip3
    Package: python3-pip
    Pin: release n=trixie*
    Pin-Priority: 700
    

    Explanation: Install package if it is selected for installation
    Explanation: and no version of the package is already installed
    Package: *
    Pin: release n=trixie*
    Pin-Priority: 50
    ```

=== ":octicons-file-code-16: Downgrade the pip3"

    ``` sh title="/etc/apt/preferences"
    Explanation: Date Created: 2025-08-14 | Date Modified: 2025-08-14

    Explanation: Emergency_downgrading  
    Package: *
    Pin: release n=bookworm*
    Pin-Priority: 1001
    ```

<!-- -->

=== ":octicons-terminal-16: Latest version of pip3"

    ``` sh
    # Check the priority of pip3
    $ apt policy python3-pip
    python3-pip:
      Installed: 25.1.1+dfsg-1
      Candidate: 25.1.1+dfsg-1
      Version table:
     *** 25.1.1+dfsg-1 700
             50 https://mirrors.ustc.edu.cn/debian trixie/main amd64 Packages
            100 /var/lib/dpkg/status
         23.0.1+dfsg-1 500
            500 https://mirrors.ustc.edu.cn/debian bookworm/main amd64 Packages


    # Check the version of pip3
    $ pip3 -V
    pip 25.1.1 from /usr/lib/python3/dist-packages/pip (python 3.11)
    ```
=== ":octicons-terminal-16: Downgrade the pip3"

    ``` sh
    $ sudo apt full-upgrade
    Reading package lists... Done
    Building dependency tree... Done
    Reading state information... Done
    Calculating upgrade... Done
    The following packages will be DOWNGRADED:
      python3-pip
    0 upgraded, 0 newly installed, 1 downgraded, 0 to remove and 0 not upgraded.
    Need to get 1,325 kB of archives.
    After this operation, 3,572 kB disk space will be freed.
    Do you want to continue? [Y/n] y
    Get:1 https://mirrors.ustc.edu.cn/debian bookworm/main amd64 python3-pip all 23.
    0.1+dfsg-1 [1,325 kB]
    Fetched 1,325 kB in 1s (1,883 kB/s)
    dpkg: warning: downgrading python3-pip from 25.1.1+dfsg-1 to 23.0.1+dfsg-1
    (Reading database ... 41913 files and directories currently installed.)
    Preparing to unpack .../python3-pip_23.0.1+dfsg-1_all.deb ...
    Unpacking python3-pip (23.0.1+dfsg-1) over (25.1.1+dfsg-1) ...
    Setting up python3-pip (23.0.1+dfsg-1) ...
    Processing triggers for man-db (2.11.2-2) ...
    
    $ pip3 -V
    pip 23.0.1 from /usr/lib/python3/dist-packages/pip (python 3.11)
    ```

---

附录：参考与链接 { id="appendix" }
----------------------

-   APT pinning 参考：[`man 5 apt_preferences`][aptpinning]

[debian]: https://mirrors.ustc.edu.cn/help/debian.html "Debian - USTC Mirror Help"
[debian-security]: https://mirrors.ustc.edu.cn/help/debian-security.html "Debian Security - USTC Mirror Help"
[aptpinning]: https://manpages.debian.org/trixie/apt/apt_preferences.5.en.html "APT_PREFERENCES(5)"
[release-notes]: https://www.debian.org/releases/trixie/release-notes/index.html "Release Notes for Debian 13 (trixie)"

[^1]: Debian 13 是在 2025 年 8 月 9 日正式发布的。
[^2]: Debian 官方手册中有建议：只在主版本发布了一个月且你已经评估了形势之后，才更新到新版本。
