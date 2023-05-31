#ifndef __ENDIAN_HPP__
#define __ENDIAN_HPP__

#include "xv_define.h"
#include "ap_axi_sdata.h"

namespace SBE_ENDIAN {

template <int D>
ap_uint<D> reverse(const ap_uint<D>& w) {
#pragma HLS INLINE
    ap_uint<D> temp;
    for (int i = 0; i < D / 8; i++) {
#pragma HLS UNROLL
        temp(i * 8 + 7, i * 8) = w(D - (i * 8) - 1, D - (i * 8) - 8);
    }
    return temp;
}

}//SBE_ENDIAN

#endif // __ENDIAN_HPP__
