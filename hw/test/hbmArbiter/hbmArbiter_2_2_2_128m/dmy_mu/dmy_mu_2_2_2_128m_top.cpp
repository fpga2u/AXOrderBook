#include "dmy_mu_2_2_2_128m_top.h"
#include "dmy_mu_2_2_2_128m.h"


void dmy_mu_2_2_2_128m_top(
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
/* register-to-host */
#pragma HLS INTERFACE s_axilite port=reg_guard_bgn  bundle=control
#pragma HLS INTERFACE s_axilite port=reg_guard_end  bundle=control

#pragma HLS INTERFACE s_axilite port=wk_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=min_addr  bundle=control
#pragma HLS INTERFACE s_axilite port=max_addr  bundle=control
#pragma HLS INTERFACE s_axilite port=min_data  bundle=control
#pragma HLS INTERFACE s_axilite port=gap_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=rdo0_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=rdo1_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=rd0err_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=rd1err_nb  bundle=control
/* mu0 */
//rd0
#pragma HLS INTERFACE axis port=rdi0
#pragma HLS INTERFACE axis port=rdo0
//rd1
#pragma HLS INTERFACE axis port=rdi1
#pragma HLS INTERFACE axis port=rdo1
//wr0
#pragma HLS INTERFACE axis port=wri0
//wr1
#pragma HLS INTERFACE axis port=wri1

/* proto */
// #pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE s_axilite port=return bundle=control

    dmy_mu_2_2_2_128m<0>::mainRun(
        /* register-to-host */
        reg_guard_bgn,

        wk_nb,
        min_addr,
        max_addr,
        min_data,
        gap_nb,

        rdo0_nb,
        rdo1_nb,
        rd0err_nb,
        rd1err_nb,

        reg_guard_end,

        //rd0
        rdi0,
        rdo0,
        //rd1
        rdi1,
        rdo1,
        //wr0
        wri0,
        //wr1
        wri1
    );

}
