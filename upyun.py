#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import hashlib
import requests
from urllib import quote

BASE_LIST = ['http://v%d.api.upyun.com' % i for i in range(4)]
BASE_AUTO, BASE_TELECOM, BASE_CNC, BASE_CTT = BASE_LIST

str = unicode

def get_datetime():
    '''
    >>> print get_datetime()
    '''
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

class UpYun():
    def __init__(self, bucket, user, passwd, timeout=None, baseurl=None):
        self.bucket = bucket
        self.user = user
        self.passwd = hashlib.md5(passwd).hexdigest()
        self.timeout = timeout or 60
        self.baseurl = baseurl or BASE_AUTO

    def put(self, localfile, dest_path, headers=None, params=None, args=''):
        '''
        >>> r = up.put('/path/to/localfile', '/path/to/upyun/file')
        '''
        method = 'PUT'
        if not headers:
            headers = {}
        headers['Mkdir'] = 'true'

        uri = '/' + self.bucket
        if dest_path[0] != '/':
            uri += '/'
        uri += dest_path

        if isinstance(uri, str):
            uri = uri.encode('utf-8')

        uri = quote(uri, safe="~/") + args

        length = os.path.getsize(localfile)

        datetime = get_datetime()
        sig = self.__get_signature(method, uri, datetime, length)

        headers['Date'] = datetime
        headers['Content-Length'] = length
        headers['Authorization'] = sig

        URL = self.baseurl + uri
        
        #response = requests.Session().request(method,URL, files=files, headers=headers)
        fh = open(localfile, 'rb')
        mydata = fh.read()
        response = requests.put(URL, data=mydata, headers=headers)
        print response.status_code

    def __get_signature(self, method, uri, date, length):
        sigstr = '&'.join([method, uri, date, str(length), self.passwd])
        sig = hashlib.md5(sigstr).hexdigest()
        print 'sig: '+sig
        return 'UpYun ' + self.user + ':' + sig


if __name__ == '__main__':
    #print get_datetime()
    up = UpYun('cli-bucket', 'lijian', 'qwerasdf')
    up.put('./README.md', 'readme.txt')
    pass
