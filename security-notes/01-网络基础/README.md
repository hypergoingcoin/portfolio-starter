# 01-网络基础

TCP/IP、HTTP、DNS、Wireshark 抓包分析的笔记放这里。

## 建议学习顺序

1. TCP 三次握手/四次挥手（配合 Wireshark 抓包看）
2. HTTP 请求/响应结构（方法、状态码、首部、Cookie）
3. DNS 解析全过程（递归/迭代）
4. 用 Wireshark 过滤表达式做分析练习：`http.request`、`tcp.port == 80`、`dns`

## 第一篇笔记任务

> 用 Wireshark 抓一次访问 http://neverssl.com（或任意 HTTP 站点）的完整过程，写出：请求行、响应行、每个首部字段的含义。
