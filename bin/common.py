#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by cheungzee.com

import os
import os.path
import re
import pickle
import struct
import socket
import json





class CommonConfParser(object):
    """
        class for Reading conf files
    """
    @classmethod
    def readConfInList(cls, ConfPath, regDelimiter=''):
        "read files, strip NR, ignore empty lines"
        f = open(ConfPath, 'r') 
        retLines = []
        for each in f:
            each = each.strip()
            if each.strip() == '':
                continue
            if regDelimiter == '':
                retLines.append(each)
            else:
                lineList = re.split(regDelimiter, each) 
                retLines.append(lineList)
        return retLines

class CommonPathNavigator(object):
    @classmethod
    def listDir(cls, dirPath, pre=''):
        """
            list files in firPath
            if pre exists, it would join the path:
            os.path.join(pre, each)
        """
        retList = []
        tmpList = os.listdir(dirPath)
        if pre != '':
            for each in tmpList:
                retList.append(os.path.join(pre, each))
        else:
            retList = tmpList
        return retList

    @classmethod
    def getFileList(cls, dirPath):
        """
            get all the files in this dir
        """
        ret = []
        for each in os.walk(dirPath):
            baseDir = each[0] 
            for eachFile in each[2]:
                filePath = os.path.join(baseDir, eachFile)
                ret.append(filePath)
        return ret


class Common(object):
    @staticmethod
    def dumpPickle(filePath, adict):
        'in pickle' 
        f = open(filePath, 'w')
        ret = pickle.dump(adict, f)
        f.close()
        return ret

    @staticmethod
    def int2Ip(intVal):
        return socket.inet_ntoa(struct.pack("!I", intVal))

    @staticmethod
    def ip2Int(ip):
        return struct.unpack("!I",socket.inet_aton(ip))[0] 

    @staticmethod
    def ip2Ipc(ip):
        return ip[:ip.rfind('.')]

    @staticmethod
    def ipc2Ip(ipc):
        return ipc + '.0'

    @classmethod
    def ipc2Int(cls, ipc):
        ip = cls.ipc2Ip(ipc)
        return cls.ip2Int(ip)

    @classmethod
    def int2Ipc(cls, intVal):
        ip = cls.int2Ip(intVal)
        return cls.ip2Ipc(ip)

    @staticmethod
    def loadPickle(filePath):
        'in pickle' 
        f = open(filePath, 'r')
        Adict = pickle.load(f)
        f.close()
        return Adict

    @classmethod
    def __stringAlist(cls, alist, indent=4):
        ret = ""
        for each in alist:
            eachVal = each
            if type(each) == int:
                eachVal = cls.int2Ip(each)

            if type(each) == dict:
                ret += "%s%s(%s):\n%s\n" % (' '*indent, each, eachVal, cls.__stringAdict(each, indent+4))
            elif type(each) == list:
                ret += "%s%s(%s):%s\n" % (' '*indent, each, eachVal, cls.__stringAlist(each, indent+4))
            else:
                ret += "%s%s(%s):%s\n" % (' '*indent, each, eachVal, each)
        return ret

    @classmethod
    def __stringAdict(cls, adict, indent=4):
        ret = ""
        for each in sorted(adict.keys()):
            eachVal = each
            if type(each) == int:
                eachVal = cls.int2Ip(each)

            if type(adict[each]) == dict:
                ret += "%s%s(%s):\n%s\n" % (' '*indent, each, eachVal, cls.__stringAdict(adict[each], indent+4))
            elif type(adict[each]) == list:
                ret += "%s%s(%s):%s\n" % (' '*indent, each, eachVal, cls.__stringAlist(adict[each], indent+4))
            else:
                ret += "%s%s(%s):%s\n" % (' '*indent, each, eachVal, adict[each])
        return ret

    @classmethod
    def writeAlist(cls, filePath, list):
        f = open(filePath, 'w')
        strDict = cls.__stringAlist(list) 
        f.write(strDict)
        f.close()

    @staticmethod
    def dumpAdict(filePath, adict):
        'in JSON' 
        f = open(filePath, 'w')
        ret = json.dump(adict, f)
        f.close()
        return ret 

    @staticmethod
    def loadAdict(filePath):
        'in JSON'
        f = open(filePath, 'r')
        Adict = json.load(f)
        f.close()
        return Adict

    @staticmethod
    def dumpPickle(filePath, adict):
        'in pickle'
        f = open(filePath, 'w')
        ret = pickle.dump(adict, f)
        f.close()
        return ret

    @staticmethod
    def loadPickle(filePath):
        'in pickle'
        f = open(filePath, 'r')
        Adict = pickle.load(f)
        f.close()
        return Adict

    @classmethod
    def writeAdict(cls, filePath, adict):
        f = open(filePath, 'w')
        strDict = cls.__stringAdict(adict)
        f.write(strDict)
        f.close()

    @classmethod
    def stringAdict(cls, adict, indent=4):
        return cls.__stringAdict(adict, indent)

