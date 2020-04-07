class Options:
    # 扫描目标
    target = None

    # 打印调试信息
    debug = False

    # 状态码
    status_code = [200, 304, 403]

    # 并发性：1 低、 2 中、 3 高
    concurrency = 2

    # 指定开发语言
    languages = ['php', 'asp', 'aspx', 'jsp']

    # 设置延迟，单位秒
    delay = None

    # 显示扫描过程
    detail = False
