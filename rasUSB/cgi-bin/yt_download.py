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
url = form.getfirst("url")


#出力ファイル名
outtmpl = "%(title)s.%(ext)s"
#出力フォルダ
down_dir = "\\..\\download\\"
udl_opts = {"outtmpl": down_dir+outtmpl}
#実際のダウンロード処理
with youtube_dl.YoutubeDL(udl_opts) as ydl:
    ydl.download([url])

print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
print('<p>ダウンロードてきました<p>')
