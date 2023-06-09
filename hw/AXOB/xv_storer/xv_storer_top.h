/**************************************
 * 用于在 XILINX VITIS 结构中读取MU/AXOB kernel输出的SBE消息，并存放到HBM/DDR中。
 **************************************/
#ifndef __XV_STORER_TOP_H__
#define __XV_STORER_TOP_H__

#include "xv_define.h"
#include "signal_stream.hpp"
#include "sbe_stream.hpp"
extern "C" void xv_storer_top(
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

#endif // __XV_STORER_TOP_H__
