auto_deploy
===========

##Server Auto Deploy Tool


####Usage:

usage: python deploy.py -c config.ini -e exc.ini -u ./package -p /root/downloads/dw



####Config Server config.ini:

config use password
* host,port,user,passwd

config use private key
* tag(default:1),host,port,user,private_key(ssh rsa),encrypt type(rsa,dsa:lowercase)

e.g.
* 127.0.0.1 22 liuzheng bmc
* 127.0.0.1 22 liuzheng /Users/liuzheng/.ssh/id_dsa dsa
* 127.0.0.1 22 liuzheng /Users/liuzheng/.ssh/local_rsa rsa



####Config Exceute Commend exc.ini:

* ls -ls |head -n 10
* grep a . |head -n 10

.....


####Why can’t I run programs in the background with &? It makes paramiko hang.

Run the program under nohup and redirect stdin, stdout and stderr to /dev/null (or to your file of choice, if you need the output later):

run("nohup yes >& /dev/null < /dev/null &")
(yes is simply an example of a program that may run for a long time or forever; >&, < and & are Bash syntax for pipe redirection and backgrounding, respectively – see your shell’s man page for details.)



####depend on
easy_install paramiko