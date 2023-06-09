/**************************************
 * 用于在 XILINX VITIS 结构中将SBE消息从HBM/DDR中读取出来，传送给MU/AXOB kernel。
 * TODO: co-sim dead-lock: 通过波形查看是一直在读寄存器0x78/0x88/0x98（Control signal of reg_frame_head_o/reg_frame_type_o/reg_frame_tail_o)
 *       当时这三个接口不是采用【static reg; reg_o=reg;】的模式，而是直接在循环中对reg_o赋值，因此vld信号在函数结束时不为高；修改模式后co-sim不再死锁。
 **************************************/
#ifndef __XV_LOADER_TOP_H__
#define __XV_LOADER_TOP_H__

#include "xv_define.h"
#include "signal_stream.hpp"
#include "sbe_stream.hpp"
extern "C" void xv_loader_top(
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

#endif // __XV_LOADER_TOP_H__
