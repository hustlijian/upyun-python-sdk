#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import readline
import sys
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

class UpyunShell(object):
    def __init__(self, upyun):
        self.upyun = upyun

        self.upyun_commands = {
            'put': self.put,
            'get': self.get,
            'getinfo': self.getinfo,
            'delete': self.delete,
            'mkdir': self.mkdir,
            'getlist': self.getlist,
            'usage': self.usage,
        }
        self.shell_commands = {
            #'cd': self.set_path,
            #'ls': self.list_local,
            'help': self.help,
            '?': self.help,
            'quit': self.exit,
        }

        self.commands = dict(
            self.upyun_commands.items() + self.shell_commands.items())
        self.path = os.getcwd()

        self.init_readline()

    def init_readline(self):
        upyunsh_dir = os.path.join(os.path.expanduser('~'), '.upyunshell/')
        if not os.path.isdir(upyunsh_dir):
            os.mkdir(upyunsh_dir)

        self.history_file = os.path.join(upyunsh_dir, '.history')

        try:
            readline.read_history_file(self.history_file)
        except IOError:
            pass

        readline.set_completer(self.complete)
        readline.parse_and_bind('tab: complete')

    def put(self, args):
       self.upyun.put(args[0], args[1]) 

    def get(self, args):
        self.upyun.get(args[0], args[1])

    def getinfo(self, args):
        self.upyun.getfileinfo(args[0])

    def delete(self, args):
        self.upyun.delete(args[0])

    def mkdir(self, args):
        self.upyun.mkdir(args[0])

    def getlist(self, args):
        self.upyun.getlist(args[0])

    def usage(self, args):
        self.upyun.usage()

    def help(self, args):
        print 'invalid command:'
        for i in self.commands.keys():
            print '%6s'%i,
        print ''
    
    def exit(self, args):
       readline.write_history_file(self.history_file) 
       sys.exit(0)

    def complete(self, text, state):
        match = [s for s in self.commands.keys() if s
            and s.startswith(text)] + [None]
        return match[state]

    def prompt(self):
        #return '[UpyunShell@%s] > ' %(self.path)
        return 'upyun $ '

    def input_loop(self):
        command = None
        while True:
            try:
                input = raw_input(self.prompt()).split()
                
                # ignore blank input
                if not input or len(input) == 0:
                    continue

                command = input.pop(0).lower()
                if command in self.commands:
                    try:
                        self.commands[command](input[:])
                    except Exception as e:
                        print 'command error %s'%e
                else:
                    self.help(input[:])
            except (EOFError, KeyboardInterrupt):
                break

def main():
    args = parse_command_line()
    up = upyun.UpYun(args.bucket, args.user, args.passwd, timeout=args.timeout, baseurl=(args.baseurl and BASE[args.baseurl]))
    shell = UpyunShell(up)
    shell.input_loop()

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
