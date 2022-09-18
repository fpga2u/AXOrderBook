#include "hbmArbiter_2_2_2_128m_top.h"

using namespace hbmArbiter_2_2_2_128m;

void hbmArbiter_2_2_2_128m_top(
    /* register-to-host */
    unsigned int& reg_guard_bgn,
    //mu0
    unsigned int& mu0_rdi_nb,
    unsigned int& mu0_wri_nb,
    unsigned int& mu0_rdo_nb,
    unsigned int& mu0_max_addr,
    //mu1
    unsigned int& mu1_rdi_nb,
    unsigned int& mu1_wri_nb,
    unsigned int& mu1_rdo_nb,
    unsigned int& mu1_max_addr,
    //hbm
    unsigned int& hbm_rd_nb,
    unsigned int& hbm_wr_nb,

    unsigned int& reg_guard_end,

    /* mu0 */
    //rd0
    rdiStream_t& mu0_rdi0,
    rdoStream_t& mu0_rdo0,
    //rd1
    rdiStream_t& mu0_rdi1,
    rdoStream_t& mu0_rdo1,
    //wr0
    wriStream_t& mu0_wri0,
    //wr1
    wriStream_t& mu0_wri1,

    /* mu1 */
    //rd0
    rdiStream_t& mu1_rdi0,
    rdoStream_t& mu1_rdo0,
    //rd1
    rdiStream_t& mu1_rdi1,
    rdoStream_t& mu1_rdo1,
    //wr0
    wriStream_t& mu1_wri0,
    //wr1
    wriStream_t& mu1_wri1,

    /* hbm */
    ap_uint<256> hbm[HBM_ENTRIES_256MB_256w]
)
{
/* register-to-host */
#pragma HLS INTERFACE s_axilite port=reg_guard_bgn  bundle=control
#pragma HLS INTERFACE s_axilite port=reg_guard_end  bundle=control
#pragma HLS INTERFACE s_axilite port=mu0_rdi_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=mu0_rdo_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=mu0_wri_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=mu0_max_addr  bundle=control
#pragma HLS INTERFACE s_axilite port=mu1_rdi_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=mu1_rdo_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=mu1_wri_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=mu1_max_addr  bundle=control
#pragma HLS INTERFACE s_axilite port=hbm_rd_nb  bundle=control
#pragma HLS INTERFACE s_axilite port=hbm_wr_nb  bundle=control
/* mu0 */
//rd0
#pragma HLS INTERFACE axis port=mu0_rdi0 depth=8
#pragma HLS INTERFACE axis port=mu0_rdo0 depth=8
//rd1
#pragma HLS INTERFACE axis port=mu0_rdi1 depth=8
#pragma HLS INTERFACE axis port=mu0_rdo1 depth=8
//wr0
#pragma HLS INTERFACE axis port=mu0_wri0 depth=8
//wr1
#pragma HLS INTERFACE axis port=mu0_wri1 depth=8

/* mu1 */
//rd0
#pragma HLS INTERFACE axis port=mu1_rdi0 depth=8
#pragma HLS INTERFACE axis port=mu1_rdo0 depth=8
//rd1
#pragma HLS INTERFACE axis port=mu1_rdi1 depth=8
#pragma HLS INTERFACE axis port=mu1_rdo1 depth=8
//wr0
#pragma HLS INTERFACE axis port=mu1_wri0 depth=8
//wr1
#pragma HLS INTERFACE axis port=mu1_wri1 depth=8

/* hbm */
// #pragma HLS INTERFACE m_axi port=hbm offset=slave bundle=gmem0 latency=50 num_read_outstanding=128 num_write_outstanding=128     //cosim work
// #pragma HLS INTERFACE m_axi port=hbm offset=slave bundle=gmem0 latency=300 num_read_outstanding=128 num_write_outstanding=128    //cosim work
// #pragma HLS INTERFACE m_axi port=hbm offset=slave bundle=gmem0 latency=300 num_read_outstanding=1 num_write_outstanding=1        //cosim work
#pragma HLS INTERFACE m_axi port=hbm offset=slave bundle=gmem0 latency=0 num_read_outstanding=4 num_write_outstanding=4 max_read_burst_length=4 max_write_burst_length=1
#pragma HLS INTERFACE s_axilite port=hbm bundle=control

/* proto */
#ifdef _C_TEST_     //for CSIM/CSYNTH/COSIM
#pragma HLS INTERFACE ap_ctrl_hs port=return
#pragma HLS INTERFACE s_axilite port=return bundle=control
#else               //for vitis hw
#pragma HLS INTERFACE ap_ctrl_none port=return
#endif

#pragma HLS dataflow


    arbiter::mainRun<0>(
        reg_guard_bgn,
        mu0_rdi_nb,
        mu0_wri_nb,
        mu0_rdo_nb,
        mu0_max_addr,
        mu1_rdi_nb,
        mu1_wri_nb,
        mu1_rdo_nb,
        mu1_max_addr,
        hbm_rd_nb,
        hbm_wr_nb,
        reg_guard_end,

        mu0_rdi0,
        mu0_rdo0,
        mu0_rdi1,
        mu0_rdo1,
        mu0_wri0,
        mu0_wri1,
        mu1_rdi0,
        mu1_rdo0,
        mu1_rdi1,
        mu1_rdo1,
        mu1_wri0,
        mu1_wri1,
        hbm
    );

}
