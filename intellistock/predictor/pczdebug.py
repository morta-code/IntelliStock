__author__ = 'polpe'

from inspect import getframeinfo

def pczdebug(current_frame, *args, **kwargs):
    frameinfo = getframeinfo(current_frame)
    print(frameinfo.filename + ":" + str(frameinfo.lineno))
    print(*args, **kwargs)
