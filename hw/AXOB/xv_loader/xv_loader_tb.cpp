#include "dbg_info.hpp"
#include "dbg_util.hpp"
#include "xv_loader_top.h"

#include "sbe_intf.hpp"
#include "sbe_ssz_origin.hpp"
#include "dbg_info.hpp"
int main()
{

	/* register-from-host */
	unsigned int    reg_frame_nb_i;        //本次host写入内存的SBE数量，=0时表示初始化
	/* register-to-host */
	unsigned int    reg_order_nb_o;               //nb of order
	unsigned int    reg_exec_nb_o;                //nb of exec
	unsigned int    reg_snap_nb_o;                //nb of snap
	unsigned int    reg_unknown_nb_o;             //nb of unknown frame
	unsigned int    reg_frame_bytes_cnt_o;        //nb of bytes of all sbe frames
	unsigned int    reg_frame_head_o;             //begin word of last read frame
	unsigned int    reg_frame_type_o;             //message type of last read frame
	unsigned int    reg_frame_tail_o;             //end word of last read frame
	/* memory */
	ap_uint<DWIDTH>    host_frame_i[64];        //本次host写入内存的SBE数据，不指定大小则cosim会失败(host_frame_i[1]是全0)
	/* stream */
	signal_stream_t    signal_stream_o;          //Stream to OB: signal
	sbe_stream::stream_t    sbe_stream_o;        //Stream to OB: snapGen

    signal_stream_word_t signal;
    ap_uint<8> MsgType;
    SBE_SSZ_ord_t_packed orderPack;
    SBE_SSZ_exe_t_packed execPack;
    SBE_SSZ_instrument_snap_t_packed snapPack;

    printf("capacity=%lu\n", sbe_stream_o.capacity());
    reg_frame_nb_i = 0;

xv_loader_top(
	/* register-from-host */
	reg_frame_nb_i,        //本次host写入内存的SBE数量，=0时表示初始化
	/* register-to-host */
	reg_order_nb_o,               //nb of order
	reg_exec_nb_o,                //nb of exec
	reg_snap_nb_o,                //nb of snap
	reg_unknown_nb_o,             //nb of unknown frame
	reg_frame_bytes_cnt_o,        //nb of bytes of all sbe frames
	reg_frame_head_o,             //begin word of last read frame
	reg_frame_type_o,             //message type of last read frame
	reg_frame_tail_o,             //end word of last read frame
	/* memory */
	host_frame_i,        //本次host写入内存的SBE数据，不指定大小则cosim会失败(host_frame_i[1]是全0)
	/* stream */
	signal_stream_o,        //Stream to OB: signal
	sbe_stream_o            //Stream to OB: snapGen
);

    signal_stream_o.read(signal);
    assert(signal.data==CMD_INIT && signal.user==SIGNAL_CMD);
    signal_stream_o.read(signal);
    assert(signal.data==CMD_STREAM_IDLE && signal.user==SIGNAL_CMD);

    //create order
    SBE_SSZ_ord_t order;
    order.Header.SecurityIDSource = __SecurityIDSource_SSZ_;
    order.Header.MsgType = __MsgType_SSZ_ORDER__;
    order.Header.MsgLen = BITSIZE_SBE_SSZ_ord_t_packed / 8;
    setSecurityID(order.Header.SecurityID, "603383");
    order.Header.ChannelNo = 2013;
    order.Header.ApplSeqNum = 1555;
    order.Header.TradingPhase.Code0 = 0;
    order.Header.TradingPhase.Code1 = 0;
    order.Price = 195000;
    order.OrderQty = 50000;
    order.Side = 50;
    order.OrdType = 50;
    order.TransactTime = 20190311091500040;
    order.Resv[0] = 0;
    order.Resv[1] = 0;

    //create exec
    SBE_SSZ_exe_t exec;
    exec.Header.SecurityIDSource = __SecurityIDSource_SSZ_;
    exec.Header.MsgType = __MsgType_SSZ_EXECUTION__;
    exec.Header.MsgLen = BITSIZE_SBE_SSZ_exe_t_packed / 8;
    setSecurityID(exec.Header.SecurityID, "000997");
    exec.Header.ChannelNo = 2;
    exec.Header.ApplSeqNum = 22222;
    exec.Header.TradingPhase.Code0 = 0;
    exec.Header.TradingPhase.Code1 = 0;
    exec.BidApplSeqNum = 0;
    exec.OfferApplSeqNum = 1555;
    exec.LastPx = 18001;
    exec.LastQty = 600;
    exec.ExecType = '4';
    exec.TransactTime = 2021061609300001;
    exec.Resv[0] = 0;
    exec.Resv[1] = 0;
    exec.Resv[2] = 0;

    //create snap
    SBE_SSZ_instrument_snap_t snap;
    snap.Header.SecurityIDSource = __SecurityIDSource_SSZ_;
    snap.Header.MsgType = __MsgType_SSZ_INSTRUMENT_SNAP__;
    snap.Header.MsgLen = BITSIZE_SBE_SSZ_instrument_snap_t_packed / 8;
    setSecurityID(snap.Header.SecurityID, "000997");
    snap.Header.ChannelNo = 1013;
    snap.Header.ApplSeqNum = 0;
    snap.Header.TradingPhase.Code0 = 2;
    snap.Header.TradingPhase.Code1 = 0;

    snap.NumTrades = 0;
    snap.TotalVolumeTrade = 0;
    snap.TotalValueTrade = 0;
    snap.PrevClosePx = 184000;
    snap.LastPx = 0;
    snap.OpenPx = 0;
    snap.HighPx = 0;
    snap.LowPx = 0;
    snap.BidWeightPx = 0;
    snap.BidWeightSize = 0;
    snap.AskWeightPx = 0;
    snap.AskWeightSize = 0;
    snap.UpLimitPx = 20240000;
    snap.DnLimitPx = 16560000;

    snap.BidLevel[0].Price = 0;
    snap.BidLevel[0].Qty = 0;

    snap.BidLevel[1].Price = 0;
    snap.BidLevel[1].Qty = 0;

    snap.BidLevel[2].Price = 0;
    snap.BidLevel[2].Qty = 0;

    snap.BidLevel[3].Price = 0;
    snap.BidLevel[3].Qty = 0;

    snap.BidLevel[4].Price = 0;
    snap.BidLevel[4].Qty = 0;

    snap.BidLevel[5].Price = 0;
    snap.BidLevel[5].Qty = 0;

    snap.BidLevel[6].Price = 0;
    snap.BidLevel[6].Qty = 0;

    snap.BidLevel[7].Price = 0;
    snap.BidLevel[7].Qty = 0;

    snap.BidLevel[8].Price = 0;
    snap.BidLevel[8].Qty = 0;

    snap.BidLevel[9].Price = 0;
    snap.BidLevel[9].Qty = 0;

    snap.AskLevel[0].Price = 0;
    snap.AskLevel[0].Qty = 0;

    snap.AskLevel[1].Price = 0;
    snap.AskLevel[1].Qty = 0;

    snap.AskLevel[2].Price = 0;
    snap.AskLevel[2].Qty = 0;

    snap.AskLevel[3].Price = 0;
    snap.AskLevel[3].Qty = 0;

    snap.AskLevel[4].Price = 0;
    snap.AskLevel[4].Qty = 0;

    snap.AskLevel[5].Price = 0;
    snap.AskLevel[5].Qty = 0;

    snap.AskLevel[6].Price = 0;
    snap.AskLevel[6].Qty = 0;

    snap.AskLevel[7].Price = 0;
    snap.AskLevel[7].Qty = 0;

    snap.AskLevel[8].Price = 0;
    snap.AskLevel[8].Qty = 0;

    snap.AskLevel[9].Price = 0;
    snap.AskLevel[9].Qty = 0;

    snap.TransactTime = 20190311083500000;
    snap.Resv[0] = 0;
    snap.Resv[1] = 0;
    snap.Resv[2] = 0;
    snap.Resv[3] = 0;

    // printf("-- input:\n");
    // printSnap("top input", "market", snap);

    unsigned int last_reg_order_nb_o=0; // nb of order
    unsigned int last_reg_exec_nb_o=0;  // nb of exec
    unsigned int last_reg_snap_nb_o=0;  // nb of snap
    for (int n=0;n<3; ++n){ //test multi securityID
        printf("------ %d ------\n", n);
        if (n>0){
            setSecurityID(order.Header.SecurityID, std::to_string(n).c_str()); //change securityID
            setSecurityID(exec.Header.SecurityID, std::to_string(n).c_str());
            setSecurityID(snap.Header.SecurityID, std::to_string(n).c_str());
            order.Price = 100000 + n*1000;
            snap.DnLimitPx = 9000000 + n*100000;
            snap.UpLimitPx = 11000000 + n*100000;
        }

        sbe_intf::SBE_SSZ_ord_t_pack(order, orderPack);
        sbe_intf::SBE_SSZ_exe_t_pack(exec, execPack);
        sbe_intf::SBE_SSZ_instrument_snap_t_pack(snap, snapPack);

        reg_frame_nb_i = 0;
        host_frame_i[0].range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_instrument_snap_t_packed) = snapPack;
        reg_frame_nb_i++;
        host_frame_i[1].range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_ord_t_packed) = orderPack;
        reg_frame_nb_i++;
        host_frame_i[2].range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_exe_t_packed) = execPack;
        reg_frame_nb_i++;

        xv_loader_top(
            /* register-from-host */
            reg_frame_nb_i,	//本次host写入内存的SBE数量，=0时表示初始化
            /* register-to-host */
            reg_order_nb_o,	//nb of order
            reg_exec_nb_o,	//nb of exec
            reg_snap_nb_o,	//nb of snap
            reg_unknown_nb_o,	//nb of unknown frame
            reg_frame_bytes_cnt_o,	//nb of bytes of all sbe frames
            reg_frame_head_o,	//begin word of last read frame
            reg_frame_type_o,	//message type of last read frame
            reg_frame_tail_o,	//end word of last read frame
            /* memory */
            host_frame_i,	//本次host写入内存的SBE数据，不指定大小则cosim会失败(host_frame_i[1]是全0)
            /* stream */
            signal_stream_o,	//Stream to OB: signal
            sbe_stream_o 	//Stream to OB: snapGen
        );

        printf("#reg_order_nb_o=%d reg_exec_nb_o=%d reg_snap_nb_o=%d sbe_stream_o.size=%lu\n", reg_order_nb_o, reg_exec_nb_o, reg_snap_nb_o, sbe_stream_o.size());
        assert(reg_order_nb_o==last_reg_order_nb_o+1 && reg_exec_nb_o==last_reg_exec_nb_o+1 && reg_snap_nb_o==last_reg_snap_nb_o+1);
        assert(reg_unknown_nb_o==0);
        for (int i=0; i<reg_order_nb_o+reg_exec_nb_o+reg_snap_nb_o -last_reg_order_nb_o-last_reg_exec_nb_o-last_reg_snap_nb_o; ++i){
            signal_stream_o.read(signal);
            printf("#%d usr=%d data=%d\n", i, signal.user, signal.data);
            switch (i)
            {
            case 0: assert(signal.data==__MsgType_SSZ_INSTRUMENT_SNAP__ && signal.user==SIGNAL_MSGTYPE); break;
            case 1: assert(signal.data==__MsgType_SSZ_ORDER__ && signal.user==SIGNAL_MSGTYPE); break;
            case 2: assert(signal.data==__MsgType_SSZ_EXECUTION__ && signal.user==SIGNAL_MSGTYPE); break;
            default:
                break;
            }

            SBE_SSZ_ord_t_packed orderPack2ob;
            SBE_SSZ_exe_t_packed execPack2ob;
            SBE_SSZ_instrument_snap_t_packed snapPack2ob;
            
            SBE_SSZ_ord_t order2ob;
            SBE_SSZ_exe_t exec2ob;
            SBE_SSZ_instrument_snap_t snap2ob;

            if (signal.user==SIGNAL_MSGTYPE) {
                switch (signal.data)
                {
                case __MsgType_SSZ_INSTRUMENT_SNAP__:
                    sbe_stream::read(sbe_stream_o, snapPack2ob);
                    sbe_intf::SBE_SSZ_instrument_snap_t_unpack(snapPack2ob, snap2ob);
                    assert(snap==snap2ob);
                    break;
                case __MsgType_SSZ_ORDER__:
                    sbe_stream::read(sbe_stream_o, orderPack2ob);
                    sbe_intf::SBE_SSZ_ord_t_unpack(orderPack2ob, order2ob);
                    assert(order==order2ob);
                    break;
                case __MsgType_SSZ_EXECUTION__:
                    sbe_stream::read(sbe_stream_o, execPack2ob);
                    sbe_intf::SBE_SSZ_exe_t_unpack(execPack2ob, exec2ob);
                    assert(exec==exec2ob);
                    break;
                
                default:
                    assert(false);
                    break;
                }
            }
        }
        signal_stream_o.read(signal);
        assert(signal.data==CMD_STREAM_IDLE && signal.user==SIGNAL_CMD);

        last_reg_order_nb_o = reg_order_nb_o;
        last_reg_exec_nb_o = reg_exec_nb_o;
        last_reg_snap_nb_o = reg_snap_nb_o;

    }

    std::cout << "load: host_order_nb = " << reg_order_nb_o << std::endl;
    std::cout << "load: host_exec nb= " << reg_exec_nb_o << std::endl;
    std::cout << "load: host_snap nb= " << reg_snap_nb_o << std::endl;
    std::cout << "load: reg_unknown_nb_o = " << reg_unknown_nb_o << std::endl;
    std::cout << "load: reg_frame_bytes_cnt_o = " << reg_frame_bytes_cnt_o << std::endl;
    std::cout << "load: reg_frame_head_o = " << reg_frame_head_o << std::endl;
    std::cout << "load: reg_frame_type_o = " << reg_frame_type_o << std::endl;
    std::cout << "load: reg_frame_tail_o = " << reg_frame_tail_o << std::endl;
    return 0;
}
