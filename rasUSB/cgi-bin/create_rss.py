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
    <itunes:image href="http://{}"/>
    <itunes:category text="youtube"/>'''

rss_2='''
      <item>
        <title>{0}</title>
        <enclosure url="{1}" length="{2}" type="video/mp4"/>
        <guid isPermaLink="true">{1}</guid>
        <pubDate>{3}</pubDate>
      </item>'''

rss_3='''
  </channel>
</rss>'''






def create_folder(CF_local_path, CF_url_path, CF_image_path):
    file_name = []
    file_size = []
    #時間の形式はRFC 2822
    file_time=[]

    CF_rss = rss_1.format(CF_image_path)
    temp_count = -1

    for temp in os.listdir(CF_local_path):
        if fnmatch.fnmatch(temp, "*.mp4"):
            temp_count = temp_count+1
            file_name.append(temp)
            file_size.append(os.path.getsize(CF_local_path+"/"+file_name[temp_count]))
            file_time.append(utils.formatdate(os.path.getmtime(CF_local_path+"/"+file_name[temp_count])))

            print(file_name[temp_count], file_size[temp_count], file_time[temp_count])

            CF_rss = CF_rss + rss_2.format(file_name[temp_count], CF_url_path+CF_local_path[2:]+file_name[temp_count], file_size[temp_count], file_time[temp_count])


    
    CF_rss = CF_rss + rss_3

    print(CF_rss)
    print(CF_local_path+"/"+"movie.rss")

    f = open(CF_local_path+"/"+"movie.rss", "w", encoding='utf-8')
    f.write(CF_rss)
    f.close()


def main():
    local_path = "../podcast/"
    url_path = "http://192.168.11.9:8080"
    image_path = "192.168.11.9:8080/art-work/001.png"
    create_folder(local_path, url_path, image_path)

    return


if __name__ == "__main__":
    main()
