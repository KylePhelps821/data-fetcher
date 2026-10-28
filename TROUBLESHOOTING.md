# 踩坑记录 (Troubleshooting)

在部署与开发过程中，遇到过以下典型问题，在此记录解决方案以供后续参考。

### 1. 邮件发送失败：550, "From" header is missing or invalid
**报错现象：** 使用 Python 的 `smtplib` 发送邮件时，QQ 邮箱服务器拒收，提示发件人格式无效。
**原因分析：** QQ 邮箱对邮件头的格式校验极其严格。直接使用中文作为发件人名称时，必须遵循 RFC 5322 标准进行编码。
**解决方案：** 使用 Python 内置的 `email.utils.formataddr` 来格式化发件人名称和邮箱。

### 2. Docker 部署时：sqlite3.OperationalError: unable to open database file
**报错现象：** 程序在本地正常，但在 Docker 中运行时，SQLite 报错无法打开/创建数据库文件。
**原因分析：** 在 `docker-compose.yml` 中写单文件挂载 `- ./data.db:/app/data.db` 时，如果宿主机上没有该文件，Docker 会自动创建一个同名**空目录**，导致 SQLite 试图往目录里写数据直接崩溃。
**解决方案：** 改为挂载整个项目目录：`- .:/app`。

### 3. 离线服务器的 GitHub TLS 连接失败
**报错现象：** 执行 `git clone` 时报 `gnutls_handshake() failed: The TLS connection was non-properly terminated`。
**原因分析：** Git 的底层网络环境被阻断，无法与 GitHub 建立安全的 TLS 握手。
**解决方案：** 使用本地打包 + `docker cp` 或 `scp` 传输到服务器。