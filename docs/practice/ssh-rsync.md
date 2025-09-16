---
title: 密钥操作与文件同步 
---

密钥操作与文件同步 { id="ssh-rsync" }
=====================================

> 创建于：2025-08-20 :octicons-chevron-right-16: 最后更新：2025-09-16

---

简介说明 { id="introduction" }
------------------------------

假设你有两台主机，一台为 ^^本地主机^^，另一台为云端的 ^^远程主机^^（服务器）。本节会记录以下实践：

1.  配置 ^^远程主机^^ 开发环境中的用户与组。
1.  通过生成并配置密钥的方式，实现 ^^本地主机^^ 到 ^^远程主机^^ 的 `ssh` 免密登录。
1.  最后利用 `rsync` 工具同步 ^^远程主机^^ 与 ^^本地主机^^ 的静态网页文件内容。

### 前置条件 { id="prerequisites" }

-   系统要求：Debian 12 (bookworm)
-   相关工具：`openssh-client 9.2p1`、`openssh-server 9.2p1`、`rsync 3.2.7`

---

安装与配置 { id="installaiton-and-configuration" }
--------------------------------------------------

下方直接提供了实现所有操作的 shell 脚本：

-   脚本 `user_and_group.sh` 实现了开发人员账户与组、远程项目文件夹及其权限的配置，在 ^^远程主机^^ 执行。
-   脚本 `generate_ssh_key.sh` 实现了密钥生成与免密登录的配置[^1]，在 ^^本地主机^^ 执行。
-   脚本 `rsync_to_remote.sh` 实现了 ^^本地主机^^ 与 ^^远程主机^^ 项目文件夹的文件同步，在 ^^本地主机^^ 执行。

??? warning "关于脚本执行权限的一些说明"

    -   脚本 `user_and_group.sh` 必须使用 `sudo` 以获取 **root** 权限执行。
    -   脚本 `generate_ssh_key.sh` 和 `rsync_to_remote.sh` 则不用 `sudo `权限，但脚本执行命令 `ssh-copy-id` 配置时，会要求输入 ^^远程主机^^ 的密码。 

### 远程主机脚本 { id="remote" }

使用下方脚本时，需要输入一个参数以提供用户名，例如 `./user_and_group.sh akiyama`。

``` sh title="user_and_group.sh" linenums="1" hl_lines="22-25 27-31 37-45"
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

### 本地主机脚本 { id="local" }

下方两个脚本均假设你使用的账户名为 **akiyama**。脚本 `rsync_to_remote.sh` 参考了我开发环境中的同步脚本，使用了 `python` 的虚拟环境。
    
!!! note "注意"

    -   使用下方脚本配置好免密登录后，请关闭远程服务器上 `sshd` 的密码登录权限，以提升安全性。
    -   脚本 `generate_ssh_keysh.sh` 中 33、34 行开头都各有一个 `\t` 制表符，复制下方脚本使用时请注意这一点。

=== ":octicons-file-code-16: `generate_ssh_key.sh`"

    ``` sh linenums="1" hl_lines="22-27 29-30 32-35"
    #!/usr/bin/env sh
    # Script Name: generate_ssh_key.sh
    # Author: Aina
    # Date Created: 2025-08-20 | Date Modified: 2025-09-16
    
    # Exit immediately if a command exits with a non-zero status
    # Treat unset variables as an error and exit immediately
    set -eu
    
    # Define variables
    username="akiyama"
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
    ```

=== ":octicons-file-code-16: `rsync_to_remote.sh`"

    ``` sh linenums="1"
    #!/usr/bin/env sh
    # Script Name: rsync_to_remote.sh
    # Author: Aina
    # Date Created: 2025-09-02 | Date Modified: 2025-09-16
    
    # Exit immediately if a command exits with a non-zero status
    # Treat unset variables as an error and exit immediately
    set -eu
    
    # Difine variables
    work_file="$(pwd)/${1:?Usage: ${0} WORKFILE}"
    username="akiyama"
    remote_host="192.168.1.2"
    src="${work_file}site/"
    des="${username}@${remote_host}:/var/www/html/"
    
    # Check the File
    if [ ! -d "${work_file}" -o ${#} -ne 1 ]; then
        echo "Usage: ${0} WORKFILE"
        exit 1
    fi
    
    # Start the venv
    . mkdocs/bin/activate
    
    # Start the build and clean
    cd "${work_file}"
    rm -rf "${src}"
    echo "Start \`mkdocs build'."
    mkdocs build
    
    # Sync
    rsync -rltD -zvu --delete "${src}" "${des}"
    rm -rf "${src}"
    echo "All done."
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

**2. 网页加载异常**

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

[^1]: 这里为了简化操作，没有给密钥设定密码。实际生产环境中，为了安全，建议设定密码并配合 `ssh-agent` 使用。
