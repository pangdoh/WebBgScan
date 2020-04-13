from wbs.core import *
from wbs.core import startserver

"""
仅用于测试，当前状态：不可用
"""

Options.status_code = ['200', '3XX', '500']
Options.languages = ['php']
Options.target = 'https://www.bilibili.com/'
Options.detail = True
Options.concurrency = 1
Options.debug = True
# Options.delay = 1

# 启动
startserver.startup()
