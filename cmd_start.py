from core import *
from core import startserver

Options.status_code = ['200', '3XX', '500']
Options.languages = ['php']
Options.target = 'https://www.bilibili.com'
Options.detail = True
Options.concurrency = 0
Options.debug = True

# 启动
startserver.startup()
