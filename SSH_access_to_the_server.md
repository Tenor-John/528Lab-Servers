# SSH接入服务器

Tags: 使用必看

# ❗用前须知

只有连接了学校**校园网** OR 实验室的 **WIFI** 才可以连接入实验室的服务器！！

（内网穿透涉及隐私、安全、法律等问题，请勿私自对实验室的服务器做修改）

## 🌐 推荐使用ssh软件(以win设备为主)

**xshell + xftp**

**mobaXterm**

## 🧾 接入语法

ip地址已修改为静态ip：192.168.1.116

```bash
### 基础语法 
ssh mmm@192.168.1.116
```

### 1️⃣ cmd / Terminal

可以通过上述的基本语法直接ssh连接入服务器

✅ 可以很方便的通过win操作linux服务器

❌ 无法与服务器之间互相传递文件

![Untitled](Untitled.png)

### 2️⃣ MobaXterm

| MobaXterm | √ | × | 收费 | 企业 | Windows | 功能强大，便携式的工具箱，内建Xserver，支持VNC/RDP/Xdmcp等远程桌面 | 工具过多有些鸡肋 | https://mobaxterm.mobatek.net |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
- 使用`SSH`协议连接Linux主机点击 `Session` -> `SSH`，进入SSH设置页面，再填入支持SSH协议的主机IP 和 用户名，最后点击页面下方OK按钮，完成配置。
- 输入ssh用户的密码；
- 连接SSH成功后，会自动连接SFTP。
- SFTP连接成功后，访问主机的目录，可以修改后访问其他目录；
- 如果想要下次连接该ssh主机时，不用输入密码，可以设置一个`主密码`，来保存各个连接的密码。
- 做完上面几个步骤之后，就成功连接到ssh主机了，窗口上面会显示该连接的名字，而且这个连接设置会被保存起来。

![Untitled](Untitled%201.png)

![Untitled](Untitled%202.png)

### 3️⃣ Xshell + Xftp

| Xshell | × | √ | 收费 | 企业 | Windows | 专业权威 | 收费高不支持sftp，需要搭配Xshell使用 | https://www.xshellcn.com |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

![Untitled](Untitled%203.png)

### 👁️ VMware Workstation 连接服务器

详细过程可以参考这篇文章，具体ip地址、服务器名称与上述过程相同

https://blog.csdn.net/zml_2015/article/details/49176553

## 🛜Linux设备连接

在两台 Linux 系统之间传输文件有多种方法，以下是几种常用的命令行方式：

### 1. scp (Secure Copy)：

scp 是一种使用 SSH 协议的安全文件传输方法。

### **常用参数**

- `r`: 递归复制整个目录
- `p`: 保留原文件的修改时间、访问时间和权限
- `q`: 不显示传输进度条
- `C`: 允许压缩
- `P`: 指定端口号（大写 P）
- `v`: 详细模式显示输出

### ① 从本地复制到远程：

```bash
# Copy from local to remote
# scp [参数] [原路径] [目标路径]
# scp 本地用户名@IP地址:文件名1 远程用户名@IP地址:文件名2
scp local_file remote_username@remote_ip:remote_folder
scp local_file remote_username@remote_ip:remote_file

# 目录传输
scp -r local_folder remote_username@remote_ip:remote_folder

# 实例
scp /opt/soft/nginx-0.5.38.tar.gz root@192.168.120.204:/opt/soft/scptest
# 实例：目录传输
scp -r /opt/soft/mongodb root@192.168.120.204:/opt/soft/scptest

```

### ② 从远程复制到本地：

```bash
# Copy from remote to local
scp username@remote_host:/path/to/remote/file /path/to/local/directory

# 实例
scp root@192.168.120.204:/opt/soft/nginx-0.5.38.tar.gz /opt/soft/
```

### ③ 文件下载

```
Copy
scp remote_username@remote_ip:/path/to/remote/file /path/to/local/directory

```

### ④ 目录下载

```bash
Copy
scp -r remote_username@remote_ip:/path/to/remote/directory /path/to/local/directory

# 实例
scp -r root@192.168.120.204:/opt/soft/mongodb /opt/soft/
```

### ❗注意事项

- 首次连接到新主机时，可能会收到主机密钥验证提示，需要接受。
- 使用 SCP 时需要有相应的权限。
- 可以通过建立 SSH 密钥对来实现免密码传输。
- 传输大量小文件时，SCP 可能比 rsync 更高效。

### 2. rsync：

rsync 是一个强大的文件同步和传输工具，特别适合大量文件或需要定期同步的情况。

从本地复制到远程：

```bash
# Copy
rsync -avz /path/to/local/directory username@remote_host:/path/to/remote/directory
```

从远程复制到本地：

```bash
# Copy
rsync -avz username@remote_host:/path/to/remote/directory /path/to/local/directory
```

### 3. sftp (SSH File Transfer Protocol)：

sftp 是一种交互式文件传输程序。

连接到远程主机：

```bash
# Copy
sftp username@remote_host
```

然后可以使用 put 和 get 命令来上传和下载文件。
