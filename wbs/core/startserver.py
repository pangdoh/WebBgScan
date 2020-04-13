from wbs.core.utils import Logger
from wbs.core.executor import threador
from wbs.core import *
import threading
import time
from PyQt5.QtWidgets import QApplication


def startup():
    Logger.log('配置信息:')
    for attr in dir(Options):
        if attr.startswith('__'):
            continue
        Logger.log("    >> %s:" % attr, getattr(Options, attr))

    if Options.delay and Options.delay > 0:
        n = 1
    elif Options.concurrency == 2:
        n = 16
    elif Options.concurrency == 1:
        n = 4
    else:
        n = 1

    Logger.debug('线程池大小：', n)
    # 创建线程池
    po = threador.create_thread_pool(n)
    # 创建锁对象
    StaticArea.lock = threading.Lock()

    for language in iter(Options.languages):
        # 读取字典
        dict_file = 'dict/%s' % language
        with open(dict_file, encoding='utf-8') as f:
            while True:
                StaticArea.lock.acquire()
                request_times = StaticArea.request_times
                completed = StaticArea.completed
                error_times = StaticArea.error_times
                StaticArea.lock.release()

                # 当前状态
                status_value = '执行中'
                end_flag = False

                while StaticArea.win_msd.end:
                    if request_times == completed + error_times:
                        end_flag = True
                        break
                    else:
                        time.sleep(1)
                        status_value = '正在结束...'
                        # 前端刷新
                        StaticArea.lock.acquire()
                        StaticArea.win_msd.w.label_status_value.setText(status_value)
                        QApplication.processEvents()
                        StaticArea.lock.release()
                if end_flag:
                    status_value = '已结束'
                    # 前端刷新
                    StaticArea.lock.acquire()
                    StaticArea.win_msd.w.label_status_value.setText(status_value)
                    QApplication.processEvents()
                    StaticArea.lock.release()
                    break

                while StaticArea.win_msd.stop:
                    status_value = '暂停'
                    time.sleep(1)
                    # 前端刷新
                    StaticArea.lock.acquire()
                    StaticArea.win_msd.w.label_status_value.setText(status_value)
                    QApplication.processEvents()
                    StaticArea.lock.release()

                url = f.readline()
                if not url:
                    break
                url = url.strip()
                if url == '':
                    continue
                if StaticArea.conn_error_rate > 5 * n:
                    print('连续性远程主机强制拒绝连接，扫描被迫关闭。')
                    StaticArea.win_msd.logger('连续性远程主机强制拒绝连接，扫描被迫关闭。')
                    break
                # 执行网络请求
                threador.exec_tasks(po, url)

                # 前端刷新
                StaticArea.lock.acquire()
                StaticArea.win_msd.w.label_status_value.setText(status_value)
                QApplication.processEvents()
                StaticArea.lock.release()

                # 配置任务数量信息
                StaticArea.task_number += 1
                StaticArea.task_queue += 1
                # 控制任务队列长度
                if StaticArea.task_queue > 2 * n:
                    while True:
                        Logger.debug('延迟读取文件3秒... 任务队列:', StaticArea.task_queue)
                        for i in range(3):
                            time.sleep(1)
                            # 前端刷新
                            StaticArea.lock.acquire()
                            QApplication.processEvents()
                            StaticArea.lock.release()

                        if StaticArea.task_queue < n:
                            break

    while True:
        if request_times == completed + error_times:
            status_value = '已结束'
            StaticArea.win_msd.w.label_status_value.setText(status_value)
            StaticArea.win_msd.push_end()
            QApplication.processEvents()
            break
        else:
            time.sleep(1)
            status_value = '正在结束...'
            # 前端刷新
            StaticArea.lock.acquire()
            StaticArea.win_msd.w.label_status_value.setText(status_value)
            QApplication.processEvents()
            StaticArea.lock.release()

    time.sleep(3)
    # 结束并恢复初始状态
    status_value = '已结束'
    StaticArea.win_msd.w.label_status_value.setText(status_value)
    QApplication.processEvents()
    StaticArea.reset()


