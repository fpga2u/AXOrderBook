#ifndef __DMY_MU_2_2_2_128M_H__
#define __DMY_MU_2_2_2_128M_H__

#include "hbmArbiter_2_2_2_128m.h"
#include <bitset>

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

    unsigned int& wr0_wk_nb,
    unsigned int& wr1_wk_nb,
    unsigned int& rd0_wk_nb,
    unsigned int& rd1_wk_nb,
    unsigned int& rdo0_rx_nb,
    unsigned int& rdo1_rx_nb,
    unsigned int& rd0err_nb,
    unsigned int& rd1err_nb,
    unsigned int& gap_wk_nb,

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
    const unsigned int guard_bgn = 0xD222128B;
    const unsigned int guard_end = 0xD222128E;

    static int reg_wr0_wk_nb = 0;
    static int reg_wr1_wk_nb = 0;
    static int reg_rd0_wk_nb = 0;
    static int reg_rd1_wk_nb = 0;
    static int reg_rdo0_rx_nb = 0;
    static int reg_rdo1_rx_nb = 0;
    static int reg_rd0err_nb = 0;
    static int reg_rd1err_nb = 0;
    static int reg_gap_wk_nb = 0;

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
        reg_wr0_wk_nb++;
    }

    loop_write0_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        // if (!rdo0.empty()){ //TODO: 不合理
        //     rdata_st rdo = rdo0.read();
        //     reg_rdo0_rx_nb++;
        // }
        reg_gap_wk_nb++;
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
        reg_wr1_wk_nb++;
    }

    loop_write1_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        // if (!rdo1.empty()){ //TODO: 不合理
        //     rdata_st rdo = rdo1.read();
        //     reg_rdo1_rx_nb++;
        // }
        reg_gap_wk_nb++;
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
        reg_rd0_wk_nb++;
    }

    loop_read0_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        // if (!rdo1.empty()){ //TODO: 不合理
        //     rdata_st rdo = rdo1.read();
        //     reg_rdo1_rx_nb++;
        // }
        reg_gap_wk_nb++;
    }

    loop_read0_a:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        // if (!rdo0.empty()){ //TODO: 这里不该用非阻塞，当读写异步时，实机会快速地跳过这里，rdo0的数据就遗留在队列中，使得Arbiter阻塞在write
            rdata_st rdo = rdo0.read();
            // printf("t=%s r=%s\n", std::bitset<8>(addr_tgt-1 + min_data).to_string().c_str(), rdo.data.to_string(16).c_str());
            // printf("t=%X r=%s\n", addr_tgt-1 + min_data, rdo.data.to_string(16).c_str());
            if (--addr_tgt + min_data != rdo.data){
                reg_rd0err_nb++;
            }
            if (addr_tgt==min_addr) addr_tgt = max_addr;
            reg_rdo0_rx_nb++;
        // }
    }


    loop_read1_r:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        raddr_st rdi;
        rdi.data.range(21-1, 0) = --addr;
        if (addr==min_addr) addr = max_addr;
        rdi.last = 1;
        rdi1.write(rdi);
        reg_rd1_wk_nb++;
    }

    loop_read1_gap:
    for (int i=0; i<gap_nb; ++i){
    #pragma HLS PIPELINE II = 16
        // if (!rdo0.empty()){ //TODO: 不合理
        //     rdata_st rdo = rdo0.read();
        //     reg_rdo0_rx_nb++;
        // }
        reg_gap_wk_nb++;
    }

    loop_read1_a:
    for (int i=0; i<wk_nb; ++i){
    #pragma HLS PIPELINE II = 1
        // if (!rdo1.empty()){ //TODO: 这里不该用非阻塞，当读写异步时，实机会快速地跳过这里，rdo0的数据就遗留在队列中，使得Arbiter阻塞在write
            rdata_st rdo = rdo1.read();
            if (--addr_tgt + min_data != rdo.data){
                reg_rd1err_nb++;
            }
            if (addr_tgt==min_addr) addr_tgt = max_addr;
            reg_rdo1_rx_nb++;
        // }
    }

    wr0_wk_nb = reg_wr0_wk_nb;
    wr1_wk_nb = reg_wr1_wk_nb;
    rd0_wk_nb = reg_rd0_wk_nb;
    rd1_wk_nb = reg_rd1_wk_nb;
    rdo0_rx_nb = reg_rdo0_rx_nb;
    rdo1_rx_nb = reg_rdo1_rx_nb;
    rd0err_nb = reg_rd0err_nb;
    rd1err_nb = reg_rd1err_nb;
    gap_wk_nb = reg_gap_wk_nb;

    reg_guard_bgn = guard_bgn; //TODO: 实机会读成0
    reg_guard_end = guard_end;
}


};

#endif
