auto_deploy
===========

##Server Auto Deploy Tool


####Usage:

usage: python deploy.py -c config.ini -e exc.ini -u ./package -p /root/downloads/dw



####Config Server :

config use password
* host,port,user,passwd

config use private key
* tag(default:1),host,port,user,private_key(ssh rsa),encrypt type(rsa,dsa:lowercase)

e.g.
* 127.0.0.1 22 liuzheng bmc
* 127.0.0.1 22 liuzheng /Users/liuzheng/.ssh/id_dsa dsa
* 127.0.0.1 22 liuzheng /Users/liuzheng/.ssh/local_rsa rsa



####Config Exceute Commend:

ls -ls |head -n 10
grep a . |head -n 10

.....

