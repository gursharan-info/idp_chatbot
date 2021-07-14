import os
import pexpect
from pexpect import pxssh
import sys
import time
# from rich import print, pretty, inspect
# pretty.install()
sys.path.append('/home/bavalpreet/IDP/')
from server_credentials import IP, SUDOPASSWORD, USERNAME, PASSWORD, SUDOPASSWORD

# print(IP, USERNAME, PASSWORD)
ip = IP
username = USERNAME
pw = PASSWORD
spw = SUDOPASSWORD

s = pxssh.pxssh()
if not s.login (ip, username, pw):
    print("SSH session failed on login.")
    print(str(s))
else:
    print("SSH session login successful")
    s.sendline ('sudo docker ps')
    s.sendline (pw)
    s.prompt()         # match the prompt
    # output_of_docker_ps = s.before
    # print(output_of_docker_ps.decode("utf8"))     # print everything before the prompt.
    output_of_docker_ps = s.before.decode("utf8")
    print(output_of_docker_ps)
    s.sendline ("sudo docker ps | grep sahib-bot-idp:latest | awk '{ print $1 }'")
    s.prompt()  
    output_of_docker_ps_grep = s.before.decode("utf8")
    print(output_of_docker_ps_grep)

    # child = pexpect.spawn('sudo docker ps')
    # child.expect('Password:')
    # child.sendline(spw)

    # sudoPassword = spw
    # print('/n')
    # print('-------------------------sudo docker ps-------------------------------')
    # command = 'sudo docker ps'
    # # p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    # print(os.popen('echo %s|sudo -S %s' % (sudoPassword, command)).read())
    # output = os.popen("sudo docker ps | grep sahib-bot-idp:latest | awk '{ print $1 }'").read()
    # print(output)
    # print(os.popen("sudo docker ps").read())
    # print(os.popen("sudo docker ps | grep sahib-bot-idp:latest | awk '{ print $1 }'").read())
    # # os.system('ssh chatbotadmin@20.198.96.248')
    # print(p)
    s.logout()
