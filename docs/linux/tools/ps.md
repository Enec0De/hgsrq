---
title: 对于 ps 工具的一些疑问
---

对于 ps 工具的一些疑问
======================

关于在学习 `ps` 官方手册时，对于 `-a` 与 `-d` 选项，及其组合在表现时的疑问。

---

官方源码
--------

下面给出了 `ps` 工具官方源码对 `-a` 与 `-d` 选项的描述，以及筛选进程的方式：

``` c title="select.c"
const char *select_bits_setup(void){
...
  /* UNIX options */
  case SS_U_a | SS_U_d:           select_bits = 0x3f3f; break; /* 3333 or 3f3f */
  case SS_U_a:                    select_bits = 0x0303; break; /* 0303 or 0f0f */
  case SS_U_d:                    select_bits = 0x3333; break;
...
}
...
/***** selected by simple option? */
static int table_accept(proc_t *buf){
  unsigned proc_index;
  proc_index = (has_our_euid(buf)    <<0)
             | (session_leader(buf)  <<1)
             | (without_a_tty(buf)   <<2)
             | (on_our_tty(buf)      <<3);
  return (select_bits & (1<<proc_index));
}
...
```

---

行为推测
--------
官方文档内对选项行为的描述：

> Except as described below, process selection options are additive. 
> The default selection is discarded, and then the selected processes are added to the set of processes to be displayed. 
> A process will thus be shown if it meets any of the given selection criteria.

这里的 below 指的是 `ps` 官方手册 EXAMPLES 的部分，并不包含 `-a` 和 `-d` 选项。根据该描述，我们有以下推测：

-   单独使用 `-a` 选项筛选出来的 `proc_index` 应该是 `0b?00?`
-   单独使用 `-d` 选项筛选出来的 `proc_index` 应该是 `0b??0?`
-   组合使用 `-ad` 选项筛选过出来的是上面两者集合的并集，也就是 `proc_index` 应为 `0b??0?` 

但实际源码中表现出来的却是，筛选所有 `proc_index` 为 `0b?0??` 或 `0b??0?` 的进程。

---

思考
----

结合注释可以推断，如果 `-d` 选项的掩码是 `0x3333` 固定不变，那么应该：

-   当 `-a` 选项的掩码是 `0x0303` 时，`-ad` 选项的掩码为 `0x3333` 才符合文档描述的行为。
-   当 `-a` 选项的掩码是 `0x0f0f` 时，`-ad` 选项的掩码为 `0x3f3f` 才符合文档描述的行为。

这与它注释的内容对应。进一步，假设：

-   `ps a` 筛选出来的进程数为 \\(B_a\\)，
-   `ps -d` 筛选出来的进程数为 \\(U_d\\)，
-   `ps -a` 筛选出来的进程数为 \\(U_a\\)，
-   `ps -ad` 筛选出来的进程数为 \\(U_{ad}\\) 

根据 `SS_B_a` 的掩码来判断，其数量关系应该满足：

\\[
B_a+U_d-U_a=U_{ad}
\\]

---

搁置
----

因为时间问题，没有办法整体审视 `ps` 工具的所有源码及其逻辑，故将此疑问暂留在此。
