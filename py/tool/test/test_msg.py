from tool.msg_util import *
import os

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
                 peak order(bid+ask)=56047; peak pxlv(bid+ask)=338
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



@timeit
def TEST_msg_ms_filt(source_log, securityID, read_nb=0, print_nb = 100):
    '''
    打印消息时戳，指定证券代码
    
    '''
    if not os.path.exists(source_log):
        raise f"{source_log} not exists"

    f = open("log/TEST_msg_ms_filt.log", "w")

    securityID = int(securityID)

    pn = 0
    rn = 0
    for msg in axsbe_file(source_log):
        rn += 1
        if read_nb>0:
            if rn >= read_nb:
                break

        if msg.SecurityID != securityID:
            continue
        # print(msg.ms)
        if msg.MsgType==axsbe_base.MsgType_order:
            f.write(f"{rn:6d}\t{securityID:06d}\torder {msg.ms}\t{msg.tick}\n")
        elif msg.MsgType==axsbe_base.MsgType_exe:
            f.write(f"{rn:6d}\t{securityID:06d}\texe   {msg.ms}\t{msg.tick}\n")
        else:
            f.write(f"{rn:6d}\t{securityID:06d}\tsnap  {msg.ms}\t{msg.tick}\n")
        pn += 1
        if pn>=print_nb:
            break

    f.close()
    print("TEST_msg_ms_filt done")
    return


@timeit
def TEST_msg_text(source_log, securityID, read_nb=0, print_nb = 100):
    '''
    打印消息文本，指定证券代码
    
    '''
    if not os.path.exists(source_log):
        raise f"{source_log} not exists"

    f = open("log/TEST_msg_text.log", "w")

    securityID = int(securityID)

    pn = 0
    rn = 0
    for msg in axsbe_file(source_log):
        rn += 1
        if read_nb>0:
            if rn >= read_nb:
                break

        if msg.SecurityID != securityID:
            continue
        # print(msg.ms)
        f.write(f"{rn:6d}\n")
        f.write(str(msg))
        pn += 1
        if pn>=print_nb:
            break

    f.close()
    print("TEST_msg_text done")
    return
