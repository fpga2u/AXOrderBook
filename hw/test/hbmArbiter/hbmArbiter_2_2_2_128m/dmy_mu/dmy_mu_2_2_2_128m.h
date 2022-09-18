#ifndef __DMY_MU_2_2_2_128M_H__
#define __DMY_MU_2_2_2_128M_H__

#include "hbmArbiter_2_2_2_128m.h"

template<int id>
class dmy_mu_2_2_2_128m
{

using raddr_st=hbmArbiter_2_2_2_128m::raddr_st;
using rdata_st=hbmArbiter_2_2_2_128m::rdata_st;
using wi_st=hbmArbiter_2_2_2_128m::wi_st;
using raddr_t=hbmArbiter_2_2_2_128m::raddr_t;
using rdata_t=hbmArbiter_2_2_2_128m::rdata_t;
using wi_t=hbmArbiter_2_2_2_128m::wi_t;

public:


static
void mainRun(
    /* register-to-host */
    unsigned int& reg_guard_bgn,

    unsigned int  wk_nb,
    unsigned int  min_addr,
    unsigned int  max_addr,
    unsigned int  min_data,
    unsigned int  gap_nb,

    unsigned int& rdo0_nb,
    unsigned int& rdo1_nb,
    unsigned int& rd0err_nb,
    unsigned int& rd1err_nb,

    unsigned int& reg_guard_end,

    //rd0
    hbmArbiter_2_2_2_128m::rdiStream_t& rdi0,
    hbmArbiter_2_2_2_128m::rdoStream_t& rdo0,
    //rd1
    hbmArbiter_2_2_2_128m::rdiStream_t& rdi1,
    hbmArbiter_2_2_2_128m::rdoStream_t& rdo1,
    //wr0
    hbmArbiter_2_2_2_128m::wriStream_t& wri0,
    //wr1
    hbmArbiter_2_2_2_128m::wriStream_t& wri1
)
{
    reg_guard_bgn = 0xD222128B;
    reg_guard_end = 0xD222128E;

    static int reg_rdo0_nb = 0;
    static int reg_rdo1_nb = 0;
    static int reg_rd0err_nb = 0;
    static int reg_rd1err_nb = 0;

    ap_uint<21> addr;

    addr = min_addr;
    loop_write0:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        wi_st wri;
        wri.data.range(256+21-1, 256) = addr;
        wri.data.range(255, 0) = min_data + addr;
        if (++addr>=max_addr) addr = min_addr;
        wri.last = 1;
        wri0.write(wri);
    }

    loop_write0_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        if (!rdo0.empty()){
            rdata_st rdo = rdo0.read();
            reg_rdo0_nb++;
        }
    }

    loop_write1:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        wi_st wri;
        wri.data.range(256+21-1, 256) = addr;
        wri.data.range(255, 0) = min_data + addr;
        if (++addr>=max_addr) addr = min_addr;
        wri.last = 1;
        wri1.write(wri);
    }

    loop_write1_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        if (!rdo1.empty()){
            rdata_st rdo = rdo1.read();
            reg_rdo1_nb++;
        }
    }


    ap_uint<21> addr_tgt = addr;
    loop_read0_r:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        raddr_st rdi;
        rdi.data.range(21-1, 0) = --addr;
        if (addr==min_addr) addr = max_addr;
        rdi.last = 1;
        rdi0.write(rdi);
    }

    loop_read0_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        if (!rdo1.empty()){
            rdata_st rdo = rdo1.read();
            reg_rdo1_nb++;
        }
    }

    loop_read0_a:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        if (!rdo0.empty()){
            rdata_st rdo = rdo0.read();
            if (--addr_tgt + min_addr != rdo.data){
                reg_rd0err_nb++;
            }
            if (addr_tgt==min_addr) addr_tgt = max_addr;
            reg_rdo0_nb++;
        }
    }


    loop_read1_r:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        raddr_st rdi;
        rdi.data.range(21-1, 0) = --addr;
        if (addr==min_addr) addr = max_addr;
        rdi.last = 1;
        rdi1.write(rdi);
    }

    loop_read1_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        if (!rdo0.empty()){
            rdata_st rdo = rdo0.read();
            reg_rdo0_nb++;
        }
    }

    loop_read1_a:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        if (!rdo1.empty()){
            rdata_st rdo = rdo1.read();
            if (--addr_tgt + min_addr != rdo.data){
                reg_rd1err_nb++;
            }
            if (addr_tgt==min_addr) addr_tgt = max_addr;
            reg_rdo1_nb++;
        }
    }

    rdo0_nb = reg_rdo0_nb;
    rdo1_nb = reg_rdo1_nb;
    rd0err_nb = reg_rd0err_nb;
    rd1err_nb = reg_rd1err_nb;

}


};

#endif
