#!/usr/bin/python

import inspect as __inspect
import re as __re
import platform as __pf
import os as __os
import sys as __sys


__sys.path.append('./')


class __configuration__:
    target = ''
    paralell = 1
    make_options = []


def __load_cmdline__():
    __first__ = True
    for arg in __sys.argv:
        if __first__:
            __first__ = False
            continue
        if not arg.startswith('-'):
            if __configuration__.target != '':
                print('You can only make one target.')
                exit(1)
            __configuration__.target = arg
        else:
            if arg.startswith('-j'):
                p__ = arg.removeprefix('-j')
                __configuration__.paralell = int(p__)
            elif arg.startswith('-'):
                __configuration__.make_options.append(arg)


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


def make(directory, target, options):
    __script__ = directory.__name__ + '/nmake'
    with open("nmake") as file:
        script__ = file.read()
    script__ = __re.sub(
        r"(?<![A-Za-z0-9_])target(?![A-Za-z0-9_])",
        "__inspect.currentframe().f_code.co_name", script__)
    exec(script__)
    target_list = targets
    __make__(target, target_list, )


def fail(s):
    print(s)
    exit(1)


def depcheck(dep) -> bool:
    pathsenv = __os.environ.get("PATH").split(":")
    for software, progs in dep.items():
        print(
            "Checking " + color.lcyan +
            f"{software}" + color.reset + " ...")
        for program in progs:
            exists = False
            for path in pathsenv:
                if __os.path.isfile(__os.path.join(path, program)):
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


def __make__(target, target_list, cwd):
    for tar in target_list:
        if tar.__name__ != target:
            continue
        params = __inspect.signature(tar).parameters
        dependencies = []
        executable = False
        for name, obj in params.items():
            if name == "dep":
                if type(obj.default) == list:
                    for deptars in obj.default:
                        dependencies.append(deptars)
                elif type(obj.default) == str:
                    dependencies.append(obj.default)
            elif name == "exec":
                executable = True
        if not executable and __os.path.exists(cwd + '/' + tar.__name__):
            return
        for dep in dependencies:
            __make__(dep, cwd)
        tar(__configuration__.make_options)


if __name__ == "__main__":
    __load_cmdline__()
    with open("nmake") as file:
        script__ = file.read()
    script__ = __re.sub(
        r"(?<![A-Za-z0-9_])target(?![A-Za-z0-9_])",
        "__inspect.currentframe().f_code.co_name", script__)
    exec(script__)

    target_list = targets
    __make__(__configuration__.target, target_list, __os.getcwd())
