#include "xv_storer_top.h"
#include "xv_storer.hpp"

void xv_storer_top(
    /* from OB */
    signal_stream_t &signal_stream_i, // Internal Stream: signal
    sbe_stream::stream_t &snap_stream_i, // Internal Stream: snapGen
    /* data-to-host */
    ap_uint<DWIDTH>  host_frame_o[64],
    /* reg-to-host */
    unsigned int &reg_frame_nb_o, // nb of host_frame_o
    unsigned int &reg_signal_nb_o // nb of signal_stream_i
)
{

/* CTRL */
#pragma HLS INTERFACE ap_ctrl_chain port=return
#pragma HLS INTERFACE s_axilite port=return bundle=control
/* from OB */
#pragma HLS INTERFACE axis register port=signal_stream_i
#pragma HLS INTERFACE axis register port=snap_stream_i
/* data-to-host */
#pragma HLS INTERFACE s_axilite port=host_frame_o bundle=control
// #pragma HLS INTERFACE m_axi port=host_frame_o offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi port=host_frame_o offset=slave bundle=gmem0 latency=0 num_read_outstanding=1 num_write_outstanding=1 max_read_burst_length=1 max_write_burst_length=1
/* reg-to-host */
#pragma HLS interface s_axilite port=reg_frame_nb_o bundle=control
#pragma HLS interface s_axilite port=reg_signal_nb_o bundle=control

#define HLS DATAFLOW

xv_storer(
    /* from OB */
    signal_stream_i, // Internal Stream: signal
    snap_stream_i, // Internal Stream: snapGen
    /* data-to-host */
    host_frame_o,
    /* reg-to-host */
    reg_frame_nb_o, // nb of host_frame_o
    reg_signal_nb_o // nb of signal_stream_i
);



}
