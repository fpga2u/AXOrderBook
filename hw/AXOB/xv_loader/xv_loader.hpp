#ifndef __XV_LOADER_HPP__
#define __XV_LOADER_HPP__

#include "xv_define.h"
#include "signal_stream.hpp"
#include "sbe_stream.hpp"
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
);

#endif // __XV_LOADER_HPP__
