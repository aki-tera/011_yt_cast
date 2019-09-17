#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fnmatch
import os
from email import utils



rss_1='''<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
  <channel>
    <title>我が家のPodcast</title>
    <itunes:owner/>
    <itunes:image href="http://{}/001.png"/>
    <itunes:category text="youtube"/>'''

rss_2='''
      <item>
        <title>{0}</title>
        <enclosure url="{1}" length="{2}" type="audio/mp4"/>
        <guid isPermaLink="true">{1}</guid>
        <pubDate>{3}</pubDate>
      </item>'''

rss_3='''
  </channel>
</rss>'''






def create_folder(CF_path, CF_image_path):
    file_name = []
    file_size = []
    #時間の形式はRFC 2822
    file_time=[]

    for temp in os.listdir(CF_path):
        if fnmatch.fnmatch(temp, "*.mp4"):
            file_name.append(temp)
            file_size.append(os.path.getsize(CF_path+"/"+file_name[0]))

            file_time.append(utils.formatdate(os.path.getmtime(CF_path+"/"+file_name[0])))

    print(file_name[0], file_size[0], file_time[0])

    CF_rss = rss_1.format( CF_image_path )
    CF_rss = CF_rss + rss_2.format(file_name[0], "/podcast/"+file_name[0], file_size[0], file_time[0])
    CF_rss = CF_rss + rss_3

    print(CF_rss)
    print(CF_path+"/"+"movie.rss")

    f = open(CF_path+"/"+"movie.rss", "w", encoding='utf-8')
    f.write(CF_rss)
    f.close()


def main():
    path="../podcast"
    image_path = "192.168.11.9:8080/art-work"
    create_folder(path, image_path)

    return


if __name__ == "__main__":
    main()
