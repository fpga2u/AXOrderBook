#ifndef __SBE_STREAM_HPP__
#define __SBE_STREAM_HPP__

#include "xv_define.h"
#include "ap_axi_sdata.h"
#include "hls_stream.h"


/** MU或AXOB收发消息流接口 **/
class sbe_stream
{
public:
#define BITSIZE_SBE_STREAM (32)
#define KEEP_SBE_STREAM (1<<(hls::bytewidth<sbe_stream_word_t>)-1)

    typedef ap_axiu<BITSIZE_SBE_STREAM, 0, 0, 0> word_t; //
    typedef hls::stream<word_t> stream_t;

    template<int D>
    static void write(ap_uint<D> &packed_data,
                      stream_t &stream)
    {
#pragma HLS INLINE
        word_t word;

        for (int io_cnt = 0; io_cnt < D / BITSIZE_SBE_STREAM; ++io_cnt)
        {
#pragma HLS unroll
            word.data = packed_data.range(D - 1 - io_cnt * BITSIZE_SBE_STREAM, D - (io_cnt + 1) * BITSIZE_SBE_STREAM);
            // word.keep = KEEP_SBE_STREAM;
            // word.last = io_cnt == (D / BITSIZE_SBE_STREAM - 1);
            stream.write(word);
        }

    }

    
    template<int D>
    static void read(stream_t &stream,
                     ap_uint<D> &packed_data)
    {
#pragma HLS INLINE
        word_t word;

        for (int io_cnt = 0; io_cnt < D / BITSIZE_SBE_STREAM; ++io_cnt)
        {
#pragma HLS unroll
            stream.read(word);
            packed_data.range(D - 1 - io_cnt * BITSIZE_SBE_STREAM, D - (io_cnt + 1) * BITSIZE_SBE_STREAM) = word.data;
        }
    }

};



#endif// __SBE_STREAM_HPP__
