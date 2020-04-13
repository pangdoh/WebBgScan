from wbs.core import *


# 显示调试信息
def debug(*args, sep=' ', end='\n', file=None):
    if Options.debug:
        print(*args, sep=sep, end=end, file=file)


# 显示日志
def log(*args, sep=' ', end='\n', file=None):
    print(*args, sep=sep, end=end, file=file)
