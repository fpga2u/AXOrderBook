#ifndef __DMY_MU_2_2_2_128M_TOP_H__
#define __DMY_MU_2_2_2_128M_TOP_H__

#include "hbmArbiter_2_2_2_128m.h"

extern "C"
void dmy_mu_2_2_2_128m_top(
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
);


#endif
