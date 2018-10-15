#!/usr/bin/python
import struct
import time
import sys
from subprocess import call
import shutil
import time
import os

def setled(color,number,value):
    if(color=='red'):
        colors = ["red:System","red:SATA1","","red:SATA2","red:Copy"]
    if(color=='green'):
        colors = ["green:System","green:SATA1","green:USB","green:SATA2","green:Copy"]

    file = open("/sys/class/leds/nsa310:"+colors[number-1]+"/"+"brightness","w") 
    file.write(str(value))
    file.close() 

def offallled():
    setled('red',1,0)
    setled('red',2,0)
    setled('red',4,0)
    setled('red',5,0)
    setled('green',1,0)
    setled('green',2,0)
    setled('green',3,0)
    setled('green',4,0)
    setled('green',5,0)
def ignoredfiles(file):
    print(file)
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        try:
            if os.path.isdir(s):
                if(os.path.isdir(d)==False):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    copytree(s,d,symlinks, ignore)
            else:
                if(os.path.isdir(d)==False):
                    shutil.copy2(s, d)
                    print(d)
        except Exception as e:
            print("type error: " + str(e))

offallled()
setled('green',1,1)

##116 => power
##133 => usb


infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else "0")

#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)

while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
    
    if(code == 116 and value == 1):
        #power pressed
        setled('green',1,0)
        setled('red',1,1)
        call("sudo poweroff", shell=True)
        print("SHUTDOWN!")

    if(code == 133 and value == 1):
        #usb pressed
        setled('green',5,1)
        if(os.path.isdir("/media/usb/public")):
            copytree('/media/usb/public','/home/public')
        if(os.path.isdir("/media/usb/catfood")):
            copytree('/media/usb/catfood','/home/catfood/samba')
        call("sudo chmod 777 -R /home/public", shell=True)
        call("sudo chmod 777 -R /home/catfood/samba", shell=True)
        time.sleep(2)
        setled('green',5,0)
    event = in_file.read(EVENT_SIZE)

in_file.close()
