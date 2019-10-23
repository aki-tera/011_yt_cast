#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cgi

# デバッグ用
import cgitb
cgitb.enable()

#PythonのCGIスクリプトから出力したHTMLの日本語文字化け防止
import sys
import io


#youtubeのダウンロード
import youtube_dl

#一番新しいファイルを取得
import glob
import os




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
        counter = len(root.findall("./*/*/title"))
    except:
        counter = 0
        #movie.rssファイルを生成する

    return(str(counter).zfill(3))


def yt_download(YT_url, YT_ydl_opts, YT_down_dir):
    #実際のダウンロード処理
    with youtube_dl.YoutubeDL(YT_ydl_opts) as ydl:
        info_dict = ydl.extract_info(YT_url, download=False)
        video_title = info_dict.get("title", None)
        video_description = info_dict.get("description", None)
        ydl.download([YT_url])

    #ダウンロードしたファイル名+拡張子を取得
    list_of_files = glob.glob(YT_down_dir+"*")
    #getctimeで最新作成時のファイルを得る
    latest_file = max(list_of_files, key=os.path.getctime)

    #ファイル名とタイトル
    return(latest_file, video_title, video_description)


def rss_modify(RM_rss_path, RM_podcast_data):

    #ファイルサイズ取得
    #現在の時間をタイムとする

    with codecs.open(RM_rss_path, "r", "utf-8") as f:
    line = f.readlines()
    count = 0
    for temp in line:
        count = count +1
        print(type(temp))
        if '<itunes:category text="youtube"/>' in temp:
            print(temp)
            line.insert(count+0, '      <item>\n')
            line.insert(count+1, '        <title>'+RM_podcast_data[1]+'</title>\n')
            line.insert(count+2, '        <description>')
            line.insert(count+3, '        <enclosure url="http://192.168.11.9:8080/'+RM_podcast_data[0]'+'" length="2770460" type="video/mp4"/>')
            line.insert(count+4, '        <guid isPermaLink="true">http://192.168.11.9:8080/'+RM_podcast_data[0]'+'</guid>')
            line.insert(count+4, '        <pubDate>Tue, 10 Sep 2019 02:29:47 -0000</pubDate>')
            line.insert(count+2, '      </item>\n')
            break
        else:
            continue
        break

    with codecs.open(path1, "w", "utf-8") as ff:
        ff.writelines(line)



def main():
    #PythonのCGIスクリプトから出力したHTMLの日本語文字化け防止
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    #postからurlを取得する
    form = cgi.FieldStorage()
    url = form.getvalue("submit")

    #rssから現在のitem数をカウントする
    #戻り値はカウント数
    #出力ファイル名
    outtmpl = "podcast"+rss_checker("podcast/movie.rss")+".%(ext)s"
    #出力フォルダ
    down_dir = "podcast/"
    ydl_opts = {"outtmpl": down_dir+outtmpl}

    #将来対応項目
    #podcastフォルダ内にファイルが多数あれば、削除する
    #check_file(folder_path, max_fail)

    #対象のurlをダウンロードする
    #ダウンロードするファイル名は、podcast000.mp4とする
    #戻り値はファイル名、タイトル、詳細
    results = yt_download(url, ydl_opts, down_dir)


    #rssに新しいファイルを追加する
    rss_modify(results)

    print(html_body1+str(results)+html_body2)

    return

#if __name__ == "__main__":
#    main()

main()
