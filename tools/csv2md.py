import pandas as pd
import os, sys 
from urllib import parse

file = 'SPC1000_program_collection.csv'

if not os.path.exists(file):
    os.exit()
a = pd.read_csv(file, encoding='euc-kr', dtype={'실행': str, '설명': str})
print('# 삼성전자 SPC-1000 소프트웨어에 대해서 알아보자')
print('')
print('이 페이지에서는 삼성 SPC-1000용 다양한 소프트웨어의 스크린샷과 설명을 제공합니다. 스크린샷을 클릭하면 테잎로딩이 실행됩니다.')
print('')
print('## 목차')
groups = list(a['분류'].unique())
if '미분류' in groups:
    groups.remove('미분류')
    groups.append('미분류')
for index, group in enumerate(groups):
    print(f'{(int(index)+1)}. [{group}](#{group})')
for group in groups:
    print('')
    print('##', group)
    print('')
    b = a[a.분류==group]
    for no in b.index:
        c = b.loc[no]
        filename = c.파일
        if not os.path.exists(f'docs/taps/{filename}'):
            continue
        print('###', c.제목 if type(c.제목) != float else '미분류 파일', f'({filename})')
        print()
        imgfilename = f'{filename}.png'
        if not os.path.exists(f'docs/images/{imgfilename}'):
            fileurl = 'https://retro-1000.github.io/images/no_screenshot.png' 
        else:
            fileurl = f'https://retro-1000.github.io/images/{parse.quote(imgfilename)}'
        # print(c.실행)
        if type(c.실행) != float:
            subcmd = f'&{c.실행}'
        else:
            subcmd = ''
        print(f'[![image]({fileurl})](https://retro-1000.github.io?tape={parse.quote(filename)}{subcmd})')
        print()
        print('*설명*', c.설명 if type(c.설명) != float else '자세한 설명은 생략한다')
        print()