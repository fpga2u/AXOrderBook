
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
            l = l.lstrip()
            if l.find("//") >= 0:
                msg = dict_to_axsbe(str_to_dict(l))
                if msg is not None:
                    yield msg




def TEST_msg_ms():
    TEST_NB = 100

    forder = open("order.log", "w")
    fsnap = open("snap.log", "w")
    fexec = open("exec.log", "w")
    # f = open("ms.log", "w")

    n = 0
    for msg in axsbe_file("data/AX_sbe_szse_000001.log"):
        # print(msg.ms)
        if isinstance(msg, axsbe_order):
            forder.write(f"order\t{n}\t{msg.ms}\t\n")
        elif isinstance(msg, axsbe_exe):
            fexec.write(f"execute\t{n}\t{msg.ms}\t\n")
        else:
            fsnap.write(f"snap\t{n}\t{msg.ms}\t\n")
        n += 1
        if n>=TEST_NB:
            break
        
    # msg_test_list = [
    # "//sequence_in=53139 sequence_out=52137 MsgType=192 SecurityIDSource=102 MDStreamID=11 SecurityID=300175           ChannelNo=2011 ApplSeqNum=88795         Price=91000              OrderQty=30000           Side=49 OrdType=50 TransactTime=20190311091502950 ",
    # "//sequence_in=6676 sequence_out=9692 MsgType=111 SecurityIDSource=102 MDStreamID=10 SecurityID=300175           ChannelNo=1011 ApplSeqNum=0             NumTrades=0              TotalVolumeTrade=0       TotalValueTrade=0        PrevClosePx=82700 LastPx=0     OpenPx=0     HighPx=0     LowPx=0      BidWeightPx=0 BidWeightSize=0          AskWeightPx=0 AskWeightSize=0          UpLimitPx=9100000 DnLimitPx=7440000 BidLevel[0].Price=0 BidLevel[0].Qty=0        BidLevel[1].Price=0 BidLevel[1].Qty=0        BidLevel[2].Price=0 BidLevel[2].Qty=0        BidLevel[3].Price=0 BidLevel[3].Qty=0        BidLevel[4].Price=0 BidLevel[4].Qty=0        BidLevel[5].Price=0 BidLevel[5].Qty=0        BidLevel[6].Price=0 BidLevel[6].Qty=0        BidLevel[7].Price=0 BidLevel[7].Qty=0        BidLevel[8].Price=0 BidLevel[8].Qty=0        BidLevel[9].Price=0 BidLevel[9].Qty=0        AskLevel[0].Price=0 AskLevel[0].Qty=0        AskLevel[1].Price=0 AskLevel[1].Qty=0        AskLevel[2].Price=0 AskLevel[2].Qty=0        AskLevel[3].Price=0 AskLevel[3].Qty=0        AskLevel[4].Price=0 AskLevel[4].Qty=0        AskLevel[5].Price=0 AskLevel[5].Qty=0        AskLevel[6].Price=0 AskLevel[6].Qty=0        AskLevel[7].Price=0 AskLevel[7].Qty=0        AskLevel[8].Price=0 AskLevel[8].Qty=0        AskLevel[9].Price=0 AskLevel[9].Qty=0        TransactTime=20190311091500000 ",
    # "//sequence_in=55999 sequence_out=359 MsgType=191 SecurityIDSource=102 MDStreamID=11 SecurityID=300175           ChannelNo=2011 ApplSeqNum=30745         BidApplSeqNum=26547      OfferApplSeqNum=0        LastPx=0     LastQty=200000           ExecType=52 TransactTime=20190311091500810 ",
    # "//sequence_in=57282 sequence_out=44255 MsgType=191 SecurityIDSource=102 MDStreamID=11 SecurityID=300175           ChannelNo=2011 ApplSeqNum=368192        BidApplSeqNum=4          OfferApplSeqNum=497      LastPx=91000 LastQty=3000000          ExecType=70 TransactTime=20190311092500000 ",
    # "//sequence_in=57282 sequence_out=44256 MsgType=191 SecurityIDSource=102 MDStreamID=11 SecurityID=300175           ChannelNo=2011 ApplSeqNum=368193        BidApplSeqNum=4          OfferApplSeqNum=106892   LastPx=91000 LastQty=30000            ExecType=70 TransactTime=20190311092500000 ",
    # "//sequence_in=57282 sequence_out=44257 MsgType=191 SecurityIDSource=102 MDStreamID=11 SecurityID=300175           ChannelNo=2011 ApplSeqNum=368194        BidApplSeqNum=4          OfferApplSeqNum=177841   LastPx=91000 LastQty=500000           ExecType=70 TransactTime=20190311092500000 ",

    # ]

    # for s in msg_test_list:
    #     msg = dict_to_axsbe(str_to_dict(s))
    #     l_logger.info(msg)

    print("TEST_msg_ms done")
    return

@timeit
def TEST_serial(TEST_NB = 100):
    '''
    测试numpy字节流的打包/解包

    5950x + 860evo:
        sz000001:tested_exe=106434 tested_order=122359 tested_snap=5082; sum=233875; used=5.0s
    '''
    tested_order = 0
    tested_exe = 0
    tested_snap = 0

    SE = axsbe_base.SecurityIDSource_SZSE
    for msg in axsbe_file("data/AX_sbe_szse_000001.log"):
        if isinstance(msg, axsbe_order):
            bytes_np = msg.bytes_np
            unpack_axsbe_order = axsbe_order()
            unpack_axsbe_order.unpack_np(bytes_np)
            if str(msg) != str(unpack_axsbe_order):
                raise RuntimeError("TEST_serial tested_order NG")
            tested_order += 1
        elif isinstance(msg, axsbe_exe):
            bytes_np = msg.bytes_np
            unpack_axsbe_execute = axsbe_exe()
            unpack_axsbe_execute.unpack_np(bytes_np)
            if str(msg) != str(unpack_axsbe_execute):
                raise RuntimeError("TEST_serial tested_exe NG")
            tested_exe += 1
        else:
            bytes_np = msg.bytes_np
            unpack_axsbe_snap = axsbe_snap()
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

    ## test: byte_stream
    print(len(axsbe_order(axsbe_base.SecurityIDSource_SZSE).bytes_stream))
    print(len(axsbe_exe(axsbe_base.SecurityIDSource_SZSE).bytes_stream))
    print(len(axsbe_snap(axsbe_base.SecurityIDSource_SZSE).bytes_stream))

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

    ##    
    TEST_msg_ms()
    ##
    TEST_serial(10000)



