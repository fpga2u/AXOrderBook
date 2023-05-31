#ifndef __XV_STORER_HPP__
#define __XV_STORER_HPP__

#include "xv_define.h"
#include "signal_stream.hpp"
#include "sbe_stream.hpp"

void xv_storer(
    /* from OB */
    signal_stream_t &signal_stream_i,       // Internal Stream: signal
    sbe_stream::stream_t &snap_stream_i,    // Internal Stream: snapGen
    /* data-to-host */
    ap_uint<DWIDTH>  host_frame_o[64],
    /* reg-to-host */
    unsigned int &reg_frame_nb_o,           // nb of host_frame_o
    unsigned int &reg_signal_nb_o           // nb of signal_stream_i
);

#endif
