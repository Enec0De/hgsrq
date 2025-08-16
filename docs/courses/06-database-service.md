---
title: 云数据库服务
status: deprecated
--- 

云数据库服务
============

云数据库是云计算的重要组成部分，它提供了一种在互联网上存储、管理和处理数据的方式。

---

1. 数据库基础介绍
--------------

### 1.1. 企业在数据存储管理中面临的挑战

**数据库的定义：**

> 什么是数据库的定义？数据库系统的架构是怎么样的？

**数据库的发展史：**

-   1950 年代：人工管理
-   1960 年代：文件系统
-   1970 年代：数据库系统
    -   20世纪末：层次型数据库、网状型数据库、关系型数据库、面向对象数据库
    -   21世纪：NoSQL、NewSQL

**数据库管理面临的挑战：**

-   数据类型多样性和异构处理能力
-   高度的可扩展性和可伸缩性
-   数据处理的时效性要求
-   大数据时代

> 数据库管理面临挑战的 5V 特性。

### 1.2. 数据库类型

**数据分类：**

-   结构化数据
-   非结构化数据
-   半结构化数据

> 关系型数据库和非关系型数据库的区别。

### 1.3. 关系型数据库简介

**数据库及数据库实例：**

-   > 什么是数据库
-   > 什么是数据库实例？
-   数据库实例是访问数据库的通道

**多实例和分布式集群：**

-   > 什么是多实例
-   > 什么是分布式集群

**关系型数据库结构：**

-   > 概念
-   > 数据存储和查询的执行过程

**一些关系型数据库的概念：**

-   模式（Schema）
-   表空间（Tablespce）
-   数据库对象
    -   表（Table）
    -   视图（View）
    -   索引（Index）
    -   序列（Sequence）
    -   存储过程（Store Procedure）
    -   函数（Function）
-   事物（Transaction）

**MySQL 内存结构和物理结构：**

> 了解以 MySQL 为例的关系型数据库的内存结构和物理结构，处理引擎以 InnoDB为主。

**MySQL 主从架构：**

> 了解 MySQL 的主从复制工作过程。

### 1.4. 非关系型数据库简介

**关系型数据库的不足：**

-   无法适应多变的数据结构
-   高并发读写的瓶颈
-   可扩展性的限制

**如何解决关系型数据库在大数据时代的问题：**

-   放松数据一致性要求
-   改变固定的表结构
-   去除事物、关联等复杂操作

> NoSQL 应运而生啦。

-   > 什么是 NoSQL ？
-   > NoSQL 的几个关键特性？

**NoSQL 数据库的几个关键特点：**

-   灵活性
-   可扩展性
-   高性能
-   功能强大

**NoSQL 数据库应用场景：**

-   键值数据库
-   文档数据库
-   向量数据库
-   其他数据库：图形数据库、时间序列数据库、搜索引擎数据库、列式数据库

---

2. 云数据库
-----------

### 2.1. 云数据库产品介绍

**云数据库的概念：**

> 什么是云数据库？云数据库的特点？
>
> 腾讯云数据库与自建数据库的对比。

### 2.2. 云数据库架构原理

**基本概念：**

-   实例
-   分片
-   集群
-   节点组
-   主机/从机
-   数据库引擎

**基本架构：**

-   如果只有一个 SET，SQL 引擎只负责透传 SQL，就是一个关系型实例
-   如果存在多个 SET，且 SQL 引擎启动分布式模式，就是一个分布式实例

**SQL 引擎：**

-   SQL 引擎位于接入层置，没有主备之分，要求多节点部署以实现容灾
-   属于 CPU 密集型服务，机器的 CPU 要求最高，其次是内存
-   SQL 引擎是由腾讯自研 proxy 发展过来，因此相关功能、文档英文简称 proxy

**DB 模块：**

-   DB 节点上部署数据库服务，属于 I/O 密集型服务，对机器 I/O 要求高，建议配置 SSD 硬盘
-   Agent 属于旁路模块，主要承担 DB 的状态监控，存活检测以及其他功能性任务的执行
-   一个 SET 内的主节点和从节点基于 MySQL 的 replication 复制协议，实现主备同步
-   目前 DB 内核可以提供兼容 MariaDB 和 MySQL 两个版本

**数据一致性：**

-   数据复制方式
    -   强同步（不可退化）
    -   强同步（可退化）
    -   异步

**高可用方案：**

透明故障转移

**可扩展性：**

弹性扩展性能和容量

**数据备份：**

实例默认均开启备份并备份 7 天，需用户手动设置。如果设置了保存 7 天，那么仅能恢复到 7 天以内。

**读写分离：**

-   代码添加注释 `/*slave*/`
-   添加只读账号
-   只读实例（不参与高可用）

**高安全性：**

-   事前
-   事中
-   事后

### 2.3. 云数据库分布式原理

**水平分表：**

-   水平分表 - 拆分
-   水平分表 - 查询
-   水平分表 - 更新

### 2.4. 云数据库 TDSQL

看文档。

---

3. NoSQL 数据库
---------------

### 3.1. 内存数据库 Redis

**Redis 简介：**

> 什么是 Redis？Redis 的功能特性有哪些？

**Redis 应用场景：**

-   缓存（Cache）
-   会话存储（Session）
-   发布订阅（Pub/Sub）
-   排行榜（Rank/Leaderboard）

**Redis 演进过程：**

单机 Redis - 持久化 - 主从复制 - 哨兵系统 - 读写分离 - 分片集群 - Redis Cluster - 代理层 - 多线程

**Redis 架构原理：**

-   代理层
-   分片集群
-   哨兵系统
-   路由机制

> 了解 Redis 架构原理。

**Redis 读写分离：**

> 了解读写分离的基本原理。

**Redis 数据持久化：**

-   AOF
-   RDB
-   混合持久化

**过期策略和淘汰机制：**

-   过期策略：定期删除、惰性删除
-   淘汰机制：6种

**Redis 数据类型：**

-   strings
-   linked lists
-   sets of strings
-   sorted sets of strings
-   hash tables

**Redis 基础操作：**

-   常用操作命令：

    `info`, `select`, `dbsize`, `keys *`, `type key`, `flushdb`, `flushall`,
    `exists key`, `del key1 key2`, `randomkey`, `rename oldkey newkey`, `renamenx oldkey newkey`,
    `expire key seconds`, `ttl key`

-   String 基本操作：

    `set key value`, `get key`, `mset key1 value1 ... keyN valueN`, `mget key1 ... keyN`,
    `incr key`, `decr key`, `flushall`, `incrby key integer`, `decrby key integer`

-   List 基本操作：

    `lpush key string`, `rpush key sting`, `llen key`, `lrange key start end`, `ltrim key start end`,
    `lset key index value`, `lrem key count value`, `lpop key`, `rpop key` 

-   Set 基本操作：

    `sadd key member`, `smembers key`, `srem key member`, `spop key`, `srandmember key`, 
    `smove srckey dstkey member`, `scard key`, `sismember key member`

### 3.2. 文档数据库 MongoDB

**MongoDB 简介：**

> 什么是 MongoDB？MongoDB 的功能特性有哪些？

**MongoDB 的特点：**

-   易扩展性
-   高性能
-   高伸缩性
-   存储动态性
-   速度与持久型

**MongoDB 的相关概念：**

存储结构：

-   文档
-   集合
-   数据库

**MongoDB 的副本集架构：**

-   数据多副本
-   只有 Primary 是可读可写的
-   读写分离
-   节点直接互有心跳

**MongoDB 常见数据类型：**

-   object id
-   string
-   boolean
-   integer
-   double
-   arrays
-   object
-   null
-   timestamp
-   date

**MongoDB 的常见操作：**

-   数据库基本操作：

    `show database`, `use database`, `db.dropDatabase()`,
    
-   集合基本操作：

    `show collections`, `db.createCollection("集合名称")`, `db.集合名称.drop()`

-   文档基本操作：

    `db.collection.insert({key1:value1,key2:value2})`,
    `db.collection.update({key1:value1,key2:value2})`,
    `db.collection.find()`,
    `db.collection.deleteMany({})`,
    `db.collection.remove({})`,
    `db.collection.deleteOne({key:value})`,
    `db.collection.createIndex(keys,option)`

### 3.3. 腾讯云 NoSQL

看文档。
