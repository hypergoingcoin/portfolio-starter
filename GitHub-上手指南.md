# GitHub 上手指南：从注册到 Pin（Windows 版）

> 目标读者：git 零基础。跟着做，约 1 小时完成"注册 → 第一次提交 → 推送 → 主页门面"全流程。
> 每一步都有**验证标准**，达不到不要进下一步。

---

## 第 1 步：注册 GitHub（约 10 分钟）

1. 打开 https://github.com/ → Sign up
2. 用户名建议：姓名拼音或`姓名缩写+sec`，**这个 ID 可能跟你很多年**，别起中二名
3. 邮箱用常用邮箱，密码用密码管理器生成（后面 PAT 也要好好保存）
4. 注册后验证邮箱，顺手开 2FA：Settings → Password and authentication

- ✅ 验证标准：能登录，右上角能看到头像

## 第 2 步：安装并配置 Git（约 20 分钟）

1. 下载：https://git-scm.com/download/win → 64-bit Git for Windows Setup
2. 安装一路默认，**唯一要注意的界面**："Adjusting your PATH environment" → 选 **"Git from the command line and also from 3rd-party software"**
3. **关掉所有终端，重新开 PowerShell**（PATH 修改要重开才生效）
4. 配置身份（把引号里换成你自己的）：
   ```powershell
   git --version
   git config --global user.name "你的GitHub用户名"
   git config --global user.email "你的邮箱"
   git config --global init.defaultBranch main
   git config --global core.quotepath false
   ```
5. 查看配置是否生效：
   ```powershell
   git config --global --list
   ```

- ✅ 验证标准：`git --version` 有版本号；`git config --global --list` 里能看到你设的 name 和 email

## 第 3 步：第一个仓库——把 py-portscan 推上去（约 30 分钟）

### 3.1 本地建仓库并提交

```powershell
cd "D:\Github-csdn -py搭建\portfolio-starter"
git init -b main
git add .
git status
git commit -m "init: portfolio starter with py-portscan"
```
- `git add .` = 把当前目录所有改动放进"暂存区"（打包箱）
- `git commit -m "..."` = 把暂存区打成一次"提交"（贴标签封箱），`-m` 后面写清楚这次改了什么
- `git status` = 随时看一眼当前状态，迷路了就敲它

### 3.2 GitHub 上建远程仓库

1. 网页右上角 **+** → **New repository**
2. Name 填 `portfolio-starter`，选 **Public**
3. **不要勾** "Add a README file"（本地已经有了，勾了会冲突）
4. Create repository 后，复制页面上的 HTTPS 地址：
   `https://github.com/你的用户名/portfolio-starter.git`

### 3.3 关联并推送

```powershell
git remote add origin https://github.com/你的用户名/portfolio-starter.git
git push -u origin main
```

### 3.4 第一次推送的认证坑（90% 的人卡在这）

push 会弹窗口要认证：**用户名 = GitHub 用户名，密码位置 = Personal Access Token（PAT）**，不是你的登录密码。

生成 PAT：
1. GitHub → 右上角头像 → **Settings**
2. 左侧最下 **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)** → Note 随便起名（如 `my-laptop`）→ Expiration 选 90 days
4. 勾选权限：**`repo`**（整个勾上即可）
5. Generate → **立刻复制保存**（离开页面后不再显示，忘了就重新生成）
6. 弹出的认证窗口里，密码栏粘贴这个 Token

> Git Credential Manager 会记住它，以后 push 不用再输。Token 过期后重新生成一个即可。

- ✅ 验证标准：刷新 GitHub 仓库页面，能看到 `portscan.py`、`README.md` 等文件

## 第 4 步：GitHub 个人主页 README（约 10 分钟）

1. **+** → New repository，仓库名**和你的用户名完全一致**（如 `zhangsan-sec`），Public，勾 "Add a README file"
2. 点 README 的铅笔图标编辑，把 `github-profile-README.md` 模板内容粘进去
3. **把所有占位符改掉**：姓名、学校、技能、链接、邮箱
4. Commit changes
5. 以后每周更新一次"在学清单 / 本周在刷"区块——**持续更新的主页 > 完美的静态主页**

- ✅ 验证标准：访问 `https://github.com/你的用户名`，看到的是改过的内容，没有"XXX/待填写"

## 第 5 步：Pin 项目到主页（约 2 分钟）

1. 进你的 profile 页（头像 → Your profile）
2. 右侧 **Customize your pins** → 勾选 `portfolio-starter`（和你的用户名仓库）→ 保存
3. Pin 的项目会显示在主页最显眼处——这就是你的"橱窗"

- ✅ 验证标准：陌生人打开你主页，30 秒内能知道：你是谁、什么方向、会什么工具、做过什么

---

## Git 速查表（贴墙上）

| 场景 | 命令 |
|---|---|
| 看当前状态 | `git status` |
| 看提交历史 | `git log --oneline` |
| 提交全部改动 | `git add . && git commit -m "说明"` |
| 推到远程 | `git push` |
| 拉远程更新 | `git pull` |
| 撤销暂存（未 commit） | `git restore --staged 文件名` |
| 撤销上次 commit（未 push，保留改动） | `git reset --soft HEAD~1` |
| 丢弃某文件的全部本地改动 | `git restore 文件名` |
| 新建分支 | `git checkout -b 分支名` |
| 看远程地址 | `git remote -v` |

### 提交信息怎么写（面试官会看 `git log`）

- ✅ 好：`add: portscan banner grabbing`、`fix: timeout too short on slow network`、`docs: add DVWA sql injection notes`
- ❌ 差：`update`、`修改`、`aaa`、`2222`
- 格式：`类型: 一句话说明`，类型用 `add / fix / docs / refactor / feat`

## 常见问题 FAQ

**Q1：`git` 无法识别？**
装完没重开终端；或 PATH 选错。重开终端还不行就卸载重装，选 "Git from the command line and also from 3rd-party software"。

**Q2：push 反复要密码还失败？**
必须用 PAT 不是密码，见第 3.4 步。注意用户名是 GitHub 用户名不是邮箱。

**Q3：push 超时 / 连接失败？**
网络问题：确认能打开 github.com；如果在用代理，给 git 配代理：`git config --global http.proxy http://127.0.0.1:端口`。

**Q4：中文文件名显示成 `\346\226\207...` 数字？**
`git config --global core.quotepath false`。

**Q5：不小心把密码/Token 提交了怎么办？**
1. **第一件事：去改密码/吊销 Token**（已经推上去过就可能已泄露）
2. 从跟踪中移除：`git rm --cached 文件名`，提交一次
3. 已 push 到公开仓库的敏感信息，要用 BFG 或 `git filter-repo` 清历史——所以**提交前过一眼 `git status`**是最好的预防

**Q6：`git init` 和 GitHub 网页建的仓库有什么区别？**
`git init` 在本地建；网页建的是远程"空房间"。`git remote add origin ...` 就是把本地房间和远程房间用电话线连起来，`git push` 是把本地家当搬过去。

**Q7：为什么默认分支叫 main 不是 master？**
GitHub 2020 年后的新标准，我们 `git config --global init.defaultBranch main` 就是保持一致。
