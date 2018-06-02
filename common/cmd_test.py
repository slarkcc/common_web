# -*- coding: utf-8 -*-
# @Time    : 2018/5/13 22:50
# @author  : slark
# @File    : cmd_test.py
# @Software: PyCharm


# 执行指定命令，读取返回结果
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname="192.168.99.106", port=22, username="chen", password="112992")

stdin, stdout, stderr = ssh.exec_command('df')
result = stdout.read().decode()
err = stderr.read()
ssh.close()

print(stdin, result, err)

# 实现sftp功能
import paramiko

transport = paramiko.Transport(("192.168.99.106", 22))
transport.connect(username="chen", password="112992")

sftp = paramiko.SFTPClient.from_transport(transport)

sftp.put("/Users/chenguang/shell_learn/hello.sh", "/home/chen/temp/hello.sh")
sftp.get("/home/chen/script/test.sh", "/Users/chenguang/temp/test.sh")

transport.close()

# 实现迷钥ssh功能
import paramiko
private_key = paramiko.RSAKey.from_private_key_file('id_rsa31')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname="192.168.99.106", port="22", username="chen", pkey=private_key)
stdin, sdtout, stderr = ssh.exec_command('ifconfig')
res_out = stdout.read()
print(res_out.decode())
ssh.close()

# 迷钥实现sftp功能
import paramiko
private_key = paramiko.RSAKey.from_private_key_file('id_rsa31')
# 连接虚拟机centos上的ip及端口
transport = paramiko.Transport(("192.168.79.9", 22))
transport.connect(username="root", pkey=private_key)
# 将实例化的Transport作为参数传入SFTPClient中
sftp = paramiko.SFTPClient.from_transport(transport)
# 将“calculator.py”上传到filelist文件夹中
sftp.put('D:\python库\Python_shell\day05\calculator.py', '/filedir/calculator.py')
# 将centos中的aaa.txt文件下载到桌面
sftp.get('/filedir/oldtext.txt', r'C:\Users\duany_000\Desktop\oldtext.txt')
transport.close()