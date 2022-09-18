#ifndef __COMB_2_2_2_128M_TOP_H__
#define __COMB_2_2_2_128M_TOP_H__

#include "hbmArbiter_2_2_2_128m_top.h"


extern "C"
void comb_2_2_2_128m_top(
    /*register dmy MU0*/
    unsigned int& MUreg_guard_bgn0,

    unsigned int  wk_nb0,
    unsigned int  min_addr0,
    unsigned int  max_addr0,
    unsigned int  min_data0,
    unsigned int  gap_nb0,

    unsigned int& rdo0_nb0,
    unsigned int& rdo1_nb0,
    unsigned int& rd0err_nb0,
    unsigned int& rd1err_nb0,

    unsigned int& MUreg_guard_end0,
    /*register dmy MU1*/
    unsigned int& MUreg_guard_bgn1,

    unsigned int  wk_nb1,
    unsigned int  min_addr1,
    unsigned int  max_addr1,
    unsigned int  min_data1,
    unsigned int  gap_nb1,

    unsigned int& rdo0_nb1,
    unsigned int& rdo1_nb1,
    unsigned int& rd0err_nb1,
    unsigned int& rd1err_nb1,

    unsigned int& MUreg_guard_end1,

    /*register latency 0*/
    unsigned int& LMreg_guard_bgn0,
    unsigned int& free_cnt0,
    unsigned int& up_nb0,
    unsigned int& dn_nb0,
    unsigned int& up_last_tick0,
    unsigned int& dn_last_tick0,
    unsigned int  history_id0,
    unsigned int& up_history_tick0,
    unsigned int& dn_history_tick0,
    bool          reset_reg0,
    unsigned int& LMreg_guard_end0,

    /*register latency 1*/
    unsigned int& LMreg_guard_bgn1,
    unsigned int& free_cnt1,
    unsigned int& up_nb1,
    unsigned int& dn_nb1,
    unsigned int& up_last_tick1,
    unsigned int& dn_last_tick1,
    unsigned int  history_id1,
    unsigned int& up_history_tick1,
    unsigned int& dn_history_tick1,
    bool          reset_reg1,
    unsigned int& LMreg_guard_end1,

    /*register latency 2*/
    unsigned int& LMreg_guard_bgn2,
    unsigned int& free_cnt2,
    unsigned int& up_nb2,
    unsigned int& dn_nb2,
    unsigned int& up_last_tick2,
    unsigned int& dn_last_tick2,
    unsigned int  history_id2,
    unsigned int& up_history_tick2,
    unsigned int& dn_history_tick2,
    bool          reset_reg2,
    unsigned int& LMreg_guard_end2,

    /*register latency 3*/
    unsigned int& LMreg_guard_bgn3,
    unsigned int& free_cnt3,
    unsigned int& up_nb3,
    unsigned int& dn_nb3,
    unsigned int& up_last_tick3,
    unsigned int& dn_last_tick3,
    unsigned int  history_id3,
    unsigned int& up_history_tick3,
    unsigned int& dn_history_tick3,
    bool          reset_reg3,
    unsigned int& LMreg_guard_end3,

    /*register arbiter*/
    unsigned int& ABreg_guard_bgn,
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

    unsigned int& ABreg_guard_end,

    /*hbm*/
    ap_uint<256> hbm[HBM_ENTRIES_256MB_256w]
);




#endif