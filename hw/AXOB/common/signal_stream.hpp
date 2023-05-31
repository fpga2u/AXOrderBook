#ifndef __SIGNAL_STREAM_HPP__
#define __SIGNAL_STREAM_HPP__

#include "xv_define.h"
#include "ap_axi_sdata.h"
#include "hls_stream.h"


/** 信号流接口，每拍一个指令 **/
#define BITSIZE_SIGNAL_STREAM (8)     //user==0为SBE消息类型、user==1为指令
#define KEEP_SIGNAL_STREAM (1<<(hls::bytewidth<signal_stream_word_t>)-1)
typedef ap_axiu<BITSIZE_SIGNAL_STREAM, 1, 0, 0> signal_stream_word_t; //
typedef hls::stream<signal_stream_word_t> signal_stream_t;

#define SIGNAL_MSGTYPE 0
#define SIGNAL_CMD     1

#define CMD_NULL            0
#define CMD_INIT            1   //初始化整个MU/OB
#define CMD_STREAM_IDLE     2   //SBE流结束

#endif// __SIGNAL_STREAM_HPP__
