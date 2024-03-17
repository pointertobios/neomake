#!/usr/bin/python

import inspect
import re
import os

class profile:
    def c(target, deps: list[str], compiler: str = "gcc", flags: list[str] = []):
        cmd = compiler + " "
        for file in deps:
            cmd += file + " "
        for flag in flags:
            cmd += flag + " "
        cmd += "-o " + target
        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    with open("nmake") as file:
        script = file.read()
    script = re.sub(r"(?<![A-Za-z0-9_])target(?![A-Za-z0-9_])", "inspect.currentframe().f_code.co_name", script)
    print(script)
    exec(script)
    for f in targets:
        f()
