#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cgi

# デバッグ用
import cgitb
cgitb.enable(display=0, logdir="../podcast/")

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

import re



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
    """
    指定のurlを指定のフォルダにダウンロードする
    ファイル名等はオプション指示となる
    Parameters
    ----------
    YT_url:string
        url
    YT_ydl_opts:dictionary
        options for youtube_dl
    YT_down_dir:string
        download path

    Returns
    ----------
    counter:tuple
        download file
        title
        description
        file size
        file type
        time stamp
    """
    #実際のダウンロード処理

    try:
        with youtube_dl.YoutubeDL(YT_ydl_opts) as ydl:
            info_dict = ydl.extract_info(YT_url, download=False)
            video_title = info_dict.get("title", None)
            video_description = info_dict.get("description", None)
            ydl.download([YT_url])
    except:
        #エラーが出た際に継続処理をさせる
        YT_ydl_opts["continue"] = True
        for i in range(100):
            try:
                with youtube_dl.YoutubeDL(YT_ydl_opts) as ydl:
                    ydl.download([YT_url])
                break
            except:
                time.sleep(60)


    #ファイルの詳細情報を入手する
    #aタグや全角スペースの削除、改行追加
    video_description = re.sub("<a.*?>|</a>|\u3000", " ", video_description).replace("<br />", "<br>").replace("<br>", "\n")

    #ダウンロードしたファイル名+拡張子を取得
    #getctimeで最新作成時のファイルを得る
    list_of_files = glob.glob(YT_down_dir+"podcast*")
    latest_file = max(list_of_files, key=os.path.getctime)
    file_size = os.path.getsize(latest_file)
    #新しい拡張があれば追加する
    file_type = {"mp4":"video/mp4", "mp3":"audio/mp3"}[latest_file[-3:]]
    #登録する日時は現在のものとする
    file_time = utils.formatdate(time.time())

    return(latest_file, video_title, video_description, file_size, file_type, file_time)


def rss_modify(RM_rss_path, RM_data):
    """
    新しいファイルをrssに追加する
    Parameters
    ----------
    RM_rss_path:string
        rss path
    RM_data:tuple
        download file
        title
        description
        file size
        file type
        time stamp

    Returns
    ----------
    """
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
            line.insert(count+3, '        <enclosure url="http://192.168.11.9:8080/'+RM_data[0][3:]+'" length="'+str(RM_data[3])+'" type="'+RM_data[4]+'"/>\n')
            line.insert(count+4, '        <guid isPermaLink="true">http://192.168.11.9:8080/'+RM_data[0][3:]+'</guid>\n')
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

    #youtube_dlのオプション設定をする
    ydl_opts = {"quiet":True}

    #ユーザ情報の入手
    with codecs.open("user_name.txt", "r", "utf-8") as f:
        line = f.readlines()
        for temp in line:
            #コメントは除外する
            if temp[:1] != "#":
                #区切り文字を使って要素を分割する
                user_info = temp.split(":")
                if re.split("/+", url)[1] == user_info[0]:
                    ydl_opts["username"] = user_info[1].rstrip("\n\r")
                    ydl_opts["password"] = user_info[2].rstrip("\n\r")


    #出力ファイルを連番にするため、rssから現在のitem数をカウントする
    outtmpl = "podcast"+rss_checker("../podcast/movie.rss")+".%(ext)s"
    #出力フォルダ
    down_dir = "../podcast/"
    #出力ファイル名をオプション変数（辞書）に登録する
    ydl_opts["outtmpl"] = down_dir+outtmpl

    #（将来対応）
    #podcastフォルダ内にファイルが多数あれば、削除する
    #check_file(folder_path, max_fail)

    #対象のurlをダウンロードする
    #ダウンロードするファイル名は、podcast000.mp4とする
    #戻り値はファイル名、タイトル、詳細
    results = yt_download(url, ydl_opts, down_dir)


    #rssに新しいファイルを追加する
    rss_modify("../podcast/movie.rss", results)

    #apache2では以下の2行が必要
    print("Content-Type: text/html")
    print()
    print(html_body)

    return

#実行のメイン

main()
