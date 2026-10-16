# portfolio-starter · 作品集启动包

> 云南师范大学 · 网络空间安全 · 2025 级 · 大二上
> 目标：渗透测试实习（主）+ 安全运维（辅）。这个仓库是你的**求职门面 + 知识库 + 工具库**三合一。

## 目录结构

```
portfolio-starter/
├── README.md                        ← 本文件
├── 从0开始行动清单.md                ← 主文档：从装 git 到进入学习节奏的完整步骤
├── GitHub-上手指南.md                ← 从注册到 Pin 的 5 步图文指南 + git 速查
├── github-profile-README.md         ← GitHub 个人主页模板（改占位符即可）
├── docker-靶场一键搭建.md            ← DVWA/Pikachu/upload-labs/sqli-labs 一键部署
├── .gitignore                       ← 全局忽略规则（密钥/日志/缓存不提交）
├── py-portscan/                     ← 第一个 Python 工具：多线程端口扫描器
│   ├── portscan.py
│   └── README.md
├── security-notes/                  ← 个人知识库骨架（按主题分目录 + 笔记模板）
│   └── README.md
└── articles/                        ← CSDN 文章初稿存放处（发文后把链接也存这里）
```

## 上手顺序（第一次用，严格按这个顺序）

1. **先读根目录的《从0开始行动清单.md》**——它是总指挥，其余文件都是它在不同阶段的展开
2. 装软件、注册账号（清单里的阶段 0）
3. 照《GitHub-上手指南.md》完成第一次 `git init / add / commit / push`
4. 跑 `py-portscan`，读源码，改一改（比如加个端口范围参数）
5. 照《docker-靶场一键搭建.md》起靶场，开始刷
6. 每次实验后：写笔记进 `security-notes/` → `git commit` → 每周更新一次主页 README

## 三条使用原则

1. **先完成，再完美**：第一版丑没关系，push 上去就是胜利，后面每周改一点
2. **一切留痕**：学过的东西不写下来 = 没学；做完的实验不 commit = 没做
3. **只碰授权目标**：工具和技巧只用于自建靶场 / CTF / 书面授权场景

## 维护节奏

- 每周至少 1 次 commit（周末实验后）
- 每周更新一次 `github-profile-README.md` 里的"在学清单"
- 每月末回看一次《从0开始行动清单.md》的里程碑表，校准下个月计划
