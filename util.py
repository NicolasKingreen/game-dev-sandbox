import math


def lerp(v0, v1, t):
    return v0 + t * (v1 - v0)

def lerp_(v0, v1, t):
    return v0 * (1 - t) + v1 * t

def f(t):
    v0 = t
    v1 = 1.0 - (1.0 - t)
    return lerp_(v0, v1, t)


def memory_usage():
    """
    Return memory usage in MB
    :return:
    """
    import os
    import psutil
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def cpu_usage():
    """
    Return CPU usage in %
    :return:
    """
    import psutil
    import os
    process = psutil.Process(os.getpid())
    return process.cpu_percent()


if __name__ == '__main__':
    print(lerp(0, 100, 0.0))
    print(lerp(0, 100, 1.0))
    print(lerp(100, 200, 0.5))
    print(lerp(100, 200, 0.75))
