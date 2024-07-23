import sys, os
import platform
from urllib import parse

if len(sys.argv) > 1:
    filename = sys.argv[1].split('\\')[-1]
    # print(filename)
    if 'tap' in filename.lower() or 'cas' in filename.lower():
        if 'Windows' in platform.platform():
            chrome = '"C:/Program Files/Google/Chrome/Application/chrome.exe"'        
        elif os.path.exists('/bin/chrome.exe'): 
            chrome = '/bin/chrome.exe'
        else:
            sys.exit()
        fileurl = parse.quote(filename)
        cmd = f'{chrome} http://localhost:8000?tape={fileurl}'
        import pyperclip
        pyperclip.copy(filename)        
        print(cmd)
        open('cmd_list.txt', 'a+').write(cmd+'\n')
        os.system(cmd)     