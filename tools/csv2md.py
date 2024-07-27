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
    exts = ['tap','zip','cas']
    for file in [file.replace(PATH,'') for file in files if file.lower()[-3:] in exts]:
        if not file in list(a['파일']):
            update = True
            print(file, length)
            a.loc[length]=['','',file,'','','','','']
            length += 1
    if update:
        a.to_csv(csvfile, encoding='euc-kr')
    os.exit()
title = '삼성전자 SPC-1000 소프트웨어에 대해서 알아보자'
summary = '삼성 SPC-1000용 다양한 소프트웨어의 스크린샷과 함께 설명을 합니다. **제목** 또는 **스크린샷**을 클릭하면 **실행화면이 열리고 테잎로딩이 실행**됩니다. 직접 실행해보세요.'
groups = list(a['분류'].unique())
groups.remove('미분류')
groups.append('미분류')

if '-html' in sys.argv:
    import jinja2 as jj
    template=\
'''
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>{{title}}</title>
  <style>
    html {
      color: #1a1a1a;
      background-color: #fdfdfd;
    }
    body {
      margin: 0 auto;
      /* max-width: 36em; */
      padding-left: 50px;
      padding-right: 50px;
      padding-top: 1px;
      padding-bottom: 50px;
      hyphens: auto;
      overflow-wrap: break-word;
      text-rendering: optimizeLegibility;
      font-kerning: normal;
    }
    @media (max-width: 600px) {
      body {
        font-size: 0.9em;
        padding: 12px;
      }
      h1 {
        font-size: 1.8em;
      }
    }
    @media print {
      html {
        background-color: white;
      }
      body {
        background-color: transparent;
        color: black;
        font-size: 12pt;
      }
      p, h2, h3 {
        orphans: 3;
        widows: 3;
      }
      h2, h3, h4 {
        page-break-after: avoid;
      }
    }
    p {
      margin: 1em 0;
    }
    a {
      color: #1a1a1a;
    }
    a:visited {
      color: #1a1a1a;
    }
    img {
      max-width: 100%;
    }
    h1, h2, h3, h4, h5, h6 {
      margin-top: 1.4em;
    }
    h5, h6 {
      font-size: 1em;
      font-style: italic;
    }
    h6 {
      font-weight: normal;
    }
    ol, ul {
      padding-left: 1.7em;
      margin-top: 1em;
    }
    li > ol, li > ul {
      margin-top: 0;
    }
    blockquote {
      margin: 1em 0 1em 1.7em;
      padding-left: 1em;
      border-left: 2px solid #e6e6e6;
      color: #606060;
    }
    code {
      font-family: Menlo, Monaco, Consolas, 'Lucida Console', monospace;
      font-size: 85%;
      margin: 0;
      hyphens: manual;
    }
    pre {
      margin: 1em 0;
      overflow: auto;
    }
    pre code {
      padding: 0;
      overflow: visible;
      overflow-wrap: normal;
    }
    .sourceCode {
     background-color: transparent;
     overflow: visible;
    }
    shadow
    {
        display:block;
        position:relative;
    }

    .shadow:before
    {
        display:block;
        content:'';
        position:absolute;
        width:100%;
        height:100%;
        -moz-box-shadow:inset 0px 0px 6px 6px rgba(255,255,255,1);
        -webkit-box-shadow:inset 0px 0px 6px 6px rgba(255,255,255,1);
        box-shadow:inset 0px 0px 6px 6px rgba(255,255,255,1);
    }
    hr {
      background-color: #1a1a1a;
      border: none;
      height: 1px;
      margin: 1em 0;
    }
    .even {
      background-color: #eeeeee;
    }
    table {
      margin: 1em 0;
      border-collapse: collapse;
      width: 100%;
      overflow-x: auto;
      display: block;
      font-variant-numeric: lining-nums tabular-nums;
    }
    table caption {
      margin-bottom: 0.75em;
    }
    img {
      transform: scale(0.9);
    }
    tbody {
      margin-top: 0.5em;
      border-top: 1px solid #1a1a1a;
      border-bottom: 1px solid #1a1a1a;
    }
    th {
      border-top: 2px solid #1a1a1a;
      padding: 0.25em 0.5em 0.25em 0.5em;
    }
    td {
      padding: 0.125em 0.5em 0.25em 0.5em;
    }
    header {
      margin-bottom: 4em;
      text-align: center;
    }
    #TOC li {
      list-style: none;
    }
    #TOC ul {
      padding-left: 1.3em;
    }
    #TOC > ul {
      padding-left: 0;
    }
    #TOC a:not(:hover) {
      text-decoration: none;
    }
    code{white-space: pre-wrap;}
    span.smallcaps{font-variant: small-caps;}
    div.columns{display: flex; gap: min(4vw, 1.5em);}
    div.column{flex: auto; overflow-x: auto;}
    div.hanging-indent{margin-left: 1.5em; text-indent: -1.5em;}
    /* The extra [class] is a hack that increases specificity enough to
       override a similar rule in reveal.js */
    ul.task-list[class]{list-style: none;}
    ul.task-list li input[type="checkbox"] {
      font-size: inherit;
      width: 0.8em;
      margin: 0 0.8em 0.2em -1.6em;
      vertical-align: middle;
    }
    .display.math{display: block; text-align: center; margin: 0.5rem auto;}
  </style>
</head>
<body>
<h1 id="삼성전자-spc-1000-소프트웨어에-대해서-알아보자">{{title}}</h1>
<p>{{summary}}</p>
{{group}}
{{table}}
</body>
</html>
'''
    jj2 = jj.Template(template)
    reports = {}
    reports['title'] = title
    reports['summary'] = md.markdown(summary)
    group_html = []
    group_html.append('''<h2 id="목차">목차</h2><ol type="1">''')
    for group in groups:
        group_html.append(f'<li><a href="#{group}">{group} ({len(a[a.분류==group])})</a></li>')
    group_html.append('</ol>')
    table_html = []
    for group in groups:
        b = a[a.분류==group]
        table_html.append(f'<h2 id="{group}">{group}</h2>')
        table_html.append(
'''<table>
<colgroup>
<col style="width: 13%" />
<col style="width: 22%; " />
<col style="width: 53%; vertical-align: bottom;" />
</colgroup>
<thead>
<tr class="header">
<th>제목</th>
<th>스크린샷</th>
<th>설명</th>
</tr>
</thead>
<tbody>''')
        index = 1
        for no in b.index:
            c = b.loc[no]
            filename = c.파일
            if not os.path.exists(f'../docs/taps/{filename}'):
                print(filename)
                continue
            title = c.제목 if type(c.제목) != float else filename
            subcmd = f'&{c.실행}' if type(c.실행) != float else ''
            execurl = f"https://retro-1000.github.io?tape={parse.quote(filename)}{subcmd}"
            fileurl = f'https://retro-1000.github.io/taps/{parse.quote(filename)}'
            comment =  (c.설명.replace('\n',' ').replace('|', ' &#x007c; ') if type(c.설명) != float else '자세한 설명은 아직 정리하지 못했다') + f'<br>**[{filename}](https://retro-1000.github.io/taps/{parse.quote(filename)})**'
            imgfilename = f'{filename}.png'
            imgsize = ''
            if not os.path.exists(f'../docs/images/{imgfilename}'):
                # print(f'no {imgfilename}')
                imgurl = 'https://upload.wikimedia.org/wikipedia/commons/2/24/SPC-1000.JPG'
            else:
                imgurl = f'https://retro-1000.github.io/images/{parse.quote(imgfilename)}'
            table_html.append(f'''<tr class="{'odd' if index%2 else 'even'}">
<td width="100px"><a
href="{execurl}">{index}. {title}</a></td>
<td><a href={execurl}><img src="{imgurl}" style="border: 1px solid gray"></a></td>
<td>{md.markdown(comment)}</td>
</tr>''')
            index += 1
        table_html.append('</tr></table>')
    reports['group'] = '\n'.join(group_html)
    reports['table'] = '\n'.join(table_html)
    import numpy as np 
    pos = sys.argv.index('-html')
    if len(sys.argv) > pos + 1:
        file = sys.argv[pos+1]
        open(file, 'w+').write(jj2.render(reports))
    else:
        print(jj2.render(reports))
else:
    print(f'# {title}')
    print('')
    print(f'{summary}')
    print('')
    print('## 목차')
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
            comment =  (c.설명.replace('\n',' ').replace('|', ' &#x007c; ') if type(c.설명) != float else '자세한 설명은 생략한다') + f'<br>**[{filename}](https://retro-1000.github.io/taps/{parse.quote(filename)})**'
            imgfilename = f'{filename}.png'
            imgsize = ''
            if not os.path.exists(f'../docs/images/{imgfilename}'):
                # print(f'no {imgfilename}')
                fileurl = 'https://upload.wikimedia.org/wikipedia/commons/2/24/SPC-1000.JPG'
            else:
                fileurl = f'https://retro-1000.github.io/images/{parse.quote(imgfilename)}'
            filetag = f'[![{title}]({fileurl}{imgsize})](https://retro-1000.github.io?tape={parse.quote(filename)}{subcmd})'
            # filetag = f'<a href={execurl}><img src="{fileurl}"></a>'
            # print(c.실행)
            # print('###', title, f'({filename})')
            # print()
            # print(f'[![{title}]({fileurl}) {imgsize}](https://retro-1000.github.io?tape={parse.quote(filename)}{subcmd})')
            # print()
            # print('**설명**', comment)
            # print()
            print(f'|[{title}]({execurl})|{filetag}|{comment}|')
        print()
