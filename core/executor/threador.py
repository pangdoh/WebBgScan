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
        Logger.log('发送请求：', url)

    # 网络请求
    res = requests.get(url)
    for status_code in Options.status_code:
        if status_code == '3XX':
            if str(res.status_code).startswith('3'):
                Logger.log('发现：', url, status_code)
        elif int(status_code) == res.status_code:
            Logger.log('发现：', url, status_code)

    if Options.delay and Options.delay > 0:
        # 设置延迟
        time.sleep(Options.delay)


def create_thread_pool(n):
    return ThreadPoolExecutor(max_workers=n)


def exec_tasks(executor, url):
    task_result = executor.submit(request_, url)
    # print(task_result.done())
