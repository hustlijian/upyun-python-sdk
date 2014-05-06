#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import sys
import cmd
import upyun

BASE = {}
BASE['auto'] = upyun.BASE_LIST[0]
BASE['telecom'] = upyun.BASE_LIST[1]
BASE['cnc'] = upyun.BASE_LIST[2]
BASE['ctt'] = upyun.BASE_LIST[3]


def parse_command_line():
    parser = argparse.ArgumentParser(
       description='An interactive shell for upyun')

    parser.add_argument(
        'bucket',
        help='bucket name of upyun')

    parser.add_argument(
        'user',
        help='user name of upyun')

    parser.add_argument(
        'passwd',
        help='password of upyun')

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        dest='timeout',
        help='timeout of each request')

    parser.add_argument(
        '-b', '--baseurl',
        choices=['auto', 'telecom', 'cnc', 'ctt'],
        dest='baseurl',
        help='the base url network SP(service provider)')

    return parser.parse_args()

class Shell(cmd.Cmd):
    '''
    upyun shell 
    '''
    def cmdloop(self, upyun, intro=None):
        self.prompt = '(upyun)-> '
        self.upyun = upyun
        return cmd.Cmd.cmdloop(self, intro)

    def do_shell(self, line):
        '''
        run some shell command
        '''
        output = os.popen(line).read()
        print output

    def do_put(self, args):
        '''
        put LOCALFILE DEST_URI
        put localfile to dest uri
        '''
        args = args.split()
        self.upyun.put(args[0], args[1]) 

    def do_get(self, args):
        '''
        get SRC_URI LOCALFILE
        get uri file to localfile
        '''
        args = args.split()
        self.upyun.get(args[0], args[1])

    def do_getinfo(self, args):
        '''
        getinfo URI
        get information of uri
        '''
        args = args.split()
        self.upyun.getfileinfo(args[0])

    def do_delete(self, args):
        '''
        delete URI
        delete a uri of file or dirctory
        '''
        args = args.split()
        self.upyun.delete(args[0])

    def do_mkdir(self, args):
        '''
        mkdir NEWDIR_URI
        make a new dirctory
        '''
        args = args.split()
        self.upyun.mkdir(args[0])

    def do_getlist(self, args):
        '''
        getlist [URI]
        get list of uri 
        '''
        if args:
            args = args.split()
            self.upyun.getlist(args[0])
        else:
            self.upyun.getlist('/')

    def do_usage(self, args):
        '''
        usage
        get the total usage space
        '''
        args = args.split()
        print self.upyun.usage()

    def do_exit(self, args):
        '''
        exit shell
        '''
        return True

    def do_EOF(self, args):
        '''
        exit shell (ctrl+d)
        '''
        return True

def main():
    args = parse_command_line()
    up = upyun.UpYun(args.bucket, args.user, args.passwd, timeout=args.timeout, baseurl=(args.baseurl and BASE[args.baseurl]))
    Shell().cmdloop(up,intro='Welcome to upyun shell\n'+'-'*50)

def upyun_test():
    up = upyun.UpYun(BUCKET_NAME, USERNAME, PASSWD)
    print up.usage() + ' B'
    up.put('./README.md', 'readme.txt')
    up.getlist()
    up.get('readme.txt', './readme.txt')
    up.getfileinfo('readme.txt')
    up.delete('readme.txt')
    up.getlist()
    up.mkdir('/newdir/')
    up.getlist()
    up.delete('/newdir')
    up.getlist()

if __name__ == '__main__':
    main()
