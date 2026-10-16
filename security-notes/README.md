# security-notes · 个人安全知识库

> 原则：**学过的东西不写下来 = 没学；做完的实验不 commit = 没做。**
> 这里放所有学习笔记、靶场 Writeup、工具心得。它是你求职时最硬核的证明材料。

## 目录结构

```
security-notes/
├── 01-网络基础/        # TCP/IP、HTTP、DNS、Wireshark 抓包分析
├── 02-Web安全/         # SQL 注入、XSS、文件上传、命令执行等原理笔记
├── 03-工具笔记/        # Burp、Nmap、Sqlmap、Metasploit 等使用与原理
├── 04-靶场Writeup/     # DVWA / Pikachu / upload-labs / sqli-labs 逐关复现
├── 05-漏洞复现/        # CVE / 真实漏洞环境复现报告
├── 06-安全运维/        # WAF/IDS/IPS、日志分析、应急响应、webshell 排查
└── 07-学习资源/        # 好书、好站、课程清单（附一句话点评）
```

## 笔记模板（每篇笔记都按这个结构写）

```markdown
# 标题（如：DVWA SQL Injection Low 级复现）

- 日期：2026-10-20
- 环境：DVWA @ localhost:8081 / Low 级
- 标签：#sql-injection #dvwa #writeup

## 目标 / 问题是什么

## 我做了什么（步骤 + 截图/命令）

## 结果

## 原理：为什么会这样（最重要的一段）

## 防御：正常开发该怎么防

## 待深入的问题
```

> 最后两段（原理 + 防御）是新手和熟手的分水岭。攻击步骤到处都有，**能讲清为什么、怎么防，才是科班人的优势**。

## 使用节奏

1. 每周实验后当天写笔记（趁热，隔周就忘）
2. `git add . && git commit -m "docs: DVWA SQL注入 Low级复现" && git push`
3. 每月底回看：这个月笔记最多的方向，就是你该深挖的方向

## 命名规范

- 文件名：`日期-主题-级别.md`，如 `2026-10-25-DVWA-SQL注入-Low.md`
- 图片放同目录 `images/` 子文件夹，markdown 里用相对路径引用
