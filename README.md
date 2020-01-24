# Simple Audit Tool

This tool performs a quick audit of the system.

Has been tested on Debian, Ubuntu, CentOS.

Checks for:
* Applications with sticky bit set
* User information (finds users with home dir on system, checks password expiration information, etc.)
* Services running
* Processes running as root
* Listening ports

### Requirements:
* Python3
* root or sudo access to system

### To-do
* Implement time functions for RedHat/CentOS
* Split the script into defined functions for readability/maintenance/scaling
