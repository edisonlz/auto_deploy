auto_deploy
===========

##Server Auto Deploy Tool

####设计思想：
目前使用fabric维护服务器的同志应该很多，但是，在我周围的的工作环境中，大都是由运维同学升级和维护服务器，
而使用fabric有学习成本，你不能强求人家用python，多数运维同学还是忠于bash的，
于是乎，就有了写shell脚本，并在远程执行的需求，从此江湖就是一片血雨腥风。


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