#coding=utf-8

"""
Deploy Utility
easy_install paramiko
"""

import getpass
import os
import paramiko
import socket
import sys
import time
import re
from stat import *
from threading import Thread
from optparse import OptionParser
import logging


delimit = re.compile(r"\s+")
remote_path = "/root/downloads"


def getSshClientByPassword(host, port, user, password):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port, user, password)
    except paramiko.SSHException, msg:
        print "\033[0;34;40mSSH Error: %s ", host, msg
        return
    except:
        print "\033[0;34;40mError: %s", host, sys.exc_info()[0]
        return
    return client


def getSshClientByPkey(host, port, user, pkey, encrypt_type="rsa"):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekeyfile = os.path.expanduser(pkey)
    print privatekeyfile
    if encrypt_type.lower() == "rsa":
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    elif encrypt_type.lower() == "dsa":
        mykey = paramiko.DSSKey.from_private_key_file(privatekeyfile)
    else:
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)


    try:
        client.connect(host, port=port, username=user, pkey=mykey)
    except paramiko.SSHException, msg:
        print "\033[0;34;40mSSH Error: %s ", user, msg
        return
    except Exception, e:
        print "\033[0;34;40mError: %s", user, sys.exc_info()[0]
        return
    return client


def onSendOK(arg1, arg2):
    print "\033[0;33;40m|Send %s,Rate %.2f%% :Total %s OK" % (arg1, float(arg1) / arg2 * 100, arg2), "\r",


def sendFile(path, client, host):
    sftpclient = client.open_sftp()
    remotefile = "%s/%s" % (remote_path, os.path.basename(path))
    print "\033[0;32;40m-------------------------------------------------------------------------------------"
    print("\033[0;32;40m|Sending %s to %s:%s" % (path, host, remotefile))
    sftpclient.put(path, remotefile, onSendOK)
    print "\033[0;32;40m-------------------------------------------------------------------------------------"


def sendDirectory(localpath, client, host):
    sftpclient = client.open_sftp()
    for root, dirs, files in os.walk(localpath):
        if len(files) != 0:
            for i in xrange(len(files)):
                localfile = "%s/%s" % (root, files[i])
                remotefile = "%s/%s" % (remote_path, files[i])
                print "\033[0;32;40m-------------------------------------------------------------------------------------"
                print("\033[0;32;40m|Sending %s to %s:%s" % (localfile, host, remotefile))
                sftpclient.put(localfile, remotefile, onSendOK)
                print
                print "\033[0;32;40m-------------------------------------------------------------------------------------"


def execCommand(cmd, client, host):
    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        results = stdout.readlines()
        return results
    except paramiko.SSHException, msg:
        print "SSH Error: %s", host, msg
        return []
    except Exception, e:
        print "Error: %s", host, sys.exc_info()[0]
        return []


def loadConfig(filename):
    ret = []
    try:
        f = open(filename, 'r+')
        entries = f.readlines()
        for i in xrange(len(entries)):
            entry = entries[i].strip()
            if entry == '':
                pass
            elif entry[0] == '#':
                pass
            else:
                fields = re.split(delimit, entry)
                if len(fields) < 3:
                    pass
                else:
                    ret.append(fields)

    except IOError, msg:
        print "\033[0;32;44mIO Error: ", msg
    except:
        print "\033[0;32;44mUnknown Error: ", sys.exc_info()[0]

    return ret


def loadScript(filename):
    ret = []
    try:
        f = open(filename, 'r+')
        entries = f.readlines()
        for i in xrange(len(entries)):
            entry = entries[i].strip()
            if entry == '':
                pass
            elif entry[0] == '#':
                pass
            else:
                ret.append(entry)

    except IOError, msg:
        print "\033[0;32;44mIO Error: ", msg
    except:
        print "\033[0;32;44mUnknown Error: ", sys.exc_info()[0]
    return ret


def deploy(config, localpath, script):
    #IP address

    if len(config) == 4:
        host = config[0]
        port = int(config[1])
        user = config[2]
        passwd = config[3]
        client = getSshClientByPassword(host, port, user, passwd)
    elif len(config) == 5:
        host = config[0]
        port = int(config[1])
        user = config[2]
        pkey = config[3]
        encrypt_type = config[4]

        client = getSshClientByPkey(host, port, user, pkey, encrypt_type)
    else:
        print "[Config Error]", config
        return

    if not client:
        print "[Config Error] Client Not Connected!"
        return

    chan = client.get_transport().open_session()

    print
    print("###########################[On %s]###########################" % host)
    print
    if localpath:
        printWrap(execCommand("mkdir -p %s" % remote_path, chan, host))

        mode = os.stat(localpath)[ST_MODE]
        if S_ISDIR(mode):
            sendDirectory(localpath, client, host)
        else:
            sendFile(localpath, client, host)
            print

    if script:
        for x in xrange(len(script)):
            command = script[x]
            if command[0] != "#":
                #print "\033[0;32;40m[%d]:%s\n" % (x, command)
                print "[%d]:%s\n" % (x, command)
                printWrap(execCommand(command, client, host))


def run(localpath, configfile, extentScript):
    configs = None
    scripts = None

    #load config
    if configfile:
        configs = loadConfig(configfile)
    if extentScript:
        scripts = loadScript(extentScript)

    #run one diff server
    for i in xrange(len(configs)):
        config = configs[i]
        deploy(config, localpath, scripts)

    print
    print


def printWrap(listset):
    #print "\033[0;31;44m-------------------------------------------------------------------------------------"
    print "-" * 60
    #print listset
    if(len(listset) == 0):
        #print "\033[0;31;44m|...																				 |"
        print "." * 6
    else:
        for i in xrange(len(listset)):
            print "|", listset[i].strip()
        #print "\033[0;31;44m-------------------------------------------------------------------------------------"
        print "-" * 60
    

if __name__ == "__main__":
    parser = OptionParser("usage: python deploy.py -c config.ini -e exc.ini -u ./package -p /root/downloads/dw")
    parser.add_option("-c", "--config", dest="config", help="config file", default="")
    parser.add_option("-e", "--execute", dest="execute", help="execute file", default="")
    parser.add_option("-u", "--upload", dest="upload", help="upload dir or file", default="")
    parser.add_option("-p", "--path", dest="path", help="remote upload path default:/root/downloads", default="")

    options, args = parser.parse_args()

    if options.path:
        remote_path = options.path

    if options.config:
        upload_path = ""
        if options.upload:
            upload_path = os.path.abspath(options.upload)

        run(upload_path, options.config, options.execute)


