# 011_yt_cast
Create iPhone podcast RSS feed

***
This program can download from Video(can be downloaded  by youtube_dl) and can create iPhone podcast RSS feed.

function
1. download files from youtube, niconico, etc.
0. login if you have account.
0. resume donwload function(if download stop, wait 60seconds and resume)

***
I ran this program with the following execution environment.

Raspberry Pi 3
1. python 3.6
0. apatch2 for podcast server(ex:port8080)
0. python's simple server(port8081)

***
Future plan
1. ~~login function~~(done at ver1.8)
0. delete files if your computer is Insufficient memory
0. It will be possible to run only on the Apache server. Currently, youtube_dl cannot run Apache server.

***

Python Library
  * youtube_dl
  * cgi
  * cgitb
  * codecs
  * sys
  * io
  * glob
  * xml.etree.ElementTree
  * time
  * email
  * re

***

参考url  

日本語の文字化け  
*https://qiita.com/eleven-junichi2/items/f3fcb6abe7fe21a4d89a*  

SimpleHTTPServer  
*http://teru0rc4.hatenablog.com/entry/2017/06/27/150126*  
*https://qiita.com/goodboy_max/items/833d482827bf0efab45a*  
*https://symfoware.blog.fc2.com/blog-entry-1977.html*  

Jqueryの通信  
*https://ginpen.com/2013/05/07/jquery-ajax-form/*  
*https://qiita.com/katsukii/items/bd64efcf4f070d77c028*  

Ajax  
*https://qiita.com/qiiChan/items/046a2f53cf4d93a6a398*  
*https://kivantium.net/python-ajax*  
[*https://old-pine.net/*](https://old-pine.net/content/ajax%E3%81%A7%E5%8B%95%E7%9A%84%E3%81%AB%E8%BF%BD%E5%8A%A0%E3%81%97%E3%81%9F%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0%E3%81%AB%E4%BA%8B%E5%89%8D%E5%AE%9A%E7%BE%A9%E3%81%97%E3%81%9Fjavascript%E3%82%92%E5%8B%95%E4%BD%9C%E3%81%95%E3%81%9B%E3%82%8B%E6%96%B9%E6%B3%95)  

CSS  
*https://webliker.info/html-css/*  

デザイン  
*https://saruwakakun.com/html-css/reference/buttons*  

cgiでの表示  
*https://qiita.com/shuichi0712/items/84427a7722463a5cb4dd*  

リンクで戻るボタン  
*http://www.shurey.com/js/samples/1_tips3.html*  

podcast用RSSの仕様  
*https://help.apple.com/itc/podcasts_connect/#/itc1723472cb*  

podcast用RSS  
*https://qiita.com/akinko/items/74886ad84fed0ee10044*  
*https://tech.matchy.net/archives/237*  

xml操作  
*https://pg-chain.com/python-xml-elementtree*  

最新のファイル取得  
*https://off.tokyo/blog/how-to-get-the-latest-file-in-a-folder-using-python/*  

javascriptでパラメータ取得  
*http://www.kogures.com/hitoshi/javascript/link-para/index.html*  
[*http://www.kogures.com/hitoshi/*](http://www.kogures.com/hitoshi/javascript/link-para/link-para-receive3.html?e=abc&j=%E6%97%A5%E6%9C%AC%E8%AA%9E)
