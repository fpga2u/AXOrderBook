#include "sbe_intf.hpp"
#include "xv_storer.hpp"


void xv_storer(
    /* from OB */
    signal_stream_t &signal_stream_i,       // Internal Stream: signal
    sbe_stream::stream_t &snap_stream_i,    // Internal Stream: snapGen
    /* data-to-host */
    ap_uint<DWIDTH>  host_frame_o[64],
    /* reg-to-host */
    unsigned int &reg_frame_nb_o,           // nb of host_frame_o
    unsigned int &reg_signal_nb_o           // nb of signal_stream_i
)
{

    static unsigned int reg_frame_nb;
    static unsigned int reg_signal_nb;
    
    SBE_SSZ_instrument_snap_t_packed snapPack;
    signal_stream_word_t signal;

    reg_frame_nb = 0;   //每次清零，输出的snap总是输出到 host_frame_o[0] 开始。
    reg_signal_nb = 0;
    while(true){
        signal_stream_i.read(signal);
        reg_signal_nb += 1;

        if (signal.user==SIGNAL_CMD)
        {
            if (signal.data==CMD_STREAM_IDLE)
                break;
            //ignore others
        }else{
            // if (signal.data==__MsgType_SSZ_INSTRUMENT_SNAP__) { //only snap
                sbe_stream::read(snap_stream_i, snapPack);
                host_frame_o[reg_frame_nb++].range(DWIDTH - 1, DWIDTH - BITSIZE_SBE_SSZ_instrument_snap_t_packed) = snapPack;
            // }
        }
    }

    reg_frame_nb_o = reg_frame_nb;
    reg_signal_nb_o = reg_signal_nb;
}
