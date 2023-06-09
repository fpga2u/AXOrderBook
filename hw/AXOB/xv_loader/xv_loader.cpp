#include "xv_loader.hpp"

#include "sbe_intf.hpp"
#include "sbe_ssz_origin.hpp"
#include "dbg_info.hpp"
void xv_loader(
	/* register-from-host */
	unsigned int    reg_frame_nb_i,        //本次host写入内存的SBE数量，=0时表示初始化
	/* register-to-host */
	unsigned int&    reg_order_nb_o,               //nb of order
	unsigned int&    reg_exec_nb_o,                //nb of exec
	unsigned int&    reg_snap_nb_o,                //nb of snap
	unsigned int&    reg_unknown_nb_o,             //nb of unknown frame
	unsigned int&    reg_frame_bytes_cnt_o,        //nb of bytes of all sbe frames
	unsigned int&    reg_frame_head_o,             //begin word of last read frame
	unsigned int&    reg_frame_type_o,             //message type of last read frame
	unsigned int&    reg_frame_tail_o,             //end word of last read frame
	/* memory */
	ap_uint<DWIDTH>    host_frame_i[64],        //本次host写入内存的SBE数据，不指定大小则cosim会失败(host_frame_i[1]是全0)
	/* stream */
	signal_stream_t&    signal_stream_o,          //Stream to OB: signal
	sbe_stream::stream_t&    sbe_stream_o         //Stream to OB: snapGen
)
{
	/* define register-to-host */
	static unsigned int    _reg_order_nb_o=0;               //nb of order
	static unsigned int    _reg_exec_nb_o=0;                //nb of exec
	static unsigned int    _reg_snap_nb_o=0;                //nb of snap
	static unsigned int    _reg_unknown_nb_o=0;             //nb of unknown frame
	static unsigned int    _reg_frame_bytes_cnt_o=0;        //nb of bytes of all sbe frames
	static unsigned int    _reg_frame_head_o=0;             //begin word of last read frame
	static unsigned int    _reg_frame_type_o=0;             //message type of last read frame
	static unsigned int    _reg_frame_tail_o=0;             //end word of last read frame

    signal_stream_word_t signal;
    ap_uint<8> MsgType;
    SBE_SSZ_ord_t_packed OrderPack;
    SBE_SSZ_exe_t_packed ExecPack;
    SBE_SSZ_instrument_snap_t_packed SnapPack;

    INFO("loader start, reg_frame_nb_i="<<reg_frame_nb_i);

data_mover:
    for (unsigned int i = 0; i<reg_frame_nb_i; ++i)
    {
        ap_uint<DWIDTH> frame = host_frame_i[i];
        MsgType = frame.range(DWIDTH - 8 - 1, DWIDTH - 8 - 8);
        _reg_frame_head_o = frame.range(DWIDTH - 1, DWIDTH - 32);
        _reg_frame_tail_o = frame.range(31, 0);
        _reg_frame_type_o = MsgType;

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
            _reg_order_nb_o++;
            _reg_frame_bytes_cnt_o += (BITSIZE_SBE_SSZ_ord_t_packed >>3);
            break;
        case __MsgType_SSZ_EXECUTION__:
            ExecPack = frame.range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_exe_t_packed);
            sbe_stream::write(ExecPack, sbe_stream_o);
            _reg_exec_nb_o++;
            _reg_frame_bytes_cnt_o += (BITSIZE_SBE_SSZ_exe_t_packed >>3);
            break;
        case __MsgType_SSZ_INSTRUMENT_SNAP__:
            SnapPack = frame.range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_instrument_snap_t_packed);
            sbe_stream::write(SnapPack, sbe_stream_o);
            _reg_snap_nb_o++;
            _reg_frame_bytes_cnt_o += (BITSIZE_SBE_SSZ_instrument_snap_t_packed >>3);
            break;
        default:
            _reg_unknown_nb_o++;
            break;
        }
    }

    //初始化
    if (reg_frame_nb_i==0){
        signal.user = SIGNAL_CMD;
        signal.data = CMD_INIT;
        signal_stream_o.write(signal);
    }
    signal.user = SIGNAL_CMD;
    signal.data = CMD_STREAM_IDLE;
    signal_stream_o.write(signal);

	/* update register-to-host */
	reg_order_nb_o = _reg_order_nb_o;                      //nb of order
	reg_exec_nb_o = _reg_exec_nb_o;                        //nb of exec
	reg_snap_nb_o = _reg_snap_nb_o;                        //nb of snap
	reg_unknown_nb_o = _reg_unknown_nb_o;                  //nb of unknown frame
	reg_frame_bytes_cnt_o = _reg_frame_bytes_cnt_o;        //nb of bytes of all sbe frames
	reg_frame_head_o = _reg_frame_head_o;                  //begin word of last read frame
	reg_frame_type_o = _reg_frame_type_o;                  //message type of last read frame
	reg_frame_tail_o = _reg_frame_tail_o;                  //end word of last read frame

	return;

}