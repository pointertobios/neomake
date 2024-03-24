# Neomake

基于Python的底层构建系统。

## 示例

项目目录：

```bash
.
├── lib.c
├── main.c
└── nmake.py
```

`nmake.py`

```python
#!/usr/bin/python -B
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
```

构建项目：

```bash
$ ./nmake.py build
gcc lib.c main.c --> main
```

清理生成的额外文件：

```bash
$ ./nmake.py clear
removing main
```
