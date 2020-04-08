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
