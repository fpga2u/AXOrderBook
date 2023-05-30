#include "xv_loader.hpp"

#include "sbe_intf.hpp"
#include "signal_stream.hpp"
#include "sbe_stream.hpp"
#include "sbe_ssz_origin.hpp"
#include "dbg_info.hpp"

void xv_loader(
    /* register-from-host */
    unsigned int reg_frame_nb_i,   // 本次host写入内存的SBE数量，=0时表示初始化
    /* data-from-host */
    ap_uint<DWIDTH> host_frame_i[64], // 本次host写入内存的SBE数据
    /* register-to-host */
    unsigned int &reg_order_nb_o,   // nb of order
    unsigned int &reg_exec_nb_o,    // nb of exec
    unsigned int &reg_snap_nb_o,    // nb of snap
    unsigned int &reg_unknown_nb_o, // nb of unknown frame
    unsigned int &reg_frame_bytes_cnt_o,
    unsigned int &reg_frame_head_o, // begin word of last read frame
    unsigned int &reg_frame_type_o, // message type of last read frame
    unsigned int &reg_frame_tail_o, // end word of last read frame
    /* to OB */
    signal_stream_t      &signal_stream_o,  // Internal Stream: signal
    sbe_stream::stream_t &sbe_stream_o     // Internal Stream: sbe
)
{

    signal_stream_word_t signal;
    ap_uint<8> MsgType;
    SBE_SSZ_ord_t_packed OrderPack;
    SBE_SSZ_exe_t_packed ExecPack;
    SBE_SSZ_instrument_snap_t_packed SnapPack;

    static unsigned int reg_frame_bytes_cnt = 0;
    static unsigned int reg_order_nb = 0;
    static unsigned int reg_exec_nb = 0;
    static unsigned int reg_snap_nb = 0;
    static unsigned int reg_unknown_nb = 0;
    static unsigned int reg_frame_head = 0;
    static unsigned int reg_frame_tail = 0;
    static unsigned int reg_frame_type = 0;

    INFO("loader start, reg_frame_nb_i="<<reg_frame_nb_i);

data_mover:
    for (unsigned int i = 0; i < reg_frame_nb_i; ++i)
    {
        ap_uint<DWIDTH> frame = host_frame_i[i];
        MsgType = frame.range(DWIDTH - 8 - 1, DWIDTH - 8 - 8);
        reg_frame_head = frame.range(DWIDTH - 1, DWIDTH - 32);
        reg_frame_tail = frame.range(31, 0);
        reg_frame_type = MsgType;

        INFO("loader move #" << i << ", MsgType="<<MsgType);

        //发送信号
        switch (MsgType)
        {
        case __MsgType_SSZ_ORDER__:
        case __MsgType_SSZ_EXECUTION__:
        case __MsgType_SSZ_INSTRUMENT_SNAP__:
            signal.user = SIGNAL_MSGTYPE;
            signal.data = MsgType;
            signal_stream_o.write(signal);
            break;
        default:
            signal.user = SIGNAL_CMD;
            signal.data = CMD_NULL;
            signal_stream_o.write(signal);
            break;
        }

        //发送SBE
        switch (MsgType)
        {
        case __MsgType_SSZ_ORDER__:
            OrderPack = frame.range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_ord_t_packed);
            sbe_stream::write(OrderPack, sbe_stream_o);
            reg_order_nb++;
            reg_frame_bytes_cnt += (BITSIZE_SBE_SSZ_ord_t_packed >>3);
            break;
        case __MsgType_SSZ_EXECUTION__:
            ExecPack = frame.range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_exe_t_packed);
            sbe_stream::write(ExecPack, sbe_stream_o);
            reg_exec_nb++;
            reg_frame_bytes_cnt += (BITSIZE_SBE_SSZ_exe_t_packed >>3);
            break;
        case __MsgType_SSZ_INSTRUMENT_SNAP__:
            SnapPack = frame.range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_instrument_snap_t_packed);
            sbe_stream::write(SnapPack, sbe_stream_o);
            reg_snap_nb++;
            reg_frame_bytes_cnt += (BITSIZE_SBE_SSZ_instrument_snap_t_packed >>3);
            break;
        default:
            reg_unknown_nb++;
            break;
        }
    }

    //初始化
    if (reg_frame_nb_i == 0){
        signal.user = SIGNAL_CMD;
        signal.data = CMD_INIT;
        signal_stream_o.write(signal);
    }
    signal.user = SIGNAL_CMD;
    signal.data = CMD_STREAM_IDLE;
    signal_stream_o.write(signal);

    //update registers
    reg_order_nb_o = reg_order_nb;
    reg_exec_nb_o = reg_exec_nb;
    reg_snap_nb_o = reg_snap_nb;
    reg_unknown_nb_o = reg_unknown_nb;
    reg_frame_bytes_cnt_o = reg_frame_bytes_cnt;
    reg_frame_head_o = reg_frame_head;
    reg_frame_tail_o = reg_frame_tail;
    reg_frame_type_o = reg_frame_type;
}

