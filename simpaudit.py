#!/usr/bin/python3

# Simple tool for basic system audits
# Written by: Cody Skinner
# @TheCodySkinner
#
# Requirements: Python 3.5+
#
# Tested on Ubuntu systems, will need to test for cross-distro compatability
# due to the use of system calls
#

import sys
import os
import subprocess
from datetime import date, datetime, timedelta
import platform

# Require Python 3.5+
if sys.version_info[0] < 3:
    exit("Current Python version: "+str(sys.version_info[0])+"\nMust be using Python 3.5+\nIf Python3 is installed, call script with 'python3 simpaudit.py'\nExiting.")

print("*****************************")
print("*     Simple Audit Tool     *")
print("*****************************")
print("A quick system audit\n")
print("-----------------------------\n")
#print("Cody Skinner -- https://codyskinner.net -- @thecodyskinner\n\n")

# Check for being run as root
if os.geteuid() != 0:
    exit("You need to have root privileges to run this script. Please run with 'sudo'. Exiting.")

# Check for SUID
print("************")
print("*   SUID   *")
print("************")
print("Applications with sticky bit set:")
print("Please wait, this process can take a while\n")
findsuid = subprocess.Popen('find / -perm /4000', shell=True, stdout=subprocess.PIPE, encoding='utf-8')
for suid in findsuid.stdout:
    suid = suid.strip('\n')
    findsuidls = subprocess.Popen("ls -l "+suid, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    suidls = findsuidls.communicate()[0]
    print(suidls.strip('\n'))
print("\n")

# Check user info
# This section is ugly, but it works. Good luck.
print("***********")
print("*  USERS  *")
print("***********")
print("Users with home directories on system:\n")
findusers = subprocess.Popen("cat /etc/passwd | grep /home | awk -F: '{print$1}'", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
for line in findusers.stdout:
    line = line.strip('\n')
    print(line)
    findhomedir = subprocess.Popen("cat /etc/passwd | grep "+line+" | awk -F: '{print$6}'", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    homedir = findhomedir.communicate()[0]
    print("Home dir: "+homedir.strip('\n'))
    getinfo = subprocess.Popen("passwd -S "+line, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    info = getinfo.communicate()[0].strip('\n')
    # print(info)
    lastchange = info.split(' ')[2]
    print("Last Password Change: "+lastchange)
    maxage = info.split(' ')[4]
    print("Max Password Age: "+maxage)
    
    # Test if Debian or RH
    if "Debian" in platform.uname().version or "Ubuntu" in platform.uname().version:
        d0 = date(int(lastchange.split('/')[2]),int(lastchange.split('/')[0]),int(lastchange.split('/')[1])) #Change date
        expiredate = d0 + timedelta(days=int(maxage))
        print("Password expire date: "+expiredate.strftime("%m")+"/"+expiredate.strftime("%d")+"/"+expiredate.strftime("%Y"))
        todaydate = date.today()
        today = date(int(todaydate.strftime("%Y")),int(todaydate.strftime("%m")),int(todaydate.strftime("%d")))
        remain = expiredate - today
        print("Days remaining before password max age: "+str(remain).split(' ')[0])
    if int(maxage) > 364:
        print("*****Consider setting a shorter max age for security*****")
    inactive = info.split(' ')[6]
    if int(inactive) >= 0:
        print("Inactivity time until account close: "+inactive)
    if int(inactive) <0:
        print("No inacvity timer set for account closure")
    print("\n")

# Check services running
print("**************")
print("*  SERVICES  *")
print("**************")
print("Current running services:\n")
findserv = subprocess.Popen("systemctl list-units --type service | grep running", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
services = findserv.communicate()[0]
print(services)

# Processes running as root
print("********************")
print("*  ROOT PROCESSES  *")
print("********************")
print("Processes running as root:\n")
findrootproc = subprocess.Popen("ps -elf | grep root", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
rootproc = findrootproc.communicate()[0]
print(rootproc)

# Ports opein
print("****************")
print("*  OPEN PORTS  *")
print("****************")
print("Listening ports on system:\n")
findports = subprocess.Popen("lsof -i -P -n | grep LISTEN", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
ports = findports.communicate()[0]
print(ports)

