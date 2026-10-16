# Docker 靶场一键搭建指南

> 目标：四条命令起四个靶场，全部跑在 Docker 里——**不污染宿主机，用完即毁**。
> 端口规划：**8080 留给 Burp Suite**，靶场从 8081 开始。

## 0. 前置条件

- Docker Desktop 已安装且显示 "Engine running"（装法见《从0开始行动清单.md》阶段 0.4）
- 验证：
  ```powershell
  docker --version
  docker ps
  ```

## 1. 端口规划表

| 靶场 | 镜像 | 访问地址 | 练什么 |
|---|---|---|---|
| DVWA | `vulnerables/web-dvwa` | http://localhost:8081 | OWASP Top10 全家桶，难度分级 |
| Pikachu | `area39/pikachu` | http://localhost:8082 | 中文界面，新手最友好 |
| upload-labs | `c0ny1/upload-labs` | http://localhost:8083 | 文件上传专项（20 关） |
| sqli-labs | `acgpiano/sqli-labs` | http://localhost:8084 | SQL 注入专项（65 关） |

## 2. 一键启动（四条命令，复制即用）

```powershell
# DVWA —— 经典 OWASP 漏洞合集
docker run -d --name dvwa -p 8081:80 --restart unless-stopped vulnerables/web-dvwa

# Pikachu —— 中文教学靶场，新手友好
docker run -d --name pikachu -p 8082:80 --restart unless-stopped area39/pikachu

# upload-labs —— 文件上传专项
docker run -d --name upload-labs -p 8083:80 --restart unless-stopped c0ny1/upload-labs

# sqli-labs —— SQL 注入专项
docker run -d --name sqli-labs -p 8084:80 --restart unless-stopped acgpiano/sqli-labs
```

检查是否都起来了：

```powershell
docker ps
```
四个容器状态都是 `Up` 就对了。

> 嫌四条命令麻烦？也可以用 docker-compose 一把梭（见文末附录）。

## 3. 逐个初始化

### DVWA
1. 浏览器打开 http://localhost:8081
2. 登录：`admin` / `password`
3. 底部点 **Create / Reset Database** 初始化（不初始化的话漏洞页面打不开）
4. 左边菜单 **DVWA Security** 把难度设成 **Low** 开始
5. 想练不同难度可以起多个容器：`-e DVWA_SECURITY_LEVEL=medium` + 换端口和容器名

### Pikachu
- 打开 http://localhost:8082 即用，无需初始化，首页有初始化按钮点一下即可
- 每个漏洞分类清晰，适合第一周刷

### upload-labs
- 打开 http://localhost:8083，共 20 关，从最弱校验到二次渲染
- ⚠️ **上传文件报错的修复**（常见）：
  ```powershell
  docker exec -it upload-labs /bin/bash
  ls                      # 确认网站根目录（一般是 /var/www/html）
  mkdir upload            # 在网站根目录创建 upload 目录
  chmod 777 upload        # 给写权限
  exit
  ```

### sqli-labs
- 打开 http://localhost:8084，首页点 "Setup/reset Database for labs" 建库
- 每关 URL 形如 `?id=1`，按关卡号逐个刷

## 4. 容器管理速查

```powershell
docker ps                  # 看运行中的容器
docker ps -a               # 看所有（含停止的）
docker stop 容器名          # 停
docker start 容器名         # 起
docker rm -f 容器名         # 删（-f 强制，数据一起没）
docker logs 容器名          # 看日志（排错用）
docker exec -it 容器名 bash # 进容器内部
docker stop $(docker ps -q) # 一键全停
```

**重置靶场**（刷乱了想重来）：
```powershell
docker rm -f dvwa
# 再跑一遍第 2 步里对应的 docker run 命令
```

## 5. 排错 FAQ

**Q：`docker run` 拉镜像极慢/超时？**
配国内镜像加速：Docker Desktop → Settings → Docker Engine，在 JSON 里加：
```json
{
  "registry-mirrors": ["https://docker.1ms.run", "https://docker.mirrors.ustc.edu.cn"]
}
```
点 Apply & restart。镜像源时效性多变，失效了就换一个。

**Q：localhost:8081 打不开？**
- `docker ps` 看容器是否 Up；`docker logs dvwa` 看报错
- WSL2 用户：可能要用 WSL 的 IP 而不是 localhost，`ip addr show eth0` 查

**Q：端口被占用？**
`netstat -ano | findstr 8081` 找到占用进程，杀掉；或改宿主端口（`-p 9081:80`）

**Q：DVWA 登录后页面空白/数据库错误？**
没点 Create / Reset Database，或点了没等它跑完

**Q：靶场数据会被保留吗？**
只要不 `docker rm`，容器重启数据还在；`--rm` 或删除容器 = 全部重来

## 6. 安全提醒

- 靶场容器**只监听本地回环/内网**，不要把 `-p 0.0.0.0:8081:80` 暴露到公网
- 所有攻击练习限定在这些容器内——**这就是"授权环境"**，出了这个范围就是违法

---

## 附录：docker-compose 一把梭版

在想放的目录建 `docker-compose.yml`：

```yaml
services:
  dvwa:
    image: vulnerables/web-dvwa
    container_name: dvwa
    ports: ["8081:80"]
    restart: unless-stopped
  pikachu:
    image: area39/pikachu
    container_name: pikachu
    ports: ["8082:80"]
    restart: unless-stopped
  upload-labs:
    image: c0ny1/upload-labs
    container_name: upload-labs
    ports: ["8083:80"]
    restart: unless-stopped
  sqli-labs:
    image: acgpiano/sqli-labs
    container_name: sqli-labs
    ports: ["8084:80"]
    restart: unless-stopped
```

然后：
```powershell
docker compose up -d     # 一把起全部
docker compose ps        # 看状态
docker compose down      # 全停并删容器
```

> 后续想练真实 CVE 复现，再上 [Vulhub](https://github.com/vulhub/vulhub)：`git clone` 后进对应漏洞目录 `docker compose up -d`，那是下个阶段的事。
