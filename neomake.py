#!/usr/bin/python

import nmprofiles
from nmprofiles import *
import platform as __pf
import os
import sys
import multiprocessing
import hashlib


sys.path.append(os.path.dirname(__file__))


class color:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    pink = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    lblack = '\033[1;30m'
    lred = '\033[1;31m'
    lgreen = '\033[1;32m'
    lyellow = '\033[1;33m'
    lblue = '\033[1;34m'
    lpink = '\033[1;35m'
    lcyan = '\033[1;36m'
    lwhite = '\033[1;37m'
    reset = '\033[0m'


class configuration:
    target = ''
    paralell = 1
    make_options = []


def __load_cmdline__():
    __first__ = True
    for arg in sys.argv:
        if __first__:
            __first__ = False
            continue
        if not arg.startswith('-'):
            if configuration.target != '':
                print('You can only make one target.')
                exit(1)
            configuration.target = arg
        else:
            if arg.startswith('-j'):
                p__ = arg.removeprefix('-j')
                configuration.paralell = int(p__)
            elif arg.startswith('-'):
                configuration.make_options.append(arg)


__load_cmdline__()


mpool = multiprocessing.Pool(processes=configuration.paralell)


# 操作系统名
Linux = 'Linux'
Windows = 'Windows'
Darwin = 'Darwin'

# CPU架构名
x86_64 = 'x86_64'
armv7l = 'armv7l'
aarch64 = 'aarch64'
ppc = 'ppc'
ppc64 = 'ppc64'
riscv = 'riscv'
riscv64 = 'riscv64'
loongarch = 'loongarch'
loongarch64 = 'loongarch64'


class platform:
    os = ''
    arch = ''


platform.os = __pf.system()
platform.arch = __pf.machine()


def depcheck(dep) -> bool:
    pathsenv = os.environ.get("PATH").split(":")
    for software, progs in dep.items():
        print(
            "Checking " + color.lcyan +
            f"{software}" + color.reset + " ...")
        for program in progs:
            exists = False
            for path in pathsenv:
                if os.path.isfile(os.path.join(path, program)):
                    exists = True
                    break
            if exists:
                print(
                    "  " + color.lyellow +
                    f"{program}" + color.reset + " existed.")
            else:
                print(
                    "  " + color.lred +
                    f"{program}" + color.reset + " not found.")

                print(
                    "Software " + color.lred + f"{software}" +
                    color.reset + " is not installed or completed.")
                return False
    print(
        "All dependencies are " +
        color.lgreen + "satisfied." + color.reset)
    return True


def touch(file):
    with open(file, 'w'):
        pass


class Target:
    def __init__(self, path: str | None, dependents, making, static=False):
        self.path = path
        self.dependents = dependents
        self.making = making
        self.static = static

    def fill_dependents(self, options):
        for tar in self.dependents:
            if type(tar) != str: # 忽略字符串类型的依赖目标，因为字符串类型的依赖目标通常是源代码
                tar.make(options)

    def should_make(self) -> bool:
        if self.path == None:
            return True
        elif not os.path.exists(self.path):
            return True
        else:
            tartime = os.path.getmtime(self.path)
            deptime = 0
            for dep in self.dependents:
                if type(dep) == str:
                    if os.path.exists(dep):
                        deptime = max(deptime, os.path.getmtime(dep))
                else:
                    if os.path.exists(dep.path):
                        deptime = max(deptime, os.path.getmtime(dep.path))
            return tartime < deptime

    def make(self, options):
        self.fill_dependents(options)
        if not self.should_make():
            return
        if self.making != None:
            deplist = []
            for d in self.dependents:
                if type(d) != str:
                    deplist.append(d.path)
                else:
                    deplist.append(d)
            self.making(self.path, deplist)

    def clear(self):
        print('try remove', os.getcwd() + '/' + str(self.path))
        if not self.static and self.path != None and os.path.exists(self.path):
            os.remove(self.path)
        for dep in self.dependents:
            if type(dep) != str:
                dep.clear()


class TargetGroup:
    targets = []
    def __init__(self, targets: dict, making):
        for key, val in targets.items():
            self.targets.append(Target(key, val, making))


making = multiprocessing.Value('i', 1)


def start_neomake():
    pass


def end_neomake():
    global making
    mpool.close()
    mpool.join()
    making.value = 0


def fail(s):
    print(s)
    end_neomake()
    exit(1)


setattr(nmprofiles, 'configuration', configuration)
setattr(nmprofiles, 'mpool', mpool)
setattr(nmprofiles, 'color', color)
setattr(nmprofiles, 'making', making)
setattr(nmprofiles, 'fail', fail)


def md5sum(s):
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()


global_metadata = {}
