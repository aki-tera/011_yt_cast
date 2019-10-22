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

#xmlの解析
import xml.etree.ElementTree as ET


#実際のダウンロード処理
#with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#    ydl.download([url])



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

html_body1 = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Podcast Creater</title>
<link rel='stylesheet' href='../CSS/style_cgi.css'>
</head>
<body>
"""

html_body2 = """
<p>
<input type='button' id='return_page' value='Return Top Page' onClick='document.location="../index.html";'>
</body>
</html>
"""


#print(html_body)

def test(str):
    print(str)

def rss_checker(RC_folder_path):
    tree = ET.parse(RC_folder_path)
    root = tree.getroot()
    counter = 0
    for child in root:
        for child1 in child:
            for child2 in child1:
                if child2.tag == "title":
                    counter = counter + 1
    return(str(counter).zfill(3))





def main():
    #PythonのCGIスクリプトから出力したHTMLの日本語文字化け防止
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    #postからurlを取得する
    form = cgi.FieldStorage()
    url = form.getvalue("submit")

    #rssから現在のitem数をカウントする
    #戻り値はカウント数
    #出力ファイル名
    outtmpl = "podcast"+rss_checker("podcast/movie.rss")+".mp4"
    #出力フォルダ
    down_dir = "podcast/"
    ydl_opts = {"outtmpl": down_dir+outtmpl}

    #podcastフォルダ内にファイルが多数あれば、削除する
    #check_file(folder_path, max_fail)



    #対象のurlをダウンロードする
    #ダウンロードするファイル名は、podcast000.mp4とする
    #戻り値はタイトル、時間、サイズ
    #download_yt(folder_path, url)

    #rssに新しいファイルを追加する
    #rss_modify(file_path, url_path, imege_path, file_title, file_time, file_size)

    test(html_body1+outtmpl+html_body2)

    return

#if __name__ == "__main__":
#    main()

main()
