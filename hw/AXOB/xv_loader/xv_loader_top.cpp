#include "xv_loader_top.h"
#include "xv_loader.hpp"

void xv_loader_top(
    /* register-from-host */
    unsigned int reg_frame_nb_i,   // 本次host写入内存的SBE数量，=0时表示初始化
    /* data-from-host */
    ap_uint<DWIDTH> host_frame_i[64], // 本次host写入内存的SBE数据
    /* register-to-host */
    unsigned int &reg_order_nb_o,   // nb of order
    unsigned int &reg_exec_nb_o,    // nb of exec
    unsigned int &reg_snap_nb_o,    // nb of snap
    unsigned int &reg_unknown_nb_o, // nb of unknown frame
    unsigned int &reg_frame_bytes_cnt_o,
    unsigned int &reg_frame_head_o, // begin word of last read frame
    unsigned int &reg_frame_type_o, // message type of last read frame
    unsigned int &reg_frame_tail_o, // end word of last read frame
    /* to OB */
    signal_stream_t      &signal_stream_o,  // Internal Stream: signal
    sbe_stream::stream_t &sbe_stream_o     // Internal Stream: sbe
)
{
/* CTRL */
#pragma HLS INTERFACE ap_ctrl_chain port=return
#pragma HLS INTERFACE s_axilite port=return bundle=control

/* register-from-host */
#pragma HLS INTERFACE s_axilite port=reg_frame_nb_i bundle=control

/* data-from-host */
#pragma HLS INTERFACE s_axilite port=host_frame_i bundle=control
#pragma HLS INTERFACE m_axi port=host_frame_i offset=slave bundle=gmem
// #pragma HLS INTERFACE m_axi port=host_frame_i offset=slave bundle=gmem0 latency=0 num_read_outstanding=4 num_write_outstanding=4 max_read_burst_length=4 max_write_burst_length=1

/* register-to-host */
#pragma HLS interface s_axilite port=reg_order_nb_o bundle=control
#pragma HLS interface s_axilite port=reg_exec_nb_o bundle=control
#pragma HLS interface s_axilite port=reg_snap_nb_o bundle=control
#pragma HLS interface s_axilite port=reg_unknown_nb_o bundle=control
#pragma HLS interface s_axilite port=reg_frame_bytes_cnt_o bundle=control
#pragma HLS interface s_axilite port=reg_frame_head_o bundle=control
#pragma HLS interface s_axilite port=reg_frame_type_o bundle=control
#pragma HLS interface s_axilite port=reg_frame_tail_o bundle=control

/* to OB */
#pragma HLS INTERFACE axis register port=signal_stream_o
#pragma HLS INTERFACE axis register port=sbe_stream_o  depth=512

#define HLS DATAFLOW

xv_loader(
    /* register-from-host */
    reg_frame_nb_i,   // 本次host写入内存的SBE数量，=0时表示初始化
    /* data-from-host */
    host_frame_i, // 本次host写入内存的SBE数据
    /* register-to-host */
    reg_order_nb_o,   // nb of order
    reg_exec_nb_o,    // nb of exec
    reg_snap_nb_o,    // nb of snap
    reg_unknown_nb_o, // nb of unknown frame
    reg_frame_bytes_cnt_o,
    reg_frame_head_o, // begin word of last read frame
    reg_frame_type_o, // message type of last read frame
    reg_frame_tail_o, // end word of last read frame
    /* to OB */
    signal_stream_o,  // Internal Stream: signal
    sbe_stream_o     // Internal Stream: sbe
);
    
}
