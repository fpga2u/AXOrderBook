# -*- coding: utf-8 -*-

from time import time
import psutil
import os

from functools import wraps
def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('%2.4f sec used by func:%r args:[%r, %r]' % \
          (te-ts, f.__name__, args, kw))
        return result
    return wrap

#内存占用，GB
def getMemUsageGB():
    return psutil.Process(os.getpid()).memory_info().rss/(1024**3)

#系统空闲内存，GB
def getMemFreeGB():
    return psutil.virtual_memory().free / (1024**3)
