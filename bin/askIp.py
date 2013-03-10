#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by cheungzee.com

import urllib2
import logging 
import json
import time


urlIpQuery_taobao = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s'
#dict uni syntax
"""
{
    "ip":"192.168.1.1",
    "country":"Zhongguo",
    "area":"Dongbei",
    "region":"Heilongjiang",
    "city":"Harbin",
    "isp":"Jiaoyuwang",
    "other":{...}
}
"""

def anaTaobao(url):
    retDict = {}
    count = 0
    while count < 3:
        count += 1
        ret = readHttp(url)    
        if ret == '': 
            time.sleep(1)
            continue
        try:
            ret = json.loads(ret) 
        except Exception, e:
            logging.error("[error in jsonLoads data][%s][%s]" % (ret, e))
            return retDict

        if ret['code'] != 0: # failed
            time.sleep(1)        
            continue
        retDict = ret
        break
    ip = retDict['data']['ip']
    country = retDict['data']['country']
    area = retDict['data']['area']
    region = retDict['data']['region']
    city = retDict['data']['city']
    isp = retDict['data']['isp']
    other = retDict

    ret = {}
    ret['ip'] = ip    
    ret['country'] = country
    ret['area'] = area    
    ret['region'] = region    
    ret['city'] = city    
    ret['isp'] = isp    
    ret['other'] = other    
 
    return ret

def readHttp(postUrl, data=""):
    retData = ''
    try:    
        request = urllib2.Request(postUrl, data)
        response = urllib2.urlopen(request, "", 30)
        retData = response.read()
        response.close()
    except Exception, e:
        logging.error("[error in getting data][%s][%s]" % (postUrl, e))
    return retData 

def askIpLocation(ip, ipData='taobao'):
    if ipData == 'taobao':
        url = urlIpQuery_taobao % (ip)
        ret = anaTaobao(url)        
    else:
        return {}
    return ret

def checkIpList(ipList, ipData='taobao'):
    retList = []
    for each in ipList:
        ret = askIpLocation(each)
        retList.append([each, ret]) 
        time.sleep(0.1)
    return retList

def locationDict2TidyStr(adict):
    theStr = ("|%-15s|" + "%-8s|"*5) % (adict['ip'], adict['country'], \
                            adict['area'], adict['region'], \
                            adict['city'], adict['isp'])
    return theStr

if __name__ == '__main__':
    ipTest = "202.118.250.20"
    print "test:"
    print "ask ip %s" % (ipTest)
    print ("|%-15s|" + "%-8s|"*5) % ('ip', '国家','地区', '省份', '城市', '运营商')
    for each in  checkIpList([ipTest, "202.118.250.220"]):
        print locationDict2TidyStr(each[1]).encode('utf8')
