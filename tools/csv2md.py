import pandas as pd
import os, sys 
from urllib import parse
import markdown as md
from io import StringIO

csvfile = 'SPC1000_program_collection.csv'

if not os.path.exists(csvfile):
    os.exit()
a = pd.read_csv(csvfile, encoding='euc-kr', dtype={'실행': str, '설명': str},  index_col=0, encoding_errors='ignore')

if '-update' in sys.argv:
    import glob
    PATH = '../docs/taps/'
    update = False
    files = glob.glob(f'{PATH}*')
    length = len(a)
    for file in [file.replace(PATH,'') for file in files if '.cas' in file.lower() or '.tap' in file.lower()]:
        if not file in list(a['파일']):
            update = True
            print(file, length)
            a.loc[length]=['','',file,'','','','','']
            length += 1
    if update:
        a.to_csv(csvfile, encoding='euc-kr')
else:
    if '-html' in sys.argv:
        orig_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
    print('# 삼성전자 SPC-1000 소프트웨어에 대해서 알아보자')
    print('')
    print('삼성 SPC-1000용 다양한 소프트웨어의 스크린샷과 함께 설명을 합니다. **제목** 또는 **스크린샷**을 클릭하면 **실행화면이 열리고 테잎로딩이 실행**됩니다. 직접 실행해보세요.')
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
        print('|제목|스크린샷|설명|')
        print('|---|---|---|')
        for no in b.index:
            c = b.loc[no]
            filename = c.파일
            if not os.path.exists(f'../docs/taps/{filename}'):
                continue
            title = c.제목 if type(c.제목) != float else '미분류 파일'
            subcmd = f'&{c.실행}' if type(c.실행) != float else ''
            execurl = f"https://retro-1000.github.io?tape={parse.quote(filename)}{subcmd}"
            comment =  (c.설명.replace('\n',' ') if type(c.설명) != float else '자세한 설명은 생략한다') + f'<br>**[{filename}](https://retro-1000.github.io/taps/{parse.quote(filename)})**'
            imgfilename = f'{filename}.png'
            imgsize = ''
            if not os.path.exists(f'../docs/images/{imgfilename}'):
                # print(f'no {imgfilename}')
                fileurl = 'https://retro-1000.github.io/images/no_screenshot.png'
            else:
                fileurl = f'https://retro-1000.github.io/images/{parse.quote(imgfilename)}'
                filetag = f'[![{title}]({fileurl}{imgsize})](https://retro-1000.github.io?tape={parse.quote(filename)}{subcmd})'
            filetag = f'<a href={execurl}><img src="{fileurl}"></a>'
            # print(c.실행)
            # print('###', title, f'({filename})')
            # print()
            # print(f'[![{title}]({fileurl}) {imgsize}](https://retro-1000.github.io?tape={parse.quote(filename)}{subcmd})')
            # print()
            # print('**설명**', comment)
            # print()
            print(f'|[{title}]({execurl})|{filetag}|{comment}|')
        print()

    if 'mystdout' in locals():
        sys.stdout = orig_stdout
        print('''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>삼성전자 SPC-1000 소프트웨어 목록</title>
</head>''')
        print('')
        print('<body>')
        print(md.markdown(mystdout.getvalue()))
        print('</body></html>')