from core import *
from core.utils import Logger
from core.executor import threador
import threading
import time


def startup():
    Logger.log('配置信息:')
    for attr in dir(Options):
        if attr.startswith('__'):
            continue
        Logger.log("    >> %s:" % attr, getattr(Options, attr))

    if Options.delay and Options.delay > 0:
        n = 1
    elif Options.concurrency == 2:
        n = 32
    elif Options.concurrency == 1:
        n = 8
    else:
        n = 2

    Logger.debug('线程池大小：', n)
    # 创建线程池
    po = threador.create_thread_pool(n)
    # 创建锁对象
    StaticArea.lock = threading.Lock()

    # 创建计时器
    timer = 0

    for language in iter(Options.languages):
        # 读取字典
        dict_file = 'dict/%s' % language
        with open(dict_file, encoding='utf-8') as f:
            while True:
                url = f.readline()
                if not url:
                    break
                url = url.strip()
                if url == '':
                    continue
                if timer > n:
                    time.sleep(2)
                    timer = 0
                else:
                    timer += 1
                # 执行网络请求
                threador.exec_tasks(po, url)
                # 配置任务数量信息
                StaticArea.task_number += 1
                StaticArea.task_queue += 1
    Logger.log('文件读取完毕')
