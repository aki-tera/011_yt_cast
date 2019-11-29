#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import youtube_dl
import cgi


# デバッグ用
import cgitb
cgitb.enable(display=0, logdir="../podcast/")

#ファイルの入出力をutf-8にする
import codecs


#PythonのCGIスクリプトから出力したHTMLの日本語文字化け防止
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


form = cgi.FieldStorage()

#オプション付きURLの場合に備えて、＆以降はカットする
url_long = form.getfirst("url")
url = url_long.split("&", 1)[0]
#sequence_list = []

#ユーザ情報の入手
try:
    with codecs.open("user_name.txt", "r", "utf-8") as f:
        line = f.readlines()
        user_name = line[0].rstrip("\n\r")
        user_pass = line[1].rstrip("\n\r")
except:
    user_name = ""
    user_pass = ""


#タイトルチェック
#quietオプションをONにして表示をなくす（apacheサーバのエラーが無くなる？）
with youtube_dl.YoutubeDL({"username":user_name, "password":user_pass, "quiet":True}) as ydl:
    info_dict = ydl.extract_info(url, download=False)
    video_title = info_dict.get('title', None)

print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
print('<p id="title_name">{}</p>'.format(video_title))
print('<p><p>')
print('<form action="/cgi-bin/yt_download.py" method="POST">')
print('<button type="submit" id="get_youtube" name="submit" value="{}">Download</button>'.format(url))
print('</form>')
print('<div id="result2">\n</div>')
