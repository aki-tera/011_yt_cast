#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import youtube_dl
import cgi


# デバッグ用
import cgitb
cgitb.enable()

#PythonのCGIスクリプトから出力したHTMLの日本語文字化け防止
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



form = cgi.FieldStorage()
url = form.getvalue("submit")


#出力ファイル名
outtmpl = "%(title)s.%(ext)s"
#出力フォルダ
down_dir = "\\..\\download\\"
ydl_opts = {"outtmpl": down_dir+outtmpl}

#実際のダウンロード処理
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])



html_body = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Podcast Creater</title>
<link rel='stylesheet' href='../CSS/style_cgi.css'>
</head>
<body>
<h1>Download complete</h1>
<p>
<p>
<input type='button' id='return_page' value='Return Top Page' onClick='document.location="../index.html";'>
</body>
</html>
"""


print(html_body)
