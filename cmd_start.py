from core import *
from core import startserver


# 配置参数
Options.target = 'http://47.244.17.247/'
Options.debug = True
Options.status_code = [200, 304]
Options.concurrency = 2
Options.languages = ['php']
# Options.delay = 1
Options.detail = True


# 启动
startserver.startup()
