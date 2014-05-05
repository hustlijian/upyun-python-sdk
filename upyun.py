#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import hashlib
import requests
from urllib import quote

BASE_LIST = ['http://v%d.api.upyun.com' % i for i in range(4)]
BASE_AUTO, BASE_TELECOM, BASE_CNC, BASE_CTT = BASE_LIST

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
        response = requests.put(URL, data=mydata, headers=headers, timeout=self.timeout)
        print response.status_code

    def get(self, uri, localfile):
        '''
        >>> up.get('/path/to/upyun/file', '/path/to/localfile')
        '''
        method = 'GET'
        headers = {}
        URI = '/' + self.bucket
        if uri[0] != '/':
            URI += '/'
        URI += uri
        uri = URI
        if isinstance(uri, str):
            uri = uri.encode('utf-8')
        datetime = get_datetime()
        sig = self.__get_signature(method, uri, datetime, 0)

        headers['Date'] = datetime
        headers['Authorization'] = sig

        URL = self.baseurl + uri
        response = requests.get(URL, headers=headers, timeout=self.timeout)
        print response.status_code
        fh = open(localfile, 'w')
        fh.write(response.content)
        fh.close()

    def getfileinfo(self, uri):
        '''
        >>> up.getfileinfo('/path/to/upyun/file')
        '''
        method = 'HEAD'
        headers = {}
        URI = '/' + self.bucket
        if uri[0] != '/':
            URI += '/'
        URI += uri
        uri = URI
        if isinstance(uri, str):
            uri = uri.encode('utf-8')
        datetime = get_datetime()
        sig = self.__get_signature(method, uri, datetime, 0)

        headers['Date'] = datetime
        headers['Authorization'] = sig

        URL = self.baseurl + uri
        response = requests.head(URL, headers=headers, timeout=self.timeout)
        print response.status_code
        info = response.headers.items()
        res = dict(iter([(k[8:].lower(), v) for k, v in info 
                    if k[:8].lower() == 'x-upyun-']))
        print res
        return res

    def delete(self, uri):
        '''
        >>> up.delete('/path/to/upyun/file')
        >>> up.delete(('/path/to/upyun/dirctory')
        '''
        method = 'DELETE'
        headers = {}
        URI = '/' + self.bucket
        if uri[0] != '/':
            URI += '/'
        URI += uri
        uri = URI
        if isinstance(uri, str):
            uri = uri.encode('utf-8')
        datetime = get_datetime()
        sig = self.__get_signature(method, uri, datetime, 0)

        headers['Date'] = datetime
        headers['Authorization'] = sig

        URL = self.baseurl + uri
        response = requests.delete(URL, headers=headers, timeout=self.timeout)
        print response.status_code

    def mkdir(self, uri):
        '''
        >>> up.mkdir('/path/to/new/upyun/dirctory')
        '''
        method = 'POST'
        headers = {}
        headers['folder']= 'true'
        headers['mkdir']= 'true'
        URI = '/' + self.bucket
        if uri[0] != '/':
            URI += '/'
        URI += uri
        uri = URI
        if isinstance(uri, str):
            uri = uri.encode('utf-8')
        datetime = get_datetime()
        sig = self.__get_signature(method, uri, datetime, 0)

        headers['Date'] = datetime
        headers['Authorization'] = sig

        URL = self.baseurl + uri
        response = requests.post(URL, headers=headers, timeout=self.timeout)
        print response.status_code

    def getlist(self, uri='/'):
        '''
        >>> up.getlist()
        >>> up.getlist(uri='/newdir')
        '''
        method = 'GET'
        headers = {}
        URI = '/' + self.bucket
        if uri[0] != '/':
            URI += '/'
        URI += uri
        uri = URI
        if isinstance(uri, str):
            uri = uri.encode('utf-8')
        datetime = get_datetime()
        sig = self.__get_signature(method, uri, datetime, 0)

        headers['Date'] = datetime
        headers['Authorization'] = sig

        URL = self.baseurl + uri
        response = requests.get(URL, headers=headers, timeout=self.timeout)
        print response.status_code
        content = response.content
        items = content.split('\n')
        res = [dict(zip(['name', 'type', 'size', 'time'],
                x.split('\t'))) for x in items]
        for i in res:
            print '%10s %2s %10s %10s'%(i['name'], i['type'], i['size'], i['time'])
        print ''
        return res

    def usage(self):
        '''
        >>> up.usage()
        '''
        args = '?usage'
        method = 'GET'
        headers = {}
        uri = '/'
        URI = '/' + self.bucket
        URI += uri
        uri = URI
        if isinstance(uri, str):
            uri = uri.encode('utf-8')
        uri = quote(uri, safe="~/") + args
        datetime = get_datetime()
        sig = self.__get_signature(method, uri, datetime, 0)

        headers['Date'] = datetime
        headers['Authorization'] = sig

        URL = self.baseurl + uri
        response = requests.get(URL, headers=headers, timeout=self.timeout)
        print response.status_code

        res = response.content
        return res

    def __get_signature(self, method, uri, date, length):
        sigstr = '&'.join([method, uri, date, str(length), self.passwd])
        sig = hashlib.md5(sigstr).hexdigest()
        return 'UpYun ' + self.user + ':' + sig


if __name__ == '__main__':
    #print get_datetime()
    up = UpYun('cli-bucket', 'lijian', 'qwerasdf')
    #up.put('./README.md', 'readme.txt')
    #up.get('readme.txt', './readme.txt')
    #up.getfileinfo('readme.txt')
    #up.delete('readme.txt')
    #up.mkdir('/newdir/')
    #up.getlist()
    up.usage()
