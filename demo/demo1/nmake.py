#!/usr/bin/python -B

import sys
sys.path.append('../../')
from neomake import *


def make_main(target, deplist):
    C(deplist, target)


main = Target('main', ['lib.c', 'main.c'], make_main)

start_neomake()

if 'build' in sys.argv:
    main.make()

elif 'clear' in sys.argv:
    main.clear()

end_neomake()
