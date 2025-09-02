---
title: 密钥操作与文件同步 
---

密钥操作与文件同步 { id="ssh-rsync" }
=====================================

> 创建于：2025-08-20 | 最后更新：2025-09-02

---

简介说明 { id="introduction" }
------------------------------

配置开发环境中的用户与组，通过生成并配置密钥的方式，实现 `ssh` 免密登录，最后利用 `rsync` 工具远程同步目标主机与本地主机的特定文件内容，部署更新后的网页文件让 Nginx 读取。

---

前置条件 { id="prerequisites" }
-------------------------------

-   系统要求：Debian 12 (bookworm)
-   相关工具：`openssh-client 9.2p1`、`openssh-server 9.2p1`、`rsync 3.2.7`

---

安装与配置 { id="installaiton-and-configuration" }
--------------------------------------------------

1.  按 `user_and_group.sh` 脚本中的方式在远程主机为开发人员创建账户。
1.  如 `generate_ssh_key.sh` 脚本所示在本地主机设定好密钥，配置好 `config` 并同步文件。
    -   这里为了简化操作，没有给密钥设定密码。实际生产环境中，为了安全，建议设定密码并配合 `ssh-agent` 使用，并在配置好密钥后关闭远程服务器的密码登录方式。
    -   脚本中 33、34 行开头都各有一个制表符，如果是直接复制脚本使用，需要注意这一点。

!!! note "注意"

    脚本 `user_and_group.sh` 必须要用 `sudo` 权限执行，`generate_ssh_key.sh` 则不必。 

=== ":octicons-file-code-16: user_and_group.sh"

    ``` sh linenums="1" hl_lines="22-25 27-31 37-45"
    #!/usr/bin/env sh
    # Script Name: user_and_group.sh
    # Author: Aina
    # Date Created: 2025-08-20 | Date Modified: 2025-08-23
    
    # Exit immediately if a command exits with a non-zero status
    # Treat unset variables as an error and exit immediately
    set -eu

    # Check the permission
    if [ $(id -u) -ne 0 ]; then
        echo 'This script must be run with `sudo`.'
        exit 1
    fi
    
    # Difine variables
    username=${1:?Plesae enter the username.}
    passwd="123456"
    project_dir="/var/www/html"
    hash="$(openssl passwd -6 "${passwd}")"
    
    # Create the group
    if ! getent group developers >/dev/null; then
        groupadd -g 2000 developers
    fi
    
    # Create the user
    if ! id -u "${username}" >/dev/null 2>&1; then 
        useradd -u 5000 -s /usr/bin/bash -g developers\
                -G sudo -p "${hash}" -m ${username}
    fi
    
    usermod -aG developers www-data
    chage -d 0 ${username}
    chmod -R 700 /home/${username}
    
    # Set permissions for the project directory
    if [ ! -d "${project_dir}" ]; then
        echo "${project_dir} not exists."
        exit 1
    fi
    
    chgrp -R developers "${project_dir}"
    chmod -R 770 "${project_dir}"
    chmod g+s "${project_dir}"
    ```
    
=== ":octicons-file-code-16: generate_ssh_key.sh"

    ``` sh linenums="1" hl_lines="22-27 29-30 32-35"
    #!/usr/bin/env sh
    # Script Name: generate_ssh_key.sh
    # Author: Aina
    # Date Created: 2025-08-20 | Date Modified: 2025-08-23
    
    # Exit immediately if a command exits with a non-zero status
    # Treat unset variables as an error and exit immediately
    set -eu
    
    # Define variables
    username=${1:?Plesae enter the username.}
    remote_host="192.168.1.2"
    src="/var/www/html"
    des="${username}@${remote_host}:/var/www/html"
    key_file="${HOME}/.ssh/${username}_key"
    
    # Check the directory
    if [ ! -d "${HOME}/.ssh" ]; then
        mkdir -p "${HOME}/.ssh"
    fi
    
    # Generate the ssh key and copy to remote host 
    if [ -f "${key_file}" ]; then
        echo "${key_file} already exist!"
    else
        ssh-keygen -t ed25519 -C "Created by ${username}." -N "" -f "${key_file}"
    fi
    
    ssh-copy-id -o StrictHostKeyChecking=accept-new \
                -i "${key_file}" "${username}@${remote_host}"

    cat >> ${HOME}/.ssh/config <<- EOF
        Match Host ${remote_host}, User ${username}
            IdentityFile ${key_file}
    EOF
    
    rsync -rltD -zvu --delete "${src}" "${des}"
    ```

---

故障排查 { id="troubleshooting" }
---------------------------------

**1. 网页无法访问**

-   **问题描述：**

    对服务器中的项目目录修改权限后，网页变得无法访问，返回 403 错误码。

-   **原因分析：**

    Nginx 进程会继承启动时的用户组及权限，运行中的进程不会实时感知系统用户组的变更。

-   **解决方案：**

    重启 Nginx 服务。

**1. 网页加载异常**

-   **问题描述：**

    传输文件后，可以访问网页，但网页渲染异常。

-   **原因分析：**

    通过 `rsync` 传输的文件，所属组会更新为用户的默认组，如果用户默认组不是 **developers**，Nginx 就无法正常访问资源文件。

-   **解决方案：**

    修改开发者用户的默认组为 **developers** 后传输文件，或直接递归修改 `/var/www/html` 下文件的所属组为 **developers**。


---

附录：参考与连接 { id="appendix" }
----------------------------------

-   `rsync` 官方文档：[`man 1 rsync`][rsync]
-   `openssh` 相关文档：[`man 1 ssh`][ssh]、[`man 1 ssh-keygen`][ssh-keygen]、[`man 1 ssh-copy-id`][ssh-copy-id]、[`man 5 ssh_config`][ssh-config]

[rsync]: https://manpages.debian.org/bookworm/rsync/rsync.1.en.html "RSYNC(1)"
[ssh]: https://manpages.debian.org/bookworm/openssh-client/ssh.1.en.html "SSH(1)"
[ssh-keygen]: https://manpages.debian.org/bookworm/openssh-client/ssh-keygen.1.en.html "SSH-KEYGEN(1)"
[ssh-copy-id]: https://manpages.debian.org/bookworm/openssh-client/ssh-copy-id.1.en.html "SSH-COPY-ID(1)"
[ssh-config]: https://manpages.debian.org/bookworm/openssh-client/ssh_config.5.en.html "SSH_CONFIG(5)"
