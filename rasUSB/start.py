#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import HTTPServer, CGIHTTPRequestHandler
import os


#デーモン起動時に必要
#但し、このファイルが対象のディレクトリにある場合は不要
#os.chdir('/media/pi/myUSB/rasUSB/')

#IPアドレスは書かなくても良い
host = ""
port = 8081
httpd = HTTPServer((host, port), CGIHTTPRequestHandler)
print('serving at port', port)
httpd.serve_forever()
