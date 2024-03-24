import os
import time
import threading


def runcommand(cmd, direc):
    os.chdir(direc)
    res = os.system(cmd)
    if res:
        c = cmd.split()[0]
        fail(color.lred + c + ' failed.' + color.reset)


def dispatch_command(cmd):
    if configuration.paralell == 1:
        runcommand(cmd, os.getcwd())
    else:
        mpool.apply_async(runcommand, [(cmd, os.getcwd()),])


def wait_until_pool_end(cmd, direc):
    while making.value:
        time.sleep(0.001)
    runcommand(cmd, direc)


class Rust:
    def __init__(self, source, target, flags=[]) -> None:
        cmd = 'rustc '
        for f in flags:
            cmd += f + ' '
        cmd += '"' + source + '" '
        cmd += '-o "' + target + '"'
        print(
            color.lyellow + 'rustc' + color.reset + ' ' + color.blue +
            '-->' + color.reset + ' ' + color.lgreen + ' ' + target + color.reset)
        dispatch_command(cmd)


class Linker:
    def __init__(self, source: list[str] | str, target, linklib=list[str], ldscript: str | None = None, flags=[]):
        cmd = "ld "
        if ldscript != None:
            cmd += '-T "' + ldscript + '" '
        for f in flags:
            cmd += f + ' '
        if type(source) == str:
            cmd += '"' + source + '" '
        else:
            for s in source:
                cmd += '"' + s + '" '
        for l in linklib:
            cmd += '"' + l + '" '
        cmd += '-o "' + target + '"'
        plasma = color.lyellow + 'ld' + color.reset + ' ' + color.lgreen + \
            target + color.reset + ' ' + color.blue + '<--' + color.reset + ' '
        if type(source) == str:
            plasma += color.green + source + color.reset + ' '
        else:
            for s in source:
                plasma += color.green + s + color.reset + ' '
        print(plasma)
        threading.Thread(
            target=wait_until_pool_end,
            args=(cmd, os.getcwd())).start()
