#!/usr/bin/env python
# -*- coding: utf-8 -*-
# run as daemon later, now just eat a file, and hug guests
# by cheungzee.com

import askIp
import logging
import sys
import re
import common
from common import CommonConfParser

class Panda(object):
    def __init__(self, logFormat='', logLocate=''):
        pass
    
    def run(self):
        print 'hi'

#test Func
def eatAfile(fileLoc, urlFilter='^/$|(/wordpress/)|(^\?p=)'):
    data = CommonConfParser.readConfInList(fileLoc, "\s")
    #dataSet = {}
    reFlt = re.compile(urlFilter)
    for each in data:
        ret = ana(each)
        if reFlt.match(ret['uri']):
            locStr = askIp.locationDict2TidyStr(ret['ipLocation']).encode('utf8')
            print locStr, ret['uri']
        else:
            pass
         
        
#test Func
def ana(line):
    """
        assume format is:
        180.153.206.32 - - [10/Mar/2013:16:06:56 +0800] \
        "GET /ajax.aspnetcdn.com/ajax/jquery.validate/1.9/jquery.validate.min.js/?ver=3.5.1 HTTP/1.1" \
        200 377273 \
        "http://www.cheungzee.com//ajax.aspnetcdn.com/ajax/jquery.validate/1.9/jquery.validate.min.js?ver=3.5.1" \
        "Mozilla/4.0"
        just:
        '$remote_addr - $remote_user [$time_local] "$request" ' \
        '$status $body_bytes_sent "$http_referer" ' \
        '"$http_user_agent" "$http_x_forwarded_for"'
    """
    cIp = line[0]
    timeStr = line[3]
    uri = line[6]
    ref = line[9]
    ua = line[10]
    ipLocation = askIp.askIpLocation(cIp)
    return {'cIp':cIp, 'ipLocation':ipLocation, 'timeStr':timeStr, \
            'uri':uri, 'ref':ref, 'ua':ua}
    
    
def logInit():
    "init root logger"
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "%s logName" % (sys.argv[0])
        sys.exit(0)
    #p = Panda(sys.argv[0])
    #p.run()
    eatAfile(sys.argv[1])
    
    