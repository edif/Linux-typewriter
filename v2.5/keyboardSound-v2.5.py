#!/usr/bin/env python

import struct
import sys
import os
try:
    import pygame
except ImportError:
    print """Unable to import pygame. Make sure you have pygame installed \n
           try running \n sudo apt install python-pygame """
    sys.exit()

#check for sudo
if os.getuid() != 0:
    exit("You need to run this script as root. 'sudo ./keyboardSound-v2.py'")
#solve latency (frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pygame.mixer.pre_init(44100, -16, 1, 64)
#pygame sound setup
pygame.mixer.init()
soundObj = pygame.mixer.Sound('Air-horn.ogg')
dingSound = pygame.mixer.Sound('ding3.wav')
inception = pygame.mixer.Sound('inception.ogg')
notime = pygame.mixer.Sound('Aint-no-time.ogg')


list = [] #holds 
in_file = None
infile_path = None

def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

#if user supplies char file path use that
if len(sys.argv) > 1:
    infile_path = sys.argv[1]
elif len(sys.argv) == 1:
    #try to guess keyboard char file
    for i in absoluteFilePaths("/dev/input/by-path"):
        if "kbd" in i:
            list.append(i)
    list.sort()  # get list in order of lowest keyboard number
    try:
        infile_path = os.path.realpath(list[0])
    except IndexError:
        exit("cannot find keyboard")

else:
    #default to event0 as last attempt
    infile_path = "/dev/input/event0"

#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

try:
    #open file in binary mode
    in_file = open(infile_path, "rb")
except IOError as err:
    exit(err)

event = in_file.read(EVENT_SIZE)
#to stop all of the sound objects playing use pygame.mixer.stop()
try:
    while event:
        tv_sec, tv_usec, type, code, value = struct.unpack(FORMAT, event)
    
        if type != 0 or code != 0 or value != 0:
            if code == 28 and value == 1:
                dingSound.play()
            if code == 30 and value == 1:
                inception.stop()
                inception.play()
            if code == 31 and value == 1:
                notime.stop()
                notime.play()    
            elif code == 32 and value == 1:
                soundObj.stop()
    		soundObj.play()
    			
        event = in_file.read(EVENT_SIZE)
except KeyboardInterrupt:
    in_file.close()
    pygame.quit()
    print("bye")

