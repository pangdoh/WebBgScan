from concurrent.futures import ThreadPoolExecutor
from core import *
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
        StaticArea.lock.acquire()
        StaticArea.request_times += 1
        StaticArea.task_queue -= 1
        Logger.log('发送请求：', url)
        StaticArea.lock.release()

    # 网络请求
    res = None
    try:
        if Options.headers:
            headers = Options.headers
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate",
            }
        res = requests.get(url, headers=headers)
        StaticArea.lock.acquire()
        if StaticArea.conn_error_rate > 0:
            StaticArea.conn_error_rate -= 1
        StaticArea.lock.release()
    except requests.exceptions.ConnectionError as e:
        StaticArea.lock.acquire()
        StaticArea.conn_error_rate += 1
        StaticArea.error_times += 1
        Logger.log('可能需要关闭扫描')
        Logger.log(e)
        StaticArea.lock.release()
    except requests.exceptions.MissingSchema as e:
        Logger.log('无效url:', url)
        print(e)
    except Exception as e:
        StaticArea.lock.acquire()
        StaticArea.error_times += 1
        Logger.log(e)
        StaticArea.lock.release()

    StaticArea.lock.acquire()
    StaticArea.completed += 1
    StaticArea.lock.release()
    if res:
        for status_code in Options.status_code:
            if status_code == '3XX':
                if str(res.status_code).startswith('3'):
                    StaticArea.lock.acquire()
                    Logger.log('发现：', url, status_code)
                    if StaticArea.win_msd:
                        StaticArea.win_msd.add_result(url, res.status_code)
                    StaticArea.lock.release()
            elif int(status_code) == res.status_code:
                StaticArea.lock.acquire()
                Logger.log('发现：', url, status_code)
                if StaticArea.win_msd:
                    StaticArea.win_msd.add_result(url, res.status_code)
                StaticArea.lock.release()

    if Options.debug:
        StaticArea.lock.acquire()
        Logger.log('任务数量：', StaticArea.task_number)
        Logger.log('任务队列：', StaticArea.task_queue)
        Logger.log('发送请求：', StaticArea.request_times)
        Logger.log('完成请求：', StaticArea.completed)
        Logger.log('error_times：', StaticArea.error_times)
        Logger.log('conn_error_rate：', StaticArea.conn_error_rate)
        StaticArea.win_msd.set_request_number(task_number=StaticArea.task_number, task_queue=StaticArea.task_queue,
                                              request_times=StaticArea.request_times, completed=StaticArea.completed)
        StaticArea.lock.release()

    if Options.delay and Options.delay > 0:
        # 设置延迟
        time.sleep(Options.delay)


def create_thread_pool(n):
    return ThreadPoolExecutor(max_workers=n)


def exec_tasks(executor, url):
    return executor.submit(request_, url)
