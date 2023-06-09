#ifndef __XV_STORER_HPP__
#define __XV_STORER_HPP__

#include "xv_define.h"
#include "signal_stream.hpp"
#include "sbe_stream.hpp"
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
);

#endif // __XV_STORER_HPP__
