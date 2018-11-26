#!/usr/bin/env python
#Author : Leegin Bernads T.S
'''
This is the script for creating multiple users with sudo privileges and add their ssh keys to the respective home directories. The keys are stored in a s3 bucket.
'''
from subprocess import Popen,PIPE
import subprocess
import boto3
import os

#create the user in the instance.
def add_user():
        f = open('/root/OCC').read()  #Reading the users from the file OCC in which I have stored the name of the users to be created.
        g = f.split('\n')
        for user in g:
                h = open('/etc/passwd').read()
                members = []
                for i in h.split('\n'):
                        members.append(i.split(":")[0])
                if user in members:
                        print("The user already exists!!")
                else:
                        subprocess.call(["useradd", "-m", user, "-s", "/bin/bash"]) #User is created and correct permissions/ownerships is set.
                        subprocess.call(["mkdir", "/home/"+user+"/.ssh"])
                        subprocess.call(["chmod", "750", "/home/"+user+"/.ssh"])
                        subprocess.call(["touch", "/home/"+user+"/.ssh/authorized_keys"])
                        subprocess.call(["chown", "-R", user+":"+user, "/home/"+user+"/.ssh"])
                        with open("/etc/sudoers","a") as file:
                                file.write(user+ "\tALL=(ALL)\tNOPASSWD:ALL\n")  #Sudo privilege is given to the user.

#copy the public keys from the s3 bucket to the .ssh folder of the user.
def copy_key():
        fh = open('/root/OCC').read()
        gh = fh.split('\n')
        for user in gh:
                BUCKET_NAME = "user-keys"
                KEY = user+".pub"
                s3 = boto3.resource('s3')
                s3.Bucket(BUCKET_NAME).download_file(KEY, '/home/'+user+'/.ssh/authorized_keys') #Copy the public keys from the s3 bucket to the home directory for  the users.

#check if the file OCC is there in the root directory.
exists = os.path.isfile('/root/OCC')
if exists:
        add_user()
        copy_key()
else:
        f1 = open('/root/OCC','w')
        print('''The file OCC which has the ssh users is not present in the instance. I have created the file "OCC" under "/root" directory for you. Please add the ssh user names in the file''')
