---
title: GNU/Linux 教程
---

GNU/Linux 教程
==============

本文档仅仅提供有效的起点，你必须学会自己（从以下原始材料）查找解决方案。

---

0. 原始材料
-----------

这里提供一些寻找解决方案的途径：

-   [Debian 网站][debian]上的通用信息
-   `/usr/share/doc/package_name` 目录下的文档
-   Unix 风格的 manpage: `dpkg -L package_name |grep '/man/man.*/'`
-   GNU 风格的 info page: `dpkg -L package_name |grep '/info/'`
-   [错误报告][bugs]
-   [Debian Wiki][dbwiki] 用于变化和特定的话题
-   国际开放标准组织的的单一 UNIX 规范 [UNIX 系统主页][unix]上
-   自由的百科全书：[维基百科][wiki]
-   [Debian 管理员手册][handbook]
-   来自 [Linux 文档项目(TLDP)][tldr] 的 HOWTO

  [debian]: https://www.debian.org/
  [wiki]: https://www.wikipedia.org/
  [dbwiki]: https://wiki.debian.org/
  [bugs]: https://bugs.debian.org/package_name
  [unix]: https://www.opengroup.org/
  [handbook]: https://www.debian.org/doc/manuals/debian-handbook/
  [tldr]: https://tldp.org/

!!! tip "提示"

    软件包的详细文档，你需要安装软件包名用 "-doc" 作为后缀名的相应文档包来得到。

    ``` bash title="python 的文档包"
    sudo apt install python3-doc
    ```

---

1. 控制台基础
-------------

### 1.1. 开机相关

-   开机时，你遇到的欢迎信息保存在文件 `/etc/motd` 中（Message Of The Day）。

### 1.2. 账户权限相关

-   登陆后你可能会想要创建账户，涉及到的工具有 `adduser(8)` 和 `deluser(8)`。

    -   其底层依靠 `useradd(8)` 和 `userdel(8)`。

-   任意用户下，输入 `su -l` 或 `su` 可以切换到 **root** 账户。

    -   前者不保存当前用户的环境设定，后者则会保存。

-   可以通过以下方式设置特权用户：

    ``` bash
    echo "penguin  ALL=(ALL) ALL" >> /etc/sudoers
    echo "penguin  ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
    ```

    涉及到的工具有 `sudo(8)` 和 `sudoers(5)`。

### 1.3. 软件包相关

-   建议新手安装额外软件包：

    ``` bash
    apt-get update
    ...
    apt-get install mc vim sudo aptitude
    ...
    ```

    但我不太认可它的建议。涉及到的工具有 `apt-get(8)`。

### 1.4. 控制台相关

-   如果你想切换控制台，例如切换到控制台 3，可以这样：`chvt 3`。
-   ++ctrl+d++ 简写为 ^D，退出命令行，等价于输入 `exit`。
-   这时候你输入了许多命令，面对杂乱的屏幕，可以用：`reset` 或 `clear`。

### 1.5. 关机相关

-   几种关机方式：

    -   `shutdown -h now` 适用于多用户模式，安全关机。
    -   `poweroff -i -f` 适用于单用户，断电快速关机。

了解完上面的内容后，你就可以开工了。

---

2. 类 Unix 文件系统
-------------------

### 2.1. 文件系统基础

-   与文件系统相关的工具有 `mount(8)` 和 `umount(8)` ，在安装 `linux-doc` 包后，可以从目录
    `/usr/share/doc/linux-doc-*/Documentation/filesystems/` 中找到每个文件系统支持的挂载选项。

-   关于文件层次的最佳详细实践在文件系统层次标准 `/usr/share/doc/debian-policy/fhs/fhs-*.txt.gz` 和 `hier(7)` 中。
-   不带参数运行 `mount(8)` 以识别文件树和物理实体之间的对应关系。

### 2.2. 文件系统权限

-   显示文件和目录权限相关的工具有：`ls(1)`。
-   设置权限相关的工具有：`chown(1)`，`chgrp(1)`，`chmod(1)`。
-   三个特殊权限位：

    -   Set User ID（SUID）位
    -   Set Group ID（SGID）位
    -   Sticky（粘滞）位

-   详细用法参考文档，这里提供一些基本用法的示例：

    ``` bash
    ls -alh              # 显示隐藏文件、详细信息、人类可读
    chown newowner foo   # 给 foo 文件设置所有者
    chown newgroup foo   # 给 foo 文件设置所属组
    chmod a+x foo        # 给 foo 文件添加权限 x
    chmod 600 foo        # 给 foo 文件设置权限 rw- --- ---
    chmod 1755 tmp       # 给 tmp 文件夹设置权限 rwx r-x r-t
    chmod 1754 tmp       # 给 tmp 文件夹设置权限 rwx r-x r-T
    ```

!!! tip "提示"

    如果你需要在 shell 脚本中访问 `ls -l` 显示的信息，你需要使用相关命令，如 `test(1)`，`stat(1)` 和 `readlink(1)`。shell 内置命令，如 `[` 或 `test`，可能也会用到。

-   将什么权限应用到新建文件受 shell 内置命令 `umask` 的限制。

    -   `(file permissions) = (requested file permissions) & ~(umask value)`
    -   文件权限 = 666 - `umask`
    -   目录权限 = 777 - `umask`
    -   `umask` 一般设置为 0002 或者 0022
    -   参见 `dash(1)`，`bash(1)`，和 `builtins(7)`。

!!! tip "提示"

    通过把 `umask 002` 写入 ~/.bashrc 文件使用 UPG 。

### 2.3. 用户和组

-   使用下面中的一个，将 **penguin** 用户添加到 **bird** 组的方法：

    -   `sudo usermod -aG bird penguin`
    -   `sudo adduser penguin bird`
    -   `sudo vigr` 编辑 `/etc/group` 和 `sudo vigr -s` 编辑 `/etc/gshadow` ，追加 **penguin** 到 **bird** 行。

-   使用下面中的一个，将 **penguin** 用户从 **bird** 组移除的方法：

    -   `sudo usermod -rG bird penguin`
    -   `sudo deluser penguin bird`
    -   `sudo vigr` 编辑 `/etc/group` 和 `sudo vigr -s` 编辑 `/etc/gshadow` ,删除 **bird** 行里面的 **penguin**。

-   使用下面一个应用配置：

    -   冷重启再登陆。
    -   执行 `kill -TERM -1` 并做一些修复行为，比如 `systemctl restart NetworkManager.service` 

!!! note "注意"

    一般用户的 `$PATH` 环境变量下可能没有包含 `/usr/sbin`，而 `usermod`，`adduser`，`vigr` 都在这个目录下。上述命令可以使用绝对路径，或是利用 `su -l`切换到 **root** 用户环境后再执行。

-   设备是另一种文件。因此，如果你从一个用户账户访问某些设备出现问题时，你需要使这个用户成为相关组的成员。

    -   由系统提供的用户和组的完整列表，可以从 `base-passwd` 包提供的 `/usr/share/doc/base-passwd/users-and-groups.html` 中获得。

-   用户和组系统的管理命令，参见 `passwd(5)`，`group(5)`，`shadow(5)`，`newgrp(1)`，`vipw(8)`，`vigr(8)`，以及 `pam_group(8)`。

!!! tip "一些例子"

    你需要属于 **dialout** 组才能重配置调制解调器、拨号到任意地方，等等。但如果 **root** 用户在 `/etc/ppp/peers/` 为受信任点创建了预定义配置文件的话，你只需要属于
    **dip** 组，就可以创建拨号 IP 来连接到那些受信任的点上，需使用的命令行工具包括 `pppd(8)`、`pon(1)` 以及 `poff(1)`。

### 2.4. 时间戳

-   `mtime`（modify time）

    -   文件内容最后一次被修改的时间。
    -   执行 `ls -l` 查看。

-   `ctime`（change time）

    -   文件元数据最后一次被修改的时间。
    -   执行 `ls -lc` 查看。

-   `atime`（access time）

    -   文件最后一次被访问的时间。
    -   执行 `ls -lu` 查看。

!!! info "更多信息"

    自 Linux 2.6.30 后，`atime` 属性更新的默认行为是 `relatime`，而 `strictatime` 才严格遵守 POSIX 标准。原因是该属性除了 `mbox(5)` 文件外很少用到。参阅 `mount(8)` 了解更多。

### 2.5. 一切皆文件

-   硬链接：`ln target link_name`
-   软链接（symlink）：`ln -s target link_name`

!!! tip "提示"

    通过执行 `ls -li` 来查看 inode 号。

-   管道（FIFO）

    -   `mkfifo mypipe`
    -   `echo "hello" > mypipe &`
    -   `cat mypipe`

-   套接字（Socket）：`netstat -an`
-   设备文件

    -   控制台 `/dev/console`，打印机 `/dev/lp0`，串口控制台 `/dev/ttyS0`。

        !!! warning "注意"

            常规访问打印机请用 `lp(1)`。

    -   执行 `ls -l /dev/sda /dev/sr0 /dev/ttyS0 /dev/zero` 查看主、次设备号，与可以读写他们的群组。
    -   现代 Linux 系统中，处在 `/dev` 之下的文件系统会自动被 `udev(7)` 机制填充。

-   procfs

    -   加载于 `/proc`，`ps(1)` 工具从这个目录结构获得信息。
    -   `/proc/sys`，使用专门的 `sysctl(8)` 修改，或使用 `/etc/sysctl.conf`。
    -   `/proc/kcore` 指向系统内存

-   sysfs

    -   加载于 `/sys`

-   tmpfs

    -   系统启动早期阶段，`/run` 目录挂载为 tmpfs
    -   `/var/run -> /run`
    -   `/var/lock -> /run/lock` 
    -   `/dev/shm -> /run/shm`

!!! info "更多信息"

    以上三个文件系统，可以参考 Linux 内核文档 `/usr/share/doc/linux-doc/Documentation/filesystems/*` 下的 `proc.rst.gz`，`sysf.rst.gz`，`tmpfs.rst.gz`。由软件包
    `linux-doc` 提供。

---

3. 一些技巧
-----------

在原文档中，这里的内容是教你如何使用 `mci(1)` 工具。但由于其本身并不难，我转而在这里记录一点，能让我在 Mac 上，将终端用得更舒服的 iTerm2 的技巧与设置。

-   在 iTerm2 设置 `Profiles` - `Keys` 中，将 `Left option (⌥)  key:` 设置为 `Esc+`，效果为：

    -   ++left-option++ 等价于 ++meta++
    -   大多数情况下也等价于 ++alt++

-   在 iTerm2 设置 `Keys` - `Key Bindings` 中，添加 `Keyboard Shortcut:` ++function+enter++ 映射到 `Action: Send Escape Sequence`，内容为 `[2~`，效果为：

    -   ++function+enter++ 等价于 ++insert++

-   Mac 自带的其他常用键位：

    -   ++function+arrow-up++ 等价于 ++page-up++
    -   ++function+arrow-down++ 等价于 ++page-down++
    -   ++function+arrow-left++ 等价于 ++home++
    -   ++function+arrow-right++ 等价于 ++end++
    -   ++function+backspace++ 等价于 ++del++

---

4. 类 Unix 工作环境基础
-----------------------

-   `bash(1)`

    -   绑定的按键有 ++control+u++ / ++h++ / ++d++ / ++c++ / ++z++ / ++s++ / ++q++ 
    -   个人额外常用 ++control+a++ / ++k++ / ++e++

        !!! tip "提示"

            ++control+s++ 的终端功能可能被 `stty(1)` 禁用。

    -   ++arrow-up++ 、++control+r++ 与命令历史有关
    -   ++tab++ 用于补全，如果要输入制表符，则需要 ++control+v+tab++ 
    -   ++control+alt+del++ 重启/关闭系统，参见 `inittab(5)`

-   鼠标

    -   在 CLI 界面如果需要鼠标支持，需要让 `gpm(8)` 作为 daemon 运行。

-   `less(1)`

    -   在脚本开头执行 `eval $(lesspipe)`，`eval $(lessfile)` 让其变得更加强大
    -   参考 `/usr/share/doc/less/LESSOPEN`

-   `vim`

    -   Debian 通过命令 `/usr/bin/editor` 提供了对系统默认编辑器的统一访问，因此其他程序，例如 `reportbug(1)`，可以调用它
    -   `sudo update-alternatives --config editor` 
    -   `:term` 后 ++control+w++
    -   `:help netrw`

-   记录 shell 活动

    -   新版本的 Vim (version>=8.2)能够被用来清晰的记录 shell 活动，使用 **TERMINAL-JOB** 模式。
    -   `:hardcopy > /path/to/logfile`
    -   在 `script(1)` 下运行 shell，按下 ++control+d++ 退出。

-   基本 Unix 命令

    -   `pwd`、`whoami`、`id`、`file`
    -   `type -p commandname`、`which commandname`、`info commandname`
    -   `apropos key-word` `man -k key-word`    
    -   `< input.txt > output.txt commandname`
    -   `tree`、`lsof filename`、`lsof -p pid`
    -   `find`、`locate`
    -   `top`、`ps aux`、`ps axf`、`ps -ef`
    -   `ps aux | grep -e "pattern"`
    -   `gzip`、`gunzip`、`bzip2`、`bunzip2`、`xz`、`unxz`
    -   `tar -xvf`、`tar -xvzf`、`tar -xvjf`、`tar -xvJf`
    -   `tar -cvf`、`tar -cvzf`、`tar -cvjf`、`tar -cvJf`
    -   `zcat README.gz | pager`

---

5. 简单 shell 命令
------------------

### 5.1. 环境变量

环境变量的默认值由 PAM 系统初始化，其中一些会被某些应用程序重新设定。

-   PAM（可插拔身份验证模块）系统的模块，如 `pam_env` 模块，通过设定 `/etc/pam.conf`、`/etc/environment` 和 `/etc/default/locale` 设置环境变量。
-   显示管理器（例如 `gdm3`）通过 `~/.profile` 给 GUI 会话重新设定环境变量。
-   用户特有程序初始化时，可以重新设置 `~/.profile`、`~/.bash_profile` 和 `~/.bashrc` 中设置的环境变量。
-   `$LANG` 变量

    -   建议最好用 `$LANG` 来配置系统环境变量，只有在逼不得已的情况下才用 `$LC_*` 环境变量。
    -   组成：`xx_YY.ZZZZ`，如 `zh_CN.UTF-8`

-   `$PATH` 变量

    -   Shell 的搜索路径
    -   普通用户账户可能不包括 `/sbin` 和 `/usr/sbin` 

-   `$HOME` 变量

    -   Shell 扩展 `~normal_user` 为 `/home/normal_user/`
    -   `sudo -H program` 将 `$HOME` 重置为目标用户的标准主目录（这里是 `/root`)

### 5.2. 通配符

-   `echo ?[a-z][^0-9]*.txt`
-   `finde . -name '*'` 会匹配 . 开头的隐藏文件名，这一点和 shell glob 模式不同。
-   BASH 内置的 `shopt` 选项定义全局行为。

参见 `glob(7)`。

### 5.3. 返回值和重定向

-   尝试执行 `echo $?` 获取返回值。
-   shell 命令常见用法：

    -   `$()`、`<()`
    -   `command &`
    -   `command1 | command2`、
    -   `command1 ; command2`、`command1 && command2`、`command1 || command2`
    -   `command > foo`、`command >> foo`
    -   `command << delimiter`、`command <<- delimiter`

-   文件描述符相关：

    -   `command1 2>&1 | command2`
    -   `command 2> stderr.txt`、`command 2>> stderr.txt`
    -   使用 `exec` 通过任意一个文件描述符打开文件
    
        ``` bash
        echo Hello > foo
        exec 3<foo 4>bar  # 分配文件描述符 3 用于读取 foo，分配文件描述符 4 用于写入 bar
        cat <&3 >&4       # 将文件描述符 3 复制到 stdin，将文件描述符 4 复制到 stdout
        exec 3<&- 4>&-    # 关闭输入、输出文件描述符 3 和 4
        cat bar           # 读出 Hello
        ```

        !!! note "注意"

            注意 `n<`，`n>` 和 `&n`

!!! tip "提示"

    `2>&1` 将 stderr 重定向到 stdout 的 **目标**，`>/dev/null` 将 stdout 重定向丢弃，因此 `command 2>&1 >/dev/null` 的作用是只显示 stderr。

    若只想传递 stderr，需要用到进程替换，执行命令 `command1 2> >(command2)`。

后台进程的管理涉及 shell 的内建命令：`jobs`、`fg`、`bg` 和 `kill`。请阅读 `bash(1)` 中的章节：“SIGNALS”、“JOB CONTROL” 和 `builtins(1)`。

---

6. 类 Unix 的文本处理
---------------------

### 6.1. 常用的文本处理工具

-   未使用正则表达式的文本处理工具：

    -   `cat(1)`、`tac(1)`、`cut(1)`、`heda(1)`、`tail(1)`、`sort(1)`、`uniq(1)`、`tr(1)`、`diff(1)`

-   默认使用基础正则表达式（BRE）：

    -   `ed(1)` - `vi(1)` - `vim(1)`
    -   `sed(1)`、`grep(1)`

-   使用扩展的正则表达式（ERE）：

    -   `awk(1)``egrep(1)`
    -   带有 `re` 模块的 `python(1)`，参见 `/usr/share/doc/python*`
    -   `tcl(3tcl)` 参见 `re_syntax(3)`，经常与 `tk(3tk)` 一起使用
    -   `perl(1)` 参见 `perlre(1)`
    -   `pcregrep` 软件包的 `pcregrep(1)` 可以匹配满足 **Perl 兼容正则表达式（PCRE）**模式的文本

### 6.2. 正则表达式

正则表达式有三种不同的版本，分为 basic（BRE）、extended（ERE）、perl（PCRE）三种，参考文档。

-   替换表达式：

    -   `&` 表示全文，`\n` 表示第 n 个捕获组。

-   全局替换：

    -   `sed -i -e 's/FROM_REGEX/TO_TEXT/g' file`
    -   `vim '+%s/FROM_REGEX/TO_TEXT/gc' '+update' '+q' file`
    -   `vim '+argdo %s/FROM_REGEX/TO_TEXT/gce|update' '+q' file1 file2 file3`
    -   `perl -i -p -e 's/FROM_REGEX/TO_TEXT/g;' file1 file2 file3`

!!! note "注意"

    `sed(1)` 和 `vim(1)` 使用 BRE；`perl(1)` 使用 ERE。

### 6.3. 提取数据

-   使用 `awk(1)` 工具从文件提取数据：

    -   `awk '($1=="text") { print }' < file.txt`

-   Shell 内建命令 `read` 使用 `$IFS`（内部域分隔符）中的字符来将行分隔成多个单词。

### 6.4. 用于管道命令的脚本片段

-   `find /usr -print`
-   `seq 1 100`
-   `... | xargs -n 1 command`
-   `... | grep -v -e regex_pattern`
-   `... | cut -d: -f3 -`
-   `... | col -bx`
-   `... | expand -`
-   `... | sort | uniq`
-   `... | tr 'A-Z' 'a-z'`
-   `... | tr -d '\n'`

使用 `find(1)` 和 `xargs(1)`，单行 shell 脚本能够在多个文件上循环使用，可以执行相当复杂的任务。
