
#ifndef __HBMARBITER_2_2_2_128M_TOP_H__
#define __HBMARBITER_2_2_2_128M_TOP_H__

#include "hbmArbiter_2_2_2_128m.h"

extern "C"
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
    hbmArbiter_2_2_2_128m::rdiStream_t& mu0_rdi0,
    hbmArbiter_2_2_2_128m::rdoStream_t& mu0_rdo0,
    //rd1
    hbmArbiter_2_2_2_128m::rdiStream_t& mu0_rdi1,
    hbmArbiter_2_2_2_128m::rdoStream_t& mu0_rdo1,
    //wr0
    hbmArbiter_2_2_2_128m::wriStream_t& mu0_wri0,
    //wr1
    hbmArbiter_2_2_2_128m::wriStream_t& mu0_wri1,

    /* mu1 */
    //rd0
    hbmArbiter_2_2_2_128m::rdiStream_t& mu1_rdi0,
    hbmArbiter_2_2_2_128m::rdoStream_t& mu1_rdo0,
    //rd1
    hbmArbiter_2_2_2_128m::rdiStream_t& mu1_rdi1,
    hbmArbiter_2_2_2_128m::rdoStream_t& mu1_rdo1,
    //wr0
    hbmArbiter_2_2_2_128m::wriStream_t& mu1_wri0,
    //wr1
    hbmArbiter_2_2_2_128m::wriStream_t& mu1_wri1,

    /* hbm */
    ap_uint<256> hbm[HBM_ENTRIES_256MB_256w]
);

#endif
