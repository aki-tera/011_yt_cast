import youtube_dl

import cgi
import os

# デバッグ用
import cgitb
cgitb.enable()

#html表示の定型文
print ("Content-Type: text/html")
print()
print ("<html><body>")

# formでの変数有無チェック
form = cgi.FieldStorage()
form_check = 0
if "yt_url" not in form:
  form_check = 1



#urlの入力
url = form["yt_url"].value
#タイトルチェック
with youtube_dl.YoutubeDL() as ydl:
    info_dict = ydl.extract_info(url, download=False)
    video_title = info_dict.get('title', None)



# パラメータエラー時の対応
# python の cgiモジュールは変数取得のためにGET/POSTメソッドによって
# 処理を変更する必要はないのでメチャ楽だ！
if form_check == 1 :
  print ("<h2>ERROR !</h2>")
  print ("Please fill in the name and addr fields.")
else :
    print("<br>")
    print ("<b>ダウンロードタイトル</b>", video_title)

print ("</body></html>")


#出力ファイル名
outtmpl = "%(title)s.%(ext)s"
#出力フォルダ
down_dir = "\\youtube\\movie\\"
udl_opts = {"outtmpl": down_dir+outtmpl}
#実際のダウンロード処理
with youtube_dl.YoutubeDL(udl_opts) as ydl:
    ydl.download([url])

print("<b>ダウンロード完了<b>")
