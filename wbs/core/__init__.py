class Options:
    # 扫描目标
    target = None

    # 打印调试信息
    debug = False

    # 状态码
    status_code = ['200', '3XX', '403']

    # 并发性：0 低、 1 中、 2 高
    concurrency = 1

    # 指定开发语言
    languages = ['php', 'asp', 'aspx', 'jsp']

    # 设置延迟，单位秒
    delay = None

    # 显示扫描过程
    detail = False

    # 设置请求头
    headers = None


class StaticArea:
    win_msd = None
    lock = None
    request_times = 0
    task_number = 0
    task_queue = 0
    completed = 0
    error_times = 0
    conn_error_rate = 0

    @staticmethod
    def reset():
        StaticArea.lock = None
        StaticArea.request_times = 0
        StaticArea.task_number = 0
        StaticArea.task_queue = 0
        StaticArea.completed = 0
        StaticArea.error_times = 0
        StaticArea.conn_error_rate = 0
