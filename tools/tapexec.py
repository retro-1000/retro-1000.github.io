#!/bin/python

import sys, os
import platform

if len(sys.argv) > 1:
    filename = sys.argv[1].split['\\'][-1]
    if 'tap' in filename.lower():
        if 'Windows' in platform.platform():
            chrome = 'C:/Program\ Files/Google/Chrome/Application/chrome.exe'        
        elif os.path.exists('/bin/chrome.exe'): 
            chrome = '/bin/chrome.exe'
        else:
            sys.exit()
        cmd = f'{chrome} http://localhost:8000?tape={filename}'
        open('cmd_list.txt', 'a+').write(cmd+'\n')
        print(cmd)
        # os.system(cmd)     