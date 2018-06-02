# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 21:27
# @author  : slark
# @File    : paramiko_use1.py
# @Software: PyCharm

import paramiko
import select
import sys


class SshClient(object):
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh_client = None
        self.ssh_shell = None
        self.trans = None
        self.channel = None

    def exec_cmd1(self):
        self.trans = paramiko.Transport((self.hostname, self.port))
        self.trans.start_client()
        self.trans.auth_password(username=self.username, password=self.password)
        self.channel = self.trans.open_session()
        self.channel.get_pty()
        self.channel.invoke_shell()

        while True:
            readlist, writelist, errlist = select.select([self.channel, sys.stdin, ], [], [])
            if sys.stdin in readlist:
                input_cmd = sys.stdin.read(1)
                self.channel.sendall(input_cmd)

            if self.channel in readlist:
                result = self.channel.recv(1024)
                if len(result) == 0:
                    print("\r\n**** EOF **** \r\n")
                    break

                sys.stdout.write(result.decode())
                sys.stdout.flush()


if __name__ == "__main__":
    ssh = SshClient("192.168.99.106", 22, "chen", "112992")
    ssh.exec_cmd1()
