#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cgi

# デバッグ用
import cgitb
cgitb.enable()

#PythonのCGIスクリプトから出力したHTMLの日本語文字化け防止
import sys
import io

#rssのタグチェック
import xml.etree.ElementTree as ET

#youtubeのダウンロード
import youtube_dl

#一番新しいファイルを取得
import glob
import os

#現在時刻を取得、時間の形式はRFC 2822
import time
from email import utils

#ファイルの入出力をutf-8にする
import codecs



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


def rss_checker(RC_rss_path):
    """
    指定のrssファイルで登録されているpodcastの数を調べて次に登録すべき番号を文字列で返す
    もしファイルがない場合は、rssを登録して且つ001の数字を返す
    Parameters
    ----------
    RC_rss_path:string
        rss-file path

    Returns
    ----------
    counter:string
        number filled by 000
    """
    try:
        tree = ET.parse(RC_rss_path)
        root = tree.getroot()
        #XPathでtitle数をカウントする
        counter = len(root.findall("./*/*/title"))+1
    except:
        counter = 1
        #（将来対応）
        #movie.rssファイルが無いので、ファイルを生成する

    return(str(counter).zfill(3))


def yt_download(YT_url, YT_ydl_opts, YT_down_dir):
    #実際のダウンロード処理
    with youtube_dl.YoutubeDL(YT_ydl_opts) as ydl:
        info_dict = ydl.extract_info(YT_url, download=False)
        video_title = info_dict.get("title", None)
        video_description = info_dict.get("description", None)
        ydl.download([YT_url])

    #ファイルの詳細情報を入手する

    #ダウンロードしたファイル名+拡張子を取得
    #getctimeで最新作成時のファイルを得る
    list_of_files = glob.glob(YT_down_dir+"*")
    latest_file = max(list_of_files, key=os.path.getctime)
    file_size = os.path.getsize(latest_file)
    #新しい拡張があれば追加する
    file_type = {"mp4":"video/mp4", "mp3":"audio/mp3"}[latest_file[-3:]]
    #登録する日時は現在のものとする
    file_time = utils.formatdate(time.time())

    return(latest_file, video_title, video_description, file_size, file_type, file_time)


def rss_modify(RM_rss_path, RM_data):
    #rssを開く
    with codecs.open(RM_rss_path, "r", "utf-8") as f:
        line = f.readlines()
    count = 0
    for temp in line:
        count = count +1
        if '<itunes:category text="youtube"/>' in temp:
            line.insert(count+0, '      <item>\n')
            line.insert(count+1, '        <title>'+RM_data[1]+'</title>\n')
            line.insert(count+2, '        <description>'+RM_data[2]+'</description>\n')
            line.insert(count+3, '        <enclosure url="http://192.168.11.9:8080/'+RM_data[0]+'" length="'+str(RM_data[3])+'" type="'+RM_data[4]+'"/>\n')
            line.insert(count+4, '        <guid isPermaLink="true">http://192.168.11.9:8080/'+RM_data[0]+'</guid>\n')
            line.insert(count+5, '        <pubDate>'+RM_data[5]+'</pubDate>\n')
            line.insert(count+6, '      </item>\n')
            break
        else:
            continue
        break

    with codecs.open(RM_rss_path, "w", "utf-8") as f:
        f.writelines(line)



def main():
    #PythonのCGIスクリプトから出力したHTMLの日本語文字化け防止
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    #postからurlを取得する
    form = cgi.FieldStorage()
    #オプション付きURLの場合に備えて、＆以降はカットする
    url_long = form.getvalue("submit")
    url = url_long.split("&", 1)[0]


    #出力ファイルを連番にするため、rssから現在のitem数をカウントする
    outtmpl = "podcast"+rss_checker("podcast/movie.rss")+".%(ext)s"
    #出力フォルダ
    down_dir = "podcast/"
    ydl_opts = {"outtmpl": down_dir+outtmpl}

    #（将来対応）
    #podcastフォルダ内にファイルが多数あれば、削除する
    #check_file(folder_path, max_fail)

    #対象のurlをダウンロードする
    #ダウンロードするファイル名は、podcast000.mp4とする
    #戻り値はファイル名、タイトル、詳細
    results = yt_download(url, ydl_opts, down_dir)


    #rssに新しいファイルを追加する
    rss_modify("podcast/movie.rss", results)

    print(html_body)

    return

#実行のメイン

main()
