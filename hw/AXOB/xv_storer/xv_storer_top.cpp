#include "xv_storer_top.h"
#include "xv_storer.hpp"

void xv_storer_top(
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

/* CTRL */
#pragma HLS INTERFACE ap_ctrl_chain port=return
#pragma HLS INTERFACE s_axilite port=return bundle=control

/* register-from-host */
/* register-to-host */
#pragma HLS INTERFACE s_axilite port=reg_frame_nb_o bundle=control
#pragma HLS INTERFACE s_axilite port=reg_signal_nb_o bundle=control
/* memory */
#pragma HLS INTERFACE s_axilite port=host_frame_o bundle=control
#pragma HLS INTERFACE port=host_frame_o m_axi offset=slave bundle=gmem0 latency=0 num_read_outstanding=1 num_write_outstanding=1 max_read_burst_length=1 max_write_burst_length=1
/* stream */
#pragma HLS INTERFACE axis register port=signal_stream_i
#pragma HLS INTERFACE axis register port=snap_stream_i

#define HLS DATAFLOW

xv_storer(
	/* register-from-host */
	/* register-to-host */
	reg_frame_nb_o,         //nb of host_frame_o
	reg_signal_nb_o,        //nb of signal_stream_i
	/* memory */
	host_frame_o,        //
	/* stream */
	signal_stream_i,        //Stream from OB: signal
	snap_stream_i           //Stream from OB: snapGen
);
}