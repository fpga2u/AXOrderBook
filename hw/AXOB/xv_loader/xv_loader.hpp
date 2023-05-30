
#ifndef __XV_LOADER_H__
#define __XV_LOADER_H__

#include "sbe_intf.hpp"
#include "signal_stream.hpp"
#include "sbe_stream.hpp"

void xv_loader(
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
);

#endif // __XV_LOADER_H__
