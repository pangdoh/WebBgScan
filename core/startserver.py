from core import Options
from core.utils import Logger
from core.executor import threador


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

    for language in iter(Options.languages):
        # 读取字典
        dict_file = 'dictionaries/%s' % language
        with open(dict_file, encoding='utf-8') as f:
            while True:
                url = f.readline()
                if not url:
                    break
                url = url.strip()
                if url == '':
                    continue
                # 执行网络请求
                threador.exec_tasks(po, url)
        Logger.log('文件读取完毕')
