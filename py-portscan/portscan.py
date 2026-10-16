#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-portscan —— 多线程 TCP 端口扫描器（学习 / 授权测试用）

功能：
  1. 扫描常见端口（-c）或自定义端口 / 端口段（-p）
  2. 多线程并发扫描，速度远快于单线程
  3. 可选抓取服务横幅（banner），初步识别运行的服务
  4. 结果按端口号排序输出，开放端口一目了然

用法示例：
  python portscan.py 127.0.0.1 -c                  # 扫描本机常见端口
  python portscan.py 127.0.0.1 -p 1-1024           # 扫描 1-1024 端口段
  python portscan.py 127.0.0.1 -p 80,443,3306 -b   # 指定端口并抓横幅
  python portscan.py scanme.nmap.org -c -t 100     # 100 线程扫授权目标

⚠️ 法律声明：只允许扫描你拥有或获得书面授权的目标。
   未经授权扫描他人系统可能违反《网络安全法》等法律法规。
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ----------------------------------------------------------------------
# 常见端口 → 服务名（常识表，不用背，查着用）
# ----------------------------------------------------------------------
COMMON_PORTS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 67: "DHCP", 68: "DHCP",
    80: "HTTP", 110: "POP3", 123: "NTP", 135: "RPC",
    139: "NetBIOS", 143: "IMAP", 161: "SNMP", 389: "LDAP",
    443: "HTTPS", 445: "SMB", 465: "SMTPS", 513: "rlogin",
    514: "syslog", 587: "SMTP-TLS", 631: "IPP", 993: "IMAPS",
    995: "POP3S", 1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle",
    2049: "NFS", 2181: "ZooKeeper", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8000: "HTTP-Alt",
    8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 9000: "HTTP-Alt",
    9200: "Elasticsearch", 11211: "Memcached", 27017: "MongoDB",
}

DEFAULT_TIMEOUT = 1.0  # 单端口连接超时（秒）


def parse_ports(spec: str) -> list:
    """把 '80,443,8000-8100' 这样的字符串解析成排好序的端口列表。"""
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:  # 端口段，如 1-1024
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if start > end:
                start, end = end, start
            # 端口合法范围 1-65535，做一次裁剪防止打爆自己
            ports.update(range(max(1, start), min(65535, end) + 1))
        else:           # 单个端口
            p = int(part)
            if 1 <= p <= 65535:
                ports.add(p)
    return sorted(ports)


def grab_banner(sock: socket.socket, timeout: float = 2.0) -> str:
    """
    尝试读取服务横幅。
    很多服务在 TCP 连接建立后会主动发送欢迎信息，
    例如 SSH 会发 'SSH-2.0-OpenSSH_9.6'，FTP 会发 '220 ...'。
    """
    try:
        sock.settimeout(timeout)
        data = sock.recv(1024)
        # 转成字符串时容忍非 UTF-8 字节，避免直接崩掉
        return data.decode("utf-8", errors="replace").strip()
    except Exception:
        # 超时/被拒/无响应都属于"没拿到横幅"，不是错误
        return ""


def scan_port(target: str, port: int, timeout: float, want_banner: bool):
    """
    扫描单个端口。
    原理：尝试建立 TCP 连接 —— 连上 = 开放；拒绝/超时 = 关闭或过滤。
    返回 (port, is_open, banner_text)
    """
    try:
        with socket.create_connection((target, port), timeout=timeout) as s:
            banner_text = grab_banner(s) if want_banner else ""
            return port, True, banner_text
    except (socket.timeout, ConnectionRefusedError):
        return port, False, ""
    except OSError:
        # 网络不可达、主机拒绝等其余网络错误
        return port, False, ""


def resolve_target(target: str):
    """域名 -> IP，顺便验证目标是否可解析。"""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="py-portscan：多线程端口扫描器（仅用于授权目标）",
        epilog="示例：python portscan.py 127.0.0.1 -c -b",
    )
    parser.add_argument("target", help="目标 IP 或域名")
    parser.add_argument("-c", "--common", action="store_true",
                        help="扫描常见端口（约 50 个）")
    parser.add_argument("-p", "--ports",
                        help="自定义端口，支持 '80,443' 或 '1-1024'")
    parser.add_argument("-b", "--banner", action="store_true",
                        help="抓取服务横幅（识别服务）")
    parser.add_argument("-t", "--threads", type=int, default=50,
                        help="线程数，默认 50")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help="单端口连接超时（秒），默认 1.0")
    args = parser.parse_args()

    # ---- 决定扫描哪些端口 ----
    if args.common:
        ports = sorted(COMMON_PORTS)
    elif args.ports:
        ports = parse_ports(args.ports)
    else:
        parser.error("请指定 -c（常见端口）或 -p（自定义端口），例如：-c 或 -p 1-1024")

    # ---- 解析目标 ----
    ip = resolve_target(args.target)
    if not ip:
        print("[!] 无法解析目标：%s" % args.target)
        sys.exit(1)

    print("[*] 目标：%s (%s)" % (args.target, ip))
    print("[*] 端口数：%d    线程：%d    超时：%.1fs" %
          (len(ports), args.threads, args.timeout))
    print("[*] 开始时间：%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 52)

    # ---- 多线程扫描 ----
    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        # 把所有端口一次性提交给线程池
        futures = [
            pool.submit(scan_port, ip, p, args.timeout, args.banner)
            for p in ports
        ]
        # 谁先完成谁先收结果
        for fut in as_completed(futures):
            port, is_open, banner_text = fut.result()
            if is_open:
                open_ports.append((port, banner_text))

    print("-" * 52)

    # ---- 输出结果 ----
    if not open_ports:
        print("[=] 没有发现开放端口")
        return

    print("[+] 发现 %d 个开放端口：" % len(open_ports))
    print("")
    print("%-8s%-16s%s" % ("端口", "服务", "横幅"))
    for port, banner_text in sorted(open_ports):
        service = COMMON_PORTS.get(port, "unknown")
        print("%-8d%-16s%s" % (port, service, banner_text[:60]))
    print("")
    print("[*] 结束时间：%s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
