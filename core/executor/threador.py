from concurrent.futures import ThreadPoolExecutor
from core import Options
from core.utils import Logger
import requests
import time


def request_(url):
    target = Options.target
    if target.endswith('/'):
        target = target[:-1]
    if url.startswith('/'):
        url = url[1:]
    url = "%s/%s" % (target, url)
    if Options.detail:
        Options.lock.acquire()
        Logger.log('发送请求：', url)
        Options.lock.release()

    # 网络请求
    try:
        res = requests.get(url)
    except Exception as e:
        Logger.log(e)
        return
    for status_code in Options.status_code:
        if status_code == '3XX':
            if str(res.status_code).startswith('3'):
                Options.lock.acquire()
                Logger.log('发现：', url, status_code)
                Options.win_msd.add_result(url, res.status_code)
                Options.lock.release()
        elif int(status_code) == res.status_code:
            Options.lock.acquire()
            Logger.log('发现：', url, status_code)
            Options.win_msd.add_result(url, res.status_code)
            Options.lock.release()

    if Options.delay and Options.delay > 0:
        # 设置延迟
        time.sleep(Options.delay)


def create_thread_pool(n):
    return ThreadPoolExecutor(max_workers=n)


def exec_tasks(executor, url):
    return executor.submit(request_, url)
