---
title: Debian 软件包管理
---

Debian 软件包管理
=================

这一章假定最新的稳定版本代号为：**bookworm**。

本文档中，APT 系统的数据源总称为**源列表**。能够在以下文件中的任意位置定义：

-   `/etc/apt/sources.list`
-   `/etc/apt/sources.list.d/*.list`
-   `/etc/apt/sources.list.d/*.source`

*[源列表]: The source list.

---

1. Debian 软件包管理的前提
--------------------------

### 1.1. Debian 软件包管理

-   官方推荐的工具：
    
    -   `apt(8)`，`apt-get(8)`作为其备选
    -   `aptitude`

!!! tip "提示"

    每个软件包都带有使用标准用户接口 `debconf(7)` 的配置脚本，帮助软件包初始化安装过程。

-   作为新手，你应该：
    
    -   在**源列表**中不包含 `testing`，`unstable` 以及不混合使用其他非 Debian 的档案库，例如 Ubuntu。
    -   不要建立 `/etc/apt/preferences`，不要修改 `/var/lib/dpkg` 中的文件。
    -   绝不使用：`dpkg -i random_package` 和 `dpkg --force-all -i random_package`。
    -   从源码直接安装的程序请放到：`/usr/local` 或 `/opt`。

-   强烈建议使用带有安全更新的 stable 套件

    -   在新的主版本发布一个月后，可以根据情况将**源列表**中 stable 版相应的套件名修改为新的（如Debian 13 发布后，将 **bookworm** 修改为 **trixie**）。

-   如果你要用 testing 和 unstable 版，有以下基本的预防措施意见：

    -   将 Debian 系统的 stable 版安装到另一个分区，使系统可以进行**双启动**。
    -   制作安装 CD 便于启动**救援模式**。
    -   考虑安装 `apt-listbugs(1)`。

!!! warning "警告"

    如果你无法做到这些预防措施中的任何一个，那你可能还没做好使用 testing 和 unstable 版的准备。

### 1.2. Debian 档案库基础

**源列表**的格式在 `sources.list(5)` 里面有详尽的描述。

### 1.3. 包管理的事件流

-   更新（`apt update`、`aptitude update`、`apt-get update`）
-   升级（`apt upgrade`、`aptitude safe-upgrade`、`apt-get upgrade`）

    -   更激进的方式，请提前备份：

        `apt full-upgrade`、`aptitude full-upgrade`、`apt get dist-upgrade`

-   安装（`apt install`、`aptitude install`、`apt-get install`）
-   移除（`apt remove`、`aptitude remove`、`apt-get remove`）
-   清除（`apt purge`、`aptitude purge`、`apt-get purge`）

### 1.4. 其他相关

-   你应该阅读优质的官方文档：

    -   `/usr/share/doc/package_name/README.Debian`
    -   `/usr/share/doc/package_name/*`

-   如果包出现了问题：

    -   [Debian bug 跟踪系统（BTS）][debianbug]
    -   请使用 `reportbug(1)` 命令

  [debianbug]: https://www.debian.org/Bugs/

---

2. 基础软件包管理操作
---------------------

-   `apt-get(8)` 和 `apt-cache(8)` 是最**基础**的基于 APT 的软件包管理工具。
-   `apt(8)` 命令是一个用于软件包管理的高级命令行界面。

    -   它基本上是 `apt-get(8)`、`apt-cache(8)` 和类似命令的一个封装，被设计为针对终端用户交互的界面，它默认启用了某些适合交互式使用的选项。

-   `aptitude(8)` 命令是最**通用**的基于 APT 的软件包管理工具。

    -   `aptitude(8)` 不太行，尤其是在处理跨版本的系统升级时。
    -   但是话又说回来，`apt-get(8)` 和 `apt-cache(8)` 可以使用 `/etc/apt/preferences` 来管理软件包的多个版本，比较繁琐；而 `aptitude(8)` 不用，且更直观。
    -   参阅 `/usr/share/doc/aptitude/README`、`apt_preferences(5)`。

!!! note "注意"

    建议用户使用新的 `apt(8)` 命令用于**交互式**的使用场景，而在 shell 脚本中使用 `apt-get(8)` 和 `apt-cache(8)` 命令。

-   软件包活动日志

    -   `/var/log/dpkg.log`
    -   `/var/log/apt/term.log`
    -   `/var/log/aptitude`o

!!! tip "提示"

    我觉得**我自己**需要注意的两个命令：`aptitude search '~c'`、`dpkg -l | grep '^rc'`。

---

3. 全面的系统升级
-----------------

你应该做的：

-   查看“发行说明”
-   备份整个系统（尤其是数据和配置信息）
-   用 `script(1)` 记录升级过程
-   用 `aptitude unmarkauto pkg_name` 来防止移除软件包
-   移除 `/etc/apt/preferences` 文件（禁用 `apt-pinning`）
-   运行 `apt-get -s dist-upgrade` 评估升级造成的影响
-   最后运行 `apt-get dist-upgrade`

---

4. 高级软件包管理操作
---------------------

### 4.1. `aptitude` 操作范例

-   用 "u" 命令更新可用的软件包列表，"U" 命令标记所有可升级的软件包以执行升级，"f" 命令清除新软件包列表，"g" 命令执行所有可升级的软件包以执行升级。
-   按下 “l”，并输入 `~i(~R~i|~Rrecommends:~i)` 来限制软件包的显示，按下 “M” 将 “已安装软件包” 的状态改为自动安装。
-   按下 “l”，并输入 `~prequired|~pimportant|~pstandard|~E` 来限制软件包的显示，按下 “m” 将 “已安装软件包” 的状态改为手动安装。
-   按下 “l”，并输入 `~i!~M` 来限制软件包的显示，在 “已安装软件包” 上按下 “[” 来陈列无用的软件包，按下 “-” 将它们移除。
-   按下 “l”，并输入 `~i` 来限制软件包的显示，之后在 “软件集” 上按下 “m” 将那些软件包标记为手动安装。

### 4.2. 对于 `aptitude` 过于高级或缺失所需的功能

-   `dpkg -l pkg_name_pattern` 列出已安装软件包的列表
-   `dpkg -L pkg_name` 根据软件包检索它安装的所有文件
 
    -   `apt-file list pkg_name_pattern`，从**档案库**检索包的文件

-   `dpkg -S file_name_pattern` 根据文件检索它属于的已安装的软件包

    -   `apt-file search file_name_pattern`，从**档案库**检索提供该文件的软件源

-   `dpkg-reconfigure pkg_name` 重置软件包的配置文件

    -   `-plow` 以最详细的方式执行
    -   `configure-debian(8)` 工具以全屏菜单的形式重新配置

-   `dpkg --audit` 软件包的审计系统，用于检测异常的包
-   `dpkg --configure -a` 配置所有**部分安装**的软件包

-   `apt-cache(8)`

    -   `apt-cache policy binary_pkg_name` 从本地缓存显示一个二进制软件包的可用版本、优先级和档案库信息
    -   `apt-cache madison pkg_name` 从本地缓存显示一个软件包的可用版本和档案库信息
    -   `apt-cache showsrc binary_pkg_name` 从本地缓存显示一个二进制软件包的源代码软件包信息

-   `apt-get build-dep pkg_name` 或者 `aptitude build-dep pkg-name`

    -   安装构建软件包所需要的软件包

-   `apt-get source pkg_name` 

    -   从标准档案库下载源代码

-   `dget [*dsc_URL]` 

    -   从其他档案库下载源代码

-   `dpkg-source -x pkg_version-revision.dsc`

    -   从源代码软件包集合（`*.orig.tar.gz` 和 `*.debian.tar.gz` / `*.diff.gz`）中构建代码树

-   `debuild binary`
-   `dpkg -i pkg_name_version-debian.revision_arch.deb`
-   `apt install /path/to/pkg_filename.deb`
-   `debi pkg_name_version-debian.revision_arch.dsc`
-   `dpkg --get-selections '*' >selection.txt`
-   `dpkg --set-selections <selection.txt`
-   `echo pkg_name hold | dpkg --set-selections`

    -   相当于 `aptitude hold pkg_name`

!!! warning "警告"

    对于支持多架构的软件包，应该指定架构名称，如：

    ``` bash
    dpkg -L libglib2.0-0:amd64
    ```

    小心使用 `dpkg -i` 和 `debi`，以及 `dpkg --force-all` 只适用于高手。

-   `aptitude(8)` 以外的其他软件包管理命令使用类似于 shell glob 的通配符。
-   `configure-debian(8)` ->  `dpkg-reconfigure(8)` -> `debconf`。
-   `dget(1)`、`debuild(1)` 和 `debi(1)` 需要 `devscripts` 软件包。
-   使用 `debsums(1)` 通过 `/var/lib/dpkg/info/*.md5sums` 验证已安装的文件。
-   安装软件包 `apt-list bugs` 可以自动检查 Debian BTS 里的严重 bug。
-   安装软件包 `apt-listchanges`，升级时会在 `NEWS.Debian` 中提供重要新闻。
-   一些搜索软件包元数据的工具：

    -   `grep-dctrl(1)`、`grep-status(1)`、`grep-available(1)` 和 `apt-rdepends(8)`。

---

5. Debian 软件包内部管理
------------------------

### 5.1. 软件包的档案与元数据

-   secure ATP 通过用本地安装的 Debian 档案库公钥，来解密 Release.gpg，从而验证**顶层** Release 的完整性。

    -   Packages 和 Sources 文件的完整性则由**顶层** Release 文件内的 MD5sum 值验证。

-   元数据的本地拷贝：

    -   `/var/lib/apt/list/*`
    -   `/var/cache/apt/apt-file/*`

-   软件包状态：

    -   APT 的软件包状态在 `/var/lib/apt/extended_states` 文件中
    -   `aptitude` 的软件包状态在 `/var/lib/aptitude/pkgstates` 文件中

-   软件包的本地副本：`/var/cache/apt/archives/*`
-   Debian 软件包的名称格式，参阅 `dpkg-source(1)`

!!! note "注意"

    可以用 `dpkg(1)` 提供的命令检查软件包版本，例如 `dpkg --compare-versions 7.0 gt 7.~pre1 ; echo $?`。

### 5.2. `dpkg` 命令

-   `dpkg` 创建的重要文件：

    -   `/var/lib/dpkg/info/package_name.conffiles`
    -   `/var/lib/dpkg/info/package_name.list`
    -   `/var/lib/dpkg/info/package_name.md5sums`
    -   `/var/lib/dpkg/info/package_name.preinst`
    -   `/var/lib/dpkg/info/package_name.postinst`
    -   `/var/lib/dpkg/info/package_name.prerm`
    -   `/var/lib/dpkg/info/package_name.postrm`
    -   `/var/lib/dpkg/info/package_name.config`
    -   `/var/lib/dpkg/alternatives/package_name`
    -   `/var/lib/dpkg/available`
    -   `/var/lib/dpkg/diversions`
    -   `/var/lib/dpkg/statoverride`
    -   `/var/lib/dpkg/status`
    -   `/var/lib/dpkg/status-old`
    -   `/var/backups/dpkg.status*`

!!! tip "提示"

    `udpkg` 命令用于打开 `udeb` 软件包，`udpkg` 命令是 `dpkg` 命令的一个精简版本。

### 5.3. 其他工具

-   `update-alternatives(1)` 命令
-   `dpkg-statoverride(1)` 命令
-   `dpkg-divert(1)` 命令

---

6. 从损坏的系统中恢复
---------------------

!!! danger "警告"

    下面的一些方法具有很高的风险。在此先对你进行警告！

### 6.1. 缺少依赖而导致安装失败

-   当你通过 `sudo dpkg -i` 安装一个包，而没有安装其依赖的包，这个包将作为“部分安装”而失败。

    -   你应当安装安装所有依赖的包，然后使用 `dpkg --configure -a` 来配置它们。

### 6.2. 软件包数据缓存错误

-   软件包数据缓存错误，能够造成奇怪的错误，比如 APT 的 `GPG error: ... invalid: BADSIG ...`。

    -   你应该通过 `sudo rm -rf /var/lib/apt/*` 删除所有缓存的数据。
    -   如果使用了 `apt-cacher-ng`，你还应运行 `sudo rm -rf /var/cache/apt-cacher-ng/*`。

### 6.3. 不兼容旧的用户配置

-   如果一个桌面 GUI 程序在重要的上游版本升级后变得不稳定，你应该怀疑这是旧的本地配置文件（由它创建的）所导致的。如果它在新建的用户账号下运行稳定，那么这个假设就得到了证实。（这是一个打包的 bug 并且打包者通常会避免它。）

    -   你应该移除相应的本地配置文件并重新启动 GUI 程序。你可能需要阅读旧的配置文件内容以便之后恢复配置信息。（别将它们删得太快了。）

### 6.4. 具有相同文件的不同软件包

-   在这种情况下，你通过 `aptitude(8)` 或 `apt-get(1)` 安装软件包，`dpkg(1)` 在对软件包解包时，会给调用程序返回错误，并不会覆盖已经存在的文件。

    -   你应该通过 `sudo dpkg -P old-pkg` 删除旧包

### 6.5. 修复损坏的软件包脚本

-   查看 `/var/lib/dpkg/info` 软件包脚本下的 `*.preinst`、`*.postinst`、`*.prerm`、`*.postrm` 文件，并使用下列方法：

    -   在行首添加 `#` 可以禁用出错的行
    -   在出错行的行尾添加 `|| true` 可以强制返回成功

### 6.6. 使用 `dpkg` 命令进行救援

-   如果软件包损坏了，你可以在软件包缓存目录 `/var/cache/apt/archives/` 找到旧的无 bug 版本，用以下命令安装它：

    -   `dpkg -i /path/to/foo_old_version_arch.deb`

-   如果系统无法从硬盘启动，安装光盘以救援模式启动，将无法启动的系统挂载到 `/target` 后，用以下命令安装：

    -   `dpkg --root /target -i /path/to/foo_old_version_arch.deb`

-   如果由于依赖问题，无法用这种方式安装软件包，并且你真的必须真么做：

    -   使用 `dpkg` 的 `--ignore-depends`、`--force-depends` 和其它选项来无视依赖
    -   参见 `dpkg(8)`

### 6.7 恢复软件包选择数据

-   如果 `/var/lib/dpkg/status` 因为某种原因出现错误，Debian 系统会丢失软件包选择数据并受到严重影响。

    -   寻找位于 `/var/lib/dpkg/status-old` 或 `/var/backups/dpkg.status.*` 中旧的 `/var/lib/dpkg/status` 文件。

-   即使失去 `/var/` 中的所有数据，你依旧可以从 `/usr/share/doc/` 目录恢复一些信息来引导你进行新的安装。

---

7. 软件包管理技巧
-----------------

-   `devscripts` 软件包中的 `who-uploads(1)` 可以识别 Debian 源软件包的实际上传者
-   设置 APT 的配置参数，例如限制 APT 的下载带宽到 800Kib/sec（= 100KiB/sec）：

    -   `sudo vim /etc/apt/apt.conf.d/99local`
    -   加入内容：`APT::Acquire::http::Dl-Limit "800";`

-   `apt` 软件包有自己的 cron 脚本 `/etc/cron.daily/apt`

    -   可以安装 `unattended-upgrades` 软件包来增强这个脚本，使它能够自动升级软件包
    -   可以通过 `/etc/apt/apt.conf.d/02backup` 和 `/etc/apt/apt.conf.d/50unattended-upgrades` 中的参数来进行自定义
    -   相关说明位于 `/usr/share/doc/unattended-upgrades/README` 中

-   当你想要从 `bookworm-backports` 档案库中手动的安装一个名叫 "package-name" 的软件及其依赖包的时候，你应该在目标档案库之前加一个 `-t` 参数

    -   `sudo apt-get install -t bookworm-backports package-name`

-   你能够使用安全 APT 来使用 Debian 兼容的外部软件包档案库，将它加入到**源列表**，并把它的档案库密钥放入 `/etc/apt/trusted.gpg.d/` 目录。参见 `sources.list(5)`、`apt-secure(8)` 和 `apt-key(8)`。

-   从混合源档案库中安装软件包是不被 Debian 官方发行版所支持的

    -   你可以临时修改 `/etc/apt/sources.list` 以操作其他源档案库里的软件包版本

-   若**没有** `/etc/apt/preferences` 文件，APT 系统使用版本字符串来选择最新的可用版本作为**候选版本**

    -   如果经常从混合源档案库中安装软件包，你可以通过创建 `/etc/apt/preferences` 文件并且在其中写入关于调整候选版本的软件包选取规则的合适条目，来自动化这些复杂的操作
    -   参阅 `apt_preferences(5)`

        !!! danger "警告"

            这被称为 **apt-pinning** 特性。新手用 **apt-pinning** 技术肯定会造成比较大的问题。你必须避免使用这个技术，除非确实需要它。

-   **紧急降级**（通过控制候选版本从新的档案库降级到旧的档案库）

    -   将 `/etc/apt/sources.list` 文件中的 **unstable** 源改为 **testing**
    -   按如下所示设置 `/etc/apt/preferences` 文件：

        ```
        Package: *
        Pin: release a=testing
        Pin-Priority: 1010
        ```

    -   运行 `apt-get update; apt-get dist-upgrade` 使整个系统的软件包强制降级
    -   在紧急降级后，移除 `/etc/apt/preferences` 这个特殊的文件

        !!! danger "警告"

            新手用 **apt-pinning** 技术肯定会造成比较大的问题。你必须避免使用这个技术，除非确实需要它。

-   如果你从源代码编译了一个程序来代替 Debian 软件包，最好将它做成一个真正的本地 Debian 软件包（`*.deb`）并使用私人档案库。

    -   如果你选择从源代码编译一个程序并将它安装到 `/usr/local`，你可能需要使用 `equivs` 工具作为最后步骤来满足缺失的软件包依赖。

-   下面给出了移植一个软件包到 stable 系统的步骤：

    !!! warning "小心"

        于系统差异，不能够保证这里描述的过程能够工作，而不需要额外的手工处理。

    -   1. 在 `/etc/apt/sources.list` 中加入以下条目：

        ``` bash
        deb-src http://deb.debian.org/debian unstable  main contrib non-free
        ```

    -   2. 安装编译所需的软件包并下载源软件包：

        ``` bash
        apt-get update
        apt-get dist-upgrade
        apt-get install fakeroot devscripts build-essential
        apt-get build-dep foo
        apt-get source foo
        cd foo*
        ```

        !!! tip "提示"

            如果需要向后移植，可以从 **backport** 源的软件包中更新一些工具链软件包，例如 `dpkg` 和 `debhelper`。

            然后执行命令 `dch -i`，更新软件包版本，例如可以在 `debian/changelog` 中添加版本后缀（如 +bp1），表示这是第一个 backport 版本。

    -   3. 像下面那样构建软件包并将它们安装到系统中：

        ``` bash
        debuild
        cd ..
        debi foo*.changes
        ```

-   用于 APT 的代理服务器

    -   细节参见 `apt.conf(5)` 和 `/usr/share/doc/apt/examples/configure-index.gz`

-   更多关于软件包管理的文档

    -   主要文档有：`aptitude(8)`, `dpkg(1)`, `tasksel(8)`, `apt(8)`, `apt-get(8)`, `apt-config(8)`, `apt-secure(8)`, `sources.list(5)`, `apt.conf(5)`, 和 `apt_preferences(5)`

        来自 `apt-doc` 软件包的 `/usr/share/doc/apt-doc/guide.html/index.html` 和 `/usr/share/doc/apt-doc/offline.html/index.html`

        来自 `aptitude-doc-en` 软件包的 `/usr/share/doc/aptitude/html/en/index.html`

    -   Debian 档案库的官方详细文档：

        [Debian Policy Manual Chapter 2 - The Debian Archive][debpolicy]

        [Debian Developer's Reference, Chapter 4 - Resources for Debian Developers 4.6 The Debian archive][debdev]

        [The Debian GNU/Linux FAQ, Chapter 6 - The Debian FTP archives][debfaq]

    -   为 Debian 用户构建一个 Debian 软件包的教程：[Debian 维护者指南][debmake]

  [debpolicy]: https://www.debian.org/doc/debian-policy/ch-archive
  [debdev]: https://www.debian.org/doc/manuals/developers-reference/resources.html#archive
  [debfaq]: https://www.debian.org/doc/manuals/debian-faq/ftparchives
  [debmake]: https://www.debian.org/doc/manuals/debmake-doc/
