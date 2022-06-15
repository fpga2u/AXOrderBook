
from cv2 import split
import axsbe_base
from axsbe_exe import axsbe_exe
from axsbe_order import axsbe_order
from axsbe_snap import axsbe_snap

from functools import wraps
from time import time

def timeit(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

def str_to_dict(s:str):
    if s[:2] != "//":
        return None
    s = s[2:].split()
    s = [x.split("=") for x in s if x[-1]!='=']
    md = dict((x[0], int(x[1])) for x in s)
    return md


def dict_to_axsbe(s:dict):
    if s['MsgType']==axsbe_base.MsgType_order:   #order
        order = axsbe_order()
        order.load_dict(s)
        return order
    elif s['MsgType']==axsbe_base.MsgType_exe:   #execute
        execute = axsbe_exe()
        execute.load_dict(s)
        return execute
    elif s['MsgType']==axsbe_base.MsgType_snap:   #snap
        snap = axsbe_snap()
        snap.load_dict(s)
        return snap
    else:
        return None


def axsbe_file(fileName):
    with open(fileName, "r") as f:
        while True:
            l = f.readline()
            if not l:
                break
            if l.find("//") >= 0:
                msg = dict_to_axsbe(str_to_dict(l.lstrip()))
                if msg is not None:
                    yield msg


def TEST_msg_byte_stream():
    ## test: byte_stream
    print(len(axsbe_order(axsbe_base.SecurityIDSource_SZSE).bytes_stream))
    print(len(axsbe_exe(axsbe_base.SecurityIDSource_SZSE).bytes_stream))
    print(len(axsbe_snap(axsbe_base.SecurityIDSource_SZSE).bytes_stream))

def TEST_msg_SL():
    ## test: save/load
    data = axsbe_order(axsbe_base.SecurityIDSource_SZSE).save()
    print(data)
    data['OrdType'] = ord('U')
    data['Side'] = ord('F')
    order = axsbe_order()
    order.load(data)
    print(order)

    data = axsbe_exe(axsbe_base.SecurityIDSource_SZSE).save()
    print(data)
    data['ExecType'] = ord('F')
    exe = axsbe_exe()
    exe.load(data)
    print(exe)

    data = axsbe_snap(axsbe_base.SecurityIDSource_SZSE).save()
    print(data)
    snap = axsbe_snap()
    data['ask'][0]['Price'] = 22200
    data['ask'][0]['Qty'] = 10000
    data['bid'][1]['Price'] = 111
    data['bid'][1]['Qty'] = 20000
    snap.load(data)
    print(snap)

def TEST_msg_ms(TEST_NB = 100):
    '''
    打印消息时戳
    
    用TEST_NB>35000可以看到快照数据的时戳在 09:41:21 之前的都比逐笔的时戳早，说明逐笔行情的传输被阻塞了
    '''
    f = open("log/ms.log", "w")

    n = 0
    for msg in axsbe_file("data/AX_sbe_szse_000001.log"):
        # print(msg.ms)
        if msg.MsgType==axsbe_base.MsgType_order:
            f.write(f"{n:6d}\torder {msg.ms}\t{msg.tick}\n")
        elif msg.MsgType==axsbe_base.MsgType_exe:
            f.write(f"{n:6d}\texe   {msg.ms}\t{msg.tick}\n")
        else:
            f.write(f"{n:6d}\tsnap  {msg.ms}\t{msg.tick}\n")
        n += 1
        if n>=TEST_NB:
            break

    f.close()
    print("TEST_msg_ms done")
    return

@timeit
def TEST_serial(TEST_NB = 100):
    '''
    测试numpy字节流的打包/解包

    5950x + 860evo:
        sz000001:tested_exe=106434 tested_order=122359 tested_snap=5082; sum=233875; used~4.6s
    '''
    tested_order = 0
    tested_exe = 0
    tested_snap = 0

    unpack_axsbe_order = axsbe_order()
    unpack_axsbe_execute = axsbe_exe()
    unpack_axsbe_snap = axsbe_snap()

    for msg in axsbe_file("data/AX_sbe_szse_000001.log"):
        if msg.MsgType==axsbe_base.MsgType_order:
            bytes_np = msg.bytes_np
            unpack_axsbe_order.unpack_np(bytes_np)
            if str(msg) != str(unpack_axsbe_order):
                raise RuntimeError("TEST_serial tested_order NG")
            tested_order += 1
        elif msg.MsgType==axsbe_base.MsgType_exe:
            bytes_np = msg.bytes_np
            unpack_axsbe_execute.unpack_np(bytes_np)
            if str(msg) != str(unpack_axsbe_execute):
                raise RuntimeError("TEST_serial tested_exe NG")
            tested_exe += 1
        else:
            bytes_np = msg.bytes_np
            unpack_axsbe_snap.unpack_np(bytes_np)
            if str(msg) != str(unpack_axsbe_snap):
                raise RuntimeError("TEST_serial tested_snap NG")
            tested_snap += 1

        if tested_exe>=TEST_NB and tested_order>=TEST_NB and tested_snap>=TEST_NB:
            break
    print(f"TEST_serial done"
          f" tested_exe={tested_exe} tested_order={tested_order} tested_snap={tested_snap};"
          f" sum={tested_exe+tested_order+tested_snap}")
    return

if __name__== '__main__':
    '''
    import os
    from log_tools import g_logger, makeLocalLogger
    l_logger = makeLocalLogger(os.path.basename(__file__))  # local logger with file name
    '''

    TEST_msg_byte_stream()
    TEST_msg_SL()

    ##    
    TEST_msg_ms()

    ##
    TEST_serial(10000)



