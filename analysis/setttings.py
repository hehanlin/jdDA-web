# -*- coding: utf-8 -*-

BROKER_URL = 'redis://he@127.0.0.1:6379/3'  # 指定 Broker

CELERY_RESULT_BACKEND = 'redis://he@127.0.0.1:6379/4'  # 指定 Backend

CELERY_CREATE_MISSING_QUEUES = True  # 某个程序中出现的队列，在broker中不存在，则立刻创建它

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC

CELERYD_CONCURRENCY = 2  # 并发worker数

CELERY_ENABLE_UTC = False

CELERYD_FORCE_EXECV = True  # 强制退出

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_IGNORE_RESULT = True  # 忽略任务结果

# CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 1  # 任务结果过期时间

CELERY_IMPORTS = (  # 指定导入的任务模块
    'analysis.tasks.goodDetail',
    # 'analysis.tasks.goodList',
    # 'analysis.tasks.brandGoodList'
)

CELERY_TASK_PUBLISH_RETRY = False  # 重试
