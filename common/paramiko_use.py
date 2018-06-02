# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 23:14
# @author  : slark
# @File    : paramiko_use.py
# @Software: PyCharm

import paramiko
import time


class SshClient(object):

    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = 30
        self.ssh_client = None
        self.ssh_shell = None

    def connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
        self.ssh_client = ssh
        self.ssh_shell = ssh.invoke_shell()

    def close(self):
        if not self.ssh_shell:
            self.ssh_shell.close()
        if not self.ssh_client:
            self.ssh_client.close()

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        print(stdout.read().decode())

    def exec_cmds(self, cmds):
        results = list()
        for cmd in cmds:
            self.ssh_shell.send(cmd)
            time.sleep(2)
            out = self.ssh_shell.recv(1024)
            results.append(out)

        return results


if __name__ == "__main__":
    cmds = ["cd temp/\n", "touch file1 file2\n", "rm  \t\t"]
    ssh = SshClient(hostname="192.168.99.106", port=22, username="chen", password="112992")
    ssh.connect()
    result = ssh.exec_cmds(cmds)
    print("########################")
    print(result[0])
    print("########################")
    print(result[1])
    print("########################")
    print(result[2])

    ssh.close()
