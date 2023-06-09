#include "xv_storer.hpp"

#include "sbe_intf.hpp"
#include "sbe_ssz_origin.hpp"
#include "dbg_info.hpp"
void xv_storer(
	/* register-from-host */
	/* register-to-host */
	unsigned int&    reg_frame_nb_o,         //nb of host_frame_o
	unsigned int&    reg_signal_nb_o,        //nb of signal_stream_i
	/* memory */
	ap_uint<DWIDTH>    host_frame_o[64],        //
	/* stream */
	signal_stream_t&    signal_stream_i,           //Stream from OB: signal
	sbe_stream::stream_t&    snap_stream_i         //Stream from OB: snapGen
)
{
	/* define register-to-host */
	static unsigned int    _reg_frame_nb_o=0;         //nb of host_frame_o
	static unsigned int    _reg_signal_nb_o=0;        //nb of signal_stream_i
    
    SBE_SSZ_instrument_snap_t_packed snapPack;
    signal_stream_word_t signal;

    _reg_frame_nb_o = 0;   //每次清零，输出的snap总是输出到 host_frame_o[0] 开始。
    _reg_signal_nb_o = 0;
    while(true){
        signal_stream_i.read(signal);
        _reg_signal_nb_o += 1;

        if (signal.user==SIGNAL_CMD)
        {
            if (signal.data==CMD_STREAM_IDLE)
                break;
            //ignore others
        }else{
            // if (signal.data==__MsgType_SSZ_INSTRUMENT_SNAP__) { //only snap
                sbe_stream::read(snap_stream_i, snapPack);
                host_frame_o[_reg_frame_nb_o++].range(DWIDTH - 1, DWIDTH - BITSIZE_SBE_SSZ_instrument_snap_t_packed) = snapPack;
            // }
        }
    }

	/* update register-to-host */
	reg_frame_nb_o = _reg_frame_nb_o;          //nb of host_frame_o
	reg_signal_nb_o = _reg_signal_nb_o;        //nb of signal_stream_i

	return;

}