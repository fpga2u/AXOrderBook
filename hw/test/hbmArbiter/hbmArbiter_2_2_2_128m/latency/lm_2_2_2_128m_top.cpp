#include "lm_2_2_2_128m_top.h"
#include "latencyMoniter.h"

using namespace hbmArbiter_2_2_2_128m;


void lm_2_2_2_128m_top(
        unsigned int&  reg_guard_bgn,
        unsigned int&  free_cnt,
        unsigned int&  up_nb,
        unsigned int&  dn_nb,
        unsigned int&  up_last_tick,
        unsigned int&  dn_last_tick,
        unsigned int   history_id,
        unsigned int&  up_history_tick,
        unsigned int&  dn_history_tick,
        bool           reset_reg,
        unsigned int&  reg_guard_end,
        hbmArbiter_2_2_2_128m::rdiStream_t& up_in,
        hbmArbiter_2_2_2_128m::rdiStream_t& up_out,
        hbmArbiter_2_2_2_128m::rdoStream_t& dn_in,
        hbmArbiter_2_2_2_128m::rdoStream_t& dn_out
)
{
/* register-to-host */
//guard
#pragma HLS INTERFACE s_axilite port=reg_guard_bgn   bundle=control
#pragma HLS INTERFACE s_axilite port=reg_guard_end   bundle=control
#pragma HLS INTERFACE mode=ap_none port=reg_guard_bgn
#pragma HLS INTERFACE mode=ap_none port=reg_guard_end

//app
#pragma HLS INTERFACE s_axilite port=free_cnt   bundle=control
#pragma HLS INTERFACE s_axilite port=up_nb   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_nb   bundle=control
#pragma HLS INTERFACE s_axilite port=up_last_tick   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_last_tick   bundle=control
#pragma HLS INTERFACE s_axilite port=history_id   bundle=control
#pragma HLS INTERFACE s_axilite port=up_history_tick   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_history_tick   bundle=control
#pragma HLS INTERFACE s_axilite port=reset_reg   bundle=control

//app output register
#pragma HLS INTERFACE mode=ap_none port=free_cnt
#pragma HLS INTERFACE mode=ap_none port=up_nb
#pragma HLS INTERFACE mode=ap_none port=dn_nb
#pragma HLS INTERFACE mode=ap_none port=up_last_tick
#pragma HLS INTERFACE mode=ap_none port=dn_last_tick
#pragma HLS INTERFACE mode=ap_none port=up_history_tick
#pragma HLS INTERFACE mode=ap_none port=dn_history_tick

/* data flow stream */
#pragma HLS INTERFACE axis port=up_in
#pragma HLS INTERFACE axis port=up_out
#pragma HLS INTERFACE axis port=dn_in
#pragma HLS INTERFACE axis port=dn_out

#ifdef _C_TEST_
#pragma HLS INTERFACE ap_ctrl_chain port=return
#else    //for vitis hw
#pragma HLS INTERFACE ap_ctrl_none port=return
#endif

#pragma HLS dataflow

    latencyMoniter<raddr_st, rdata_st, 0x222128FB, 0x222128FE>::mainRun(
        up_in,
        up_out,
        dn_in,
        dn_out,
        reg_guard_bgn,
        free_cnt,
        up_nb,
        dn_nb,
        up_last_tick,
        dn_last_tick,
        history_id,
        up_history_tick,
        dn_history_tick,
        reset_reg,
        reg_guard_end
    );
}

