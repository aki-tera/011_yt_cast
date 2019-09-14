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
#sequence_list = []


#タイトルチェック
with youtube_dl.YoutubeDL() as ydl:
    info_dict = ydl.extract_info(url, download=False)
    video_title = info_dict.get('title', None)

print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
print('<p id="title_name">{}</p>'.format(video_title))
print('<p><p>')
print('<form action="/cgi-bin/yt_download.py" method="POST">')
print('<button type="submit" id="get_youtube" name="submit" value="{}">Download</button>'.format(url))
print('</form>')
print('<div id="result2">\n</div>')
