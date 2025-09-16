---
title: 系统升级与紧急降级
---

系统升级与紧急降级 { id="apt-advanced" }
========================================

> 创建于：2025-08-14 :octicons-chevron-right-16: 最后更新：2025-09-17

---

简介说明 { id="introduction" }
------------------------------

Debian 13 (trixie)[^1] 于近期发布。

本节将会记录系统全面更新的实践，并附加对单个软件包（`pip3`）进行紧急降级操作的演示。因为这些操作本身就很危险，因此不提供“故障排查”内容用于参考。建议在开始前请做好数据备份，出问题了直接重装系统。

!!! danger "警告"

    本页面只专注于全面更新与紧急降级的 ^^操作本身^^，不去考虑新发布系统的稳定性[^2]，是否使用新系统请自行判断。

### 前置条件 { id="prerequisites" }

-   系统要求：Debian 12 (bookworm)
-   相关工具：`dpkg`、`apt-get`、`apt-mark`、`apt-cache`、`apt`、`tmux`
-   数据源：[中科大镜像软件源][debian]、[中科大镜像软件安全更新源][debian-security]

---

全面更新 { id="upgrade" }
-------------------------

如果是远程连接，建议在 `tmux` 中运行下方脚本，防止网络波动导致更新失败。脚本思路如下：

1.  **十分重要**的 ^^前期安全检查工作^^（来自 [Release Notes for Debian 13][release-notes] 的建议）：

    ??? danger "进行全面更新前后你需要做的事情"
        
        -   使用脚本前：手动执行 `apt list '?narrow(?installed, ?not(?origin(Debian)))'` 命令，处理可能会出问题的包。
    
        -   更新系统后：手动执行 `apt purge '~o'`、`apt purge '~c'` 和 `apt autoremove` 命令，清理多余的包和配置文件。

    -   检查当前系统版本：确定你正在从 Debian 12 升级到 Debian 13。
    -   使用 `tar` 和 `dpkg` 工具备份重要数据。
    -   使用 `find`、`dpkg` 和 `apt-mark` 工具进行前期检查。

1.  修改 APT 系统数据源为[中科大镜像软件源][debian]与[中科大镜像软件安全更新源][debian-security]。
1.  开始执行更新系统的操作，更新后重启系统。

``` sh linenums="1" hl_lines="16-22 38-40 42-49 51-56 58-60 62-65"
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

---

紧急降级 { id="downgrade" }
---------------------------

如果你在生产环境中，发现新版本的 `pip3` 有 bug，需要回退，下面提供了一个具体实践用于演示如何对其降级。操作前请仔细阅读[文档][aptpinning]。这个操作很危险，建议结合 `apt-cache` 和 `apt policy` 工具严谨地使用这个技术。

!!! danger "实际使用这个技术之前你必须知道的事"

    降级在 Debian 设计上就不被官方支持。该操作只建议用于回退通过 `apt-pinning` 临时升级的 ^^非核心^^、^^低依赖^^ 软件。其他非常规、高风险的用法，极易产生系统依赖链的断裂，造成难以挽回的后果。

    对于重要系统，你应当备份所有重要数据，从零开始重新安装一个新的系统。


先确认降级前的系统状态与 `pip3` 的版本：

-   文件 `/etc/apt/preferences` 的内容如下所示。
-   使用 `apt policy` 工具可以检查当前软件包的选择优先级。

=== ":octicons-file-code-16: `/etc/apt/preferences`"

    ``` sh
    Explanation: Date Created: 2025-08-10 | Date Modified: 2025-08-14

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

=== ":octicons-terminal-16: terminal"

    ``` sh
    $ sudo apt policy python3-pip # Check the priority of pip3
    python3-pip:
      Installed: 25.1.1+dfsg-1
      Candidate: 25.1.1+dfsg-1
      Version table:
     *** 25.1.1+dfsg-1 700
             50 https://mirrors.ustc.edu.cn/debian trixie/main amd64 Packages
            100 /var/lib/dpkg/status
         23.0.1+dfsg-1 500
            500 https://mirrors.ustc.edu.cn/debian bookworm/main amd64 Packages
    $ pip3 -V # Check the version of pip3
    pip 25.1.1 from /usr/lib/python3/dist-packages/pip (python 3.11)
    ```

### 开始降级操作 { id="begin-downgrade" }

接下来我们开始进行版本回退操作：

1.  先修改 `/etc/apt/preferences` 的内容：

    ``` sh title="/etc/apt/preferences"
    Explanation: Date Created: 2025-08-14 | Date Modified: 2025-08-14
    
    Explanation: Emergency_downgrading  
    Package: *
    Pin: release n=bookworm*
    Pin-Priority: 1001
    ```

1.  执行 `sudo apt update` 后使用 `sudo apt full-upgrade` 命令开始降级，此时屏幕的输出如下（略去无关内容）：

    !!! danger "警告"

        请在每次修改好 `/etc/apt/preferences` 文件内容后，都执行一次执行 `sudo apt update` 以应用配置。

    ``` sh
    $ sudo apt update && sudo apt full-upgrade
    ...
    The following packages will be DOWNGRADED:
      python3-pip
    0 upgraded, 0 newly installed, 1 downgraded, 0 to remove and 0 not upgraded.
    ...
    Do you want to continue? [Y/n] y # Enter `y' to continue.
    Get:1 https://mirrors.ustc.edu.cn/debian bookworm/main amd64 python3-pip all 23.0.1+dfsg-1 [1,325 kB]
    Fetched 1,325 kB in 1s (1,883 kB/s)
    dpkg: warning: downgrading python3-pip from 25.1.1+dfsg-1 to 23.0.1+dfsg-1
    (Reading database ... 41913 files and directories currently installed.)
    Preparing to unpack .../python3-pip_23.0.1+dfsg-1_all.deb ...
    Unpacking python3-pip (23.0.1+dfsg-1) over (25.1.1+dfsg-1) ...
    ...
    ```

1.  上述命令执行完成后，你可以检查你的 `pip3` 版本：
 
    ``` sh
    $ pip3 -V # Check the version of pip3
    pip 23.0.1 from /usr/lib/python3/dist-packages/pip (python 3.11)
    ```

---

附录：参考与链接 { id="appendix" }
----------------------

-   APT pinning 参考：[`man 5 apt_preferences`][aptpinning]

[debian]: https://mirrors.ustc.edu.cn/help/debian.html "Debian - USTC Mirror Help"
[debian-security]: https://mirrors.ustc.edu.cn/help/debian-security.html "Debian Security - USTC Mirror Help"
[aptpinning]: https://manpages.debian.org/bookworm/apt/apt_preferences.5.en.html "APT_PREFERENCES(5)"
[release-notes]: https://www.debian.org/releases/trixie/release-notes/index.html "Release Notes for Debian 13 (trixie)"

[^1]: Debian 13 是在 2025 年 8 月 9 日正式发布的。
[^2]: Debian 官方手册中有建议：只在主版本发布了一个月且你已经评估了形势之后，才更新到新版本。
