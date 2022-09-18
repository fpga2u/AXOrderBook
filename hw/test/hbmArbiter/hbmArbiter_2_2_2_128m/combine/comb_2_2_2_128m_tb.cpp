#include "comb_2_2_2_128m_top.h"


#define CALL_DUT()\
    comb_2_2_2_128m_top(\
    MUreg_guard_bgn0,\
\
    wk_nb0,\
    min_addr0,\
    max_addr0,\
    min_data0,\
    gap_nb0,\
\
    rdo0_nb0,\
    rdo1_nb0,\
    rd0err_nb0,\
    rd1err_nb0,\
\
    MUreg_guard_end0,\
    MUreg_guard_bgn1,\
\
    wk_nb1,\
    min_addr1,\
    max_addr1,\
    min_data1,\
    gap_nb1,\
\
    rdo0_nb1,\
    rdo1_nb1,\
    rd0err_nb1,\
    rd1err_nb1,\
\
    MUreg_guard_end1,\
\
    LMreg_guard_bgn0,\
    free_cnt0,\
    up_nb0,\
    dn_nb0,\
    up_last_tick0,\
    dn_last_tick0,\
    history_id0,\
    up_history_tick0,\
    dn_history_tick0,\
    reset_reg0,\
    LMreg_guard_end0,\
\
    LMreg_guard_bgn1,\
    free_cnt1,\
    up_nb1,\
    dn_nb1,\
    up_last_tick1,\
    dn_last_tick1,\
    history_id1,\
    up_history_tick1,\
    dn_history_tick1,\
    reset_reg1,\
    LMreg_guard_end1,\
\
    LMreg_guard_bgn2,\
    free_cnt2,\
    up_nb2,\
    dn_nb2,\
    up_last_tick2,\
    dn_last_tick2,\
    history_id2,\
    up_history_tick2,\
    dn_history_tick2,\
    reset_reg2,\
    LMreg_guard_end2,\
\
    LMreg_guard_bgn3,\
    free_cnt3,\
    up_nb3,\
    dn_nb3,\
    up_last_tick3,\
    dn_last_tick3,\
    history_id3,\
    up_history_tick3,\
    dn_history_tick3,\
    reset_reg3,\
    LMreg_guard_end3,\
\
    ABreg_guard_bgn,\
    mu0_rdi_nb,\
    mu0_wri_nb,\
    mu0_rdo_nb,\
    mu0_max_addr,\
    mu1_rdi_nb,\
    mu1_wri_nb,\
    mu1_rdo_nb,\
    mu1_max_addr,\
    hbm_rd_nb,\
    hbm_wr_nb,\
\
    ABreg_guard_end,\
\
    hbm\
\
    )











int main(){

    /*register dmy MU0*/
    unsigned int MUreg_guard_bgn0 = 0;

    unsigned int  wk_nb0 = 16;
    unsigned int  min_addr0 = 0;
    unsigned int  max_addr0 = 16;
    unsigned int  min_data0 = 0;
    unsigned int  gap_nb0 = 4;

    unsigned int rdo0_nb0 = 0;
    unsigned int rdo1_nb0 = 0;
    unsigned int rd0err_nb0 = 0;
    unsigned int rd1err_nb0 = 0;

    unsigned int MUreg_guard_end0 = 0;
    /*register dmy MU1*/
    unsigned int MUreg_guard_bgn1 = 0;

    unsigned int  wk_nb1 = 64;
    unsigned int  min_addr1 = 64;
    unsigned int  max_addr1 = 128;
    unsigned int  min_data1 = 0;
    unsigned int  gap_nb1 = 1;

    unsigned int rdo0_nb1 = 0;
    unsigned int rdo1_nb1 = 0;
    unsigned int rd0err_nb1 = 0;
    unsigned int rd1err_nb1 = 0;

    unsigned int MUreg_guard_end1 = 0;

    /*register latency 0*/
    unsigned int LMreg_guard_bgn0 = 0;
    unsigned int free_cnt0 = 0;
    unsigned int up_nb0 = 0;
    unsigned int dn_nb0 = 0;
    unsigned int up_last_tick0 = 0;
    unsigned int dn_last_tick0 = 0;
    unsigned int  history_id0 = 0;
    unsigned int up_history_tick0 = 0;
    unsigned int dn_history_tick0 = 0;
    bool          reset_reg0 = 0;
    unsigned int LMreg_guard_end0 = 0;

    /*register latency 1*/
    unsigned int LMreg_guard_bgn1 = 0;
    unsigned int free_cnt1 = 0;
    unsigned int up_nb1 = 0;
    unsigned int dn_nb1 = 0;
    unsigned int up_last_tick1 = 0;
    unsigned int dn_last_tick1 = 0;
    unsigned int  history_id1 = 0;
    unsigned int up_history_tick1 = 0;
    unsigned int dn_history_tick1 = 0;
    bool          reset_reg1 = 0;
    unsigned int LMreg_guard_end1 = 0;

    /*register latency 2*/
    unsigned int LMreg_guard_bgn2 = 0;
    unsigned int free_cnt2 = 0;
    unsigned int up_nb2 = 0;
    unsigned int dn_nb2 = 0;
    unsigned int up_last_tick2 = 0;
    unsigned int dn_last_tick2 = 0;
    unsigned int  history_id2 = 0;
    unsigned int up_history_tick2 = 0;
    unsigned int dn_history_tick2 = 0;
    bool          reset_reg2 = 0;
    unsigned int LMreg_guard_end2 = 0;

    /*register latency 3*/
    unsigned int LMreg_guard_bgn3 = 0;
    unsigned int free_cnt3 = 0;
    unsigned int up_nb3 = 0;
    unsigned int dn_nb3 = 0;
    unsigned int up_last_tick3 = 0;
    unsigned int dn_last_tick3 = 0;
    unsigned int  history_id3 = 0;
    unsigned int up_history_tick3 = 0;
    unsigned int dn_history_tick3 = 0;
    bool          reset_reg3 = 0;
    unsigned int LMreg_guard_end3 = 0;

    /*register arbiter*/
    unsigned int ABreg_guard_bgn = 0;
    //mu0
    unsigned int mu0_rdi_nb = 0;
    unsigned int mu0_wri_nb = 0;
    unsigned int mu0_rdo_nb = 0;
    unsigned int mu0_max_addr = 0;
    //mu1
    unsigned int mu1_rdi_nb = 0;
    unsigned int mu1_wri_nb = 0;
    unsigned int mu1_rdo_nb = 0;
    unsigned int mu1_max_addr = 0;
    //hbm
    unsigned int hbm_rd_nb = 0;
    unsigned int hbm_wr_nb = 0;

    unsigned int ABreg_guard_end = 0;

    /*hbm*/
    ap_uint<256> hbm[HBM_ENTRIES_256MB_256w];
    for (int i=0; i<HBM_ENTRIES_256MB_256w;++i){
        hbm[i] = 0;
    }

    CALL_DUT();

    wk_nb0 = 0;
    wk_nb1 = 0;

    for (int i=0; i<258; ++i){
        CALL_DUT();
        printf("-------- %d\n", i);
        printf("mu0 rdo0_nb=%d; rdo1_nb=%d\n", rdo0_nb0, rdo1_nb0);
        printf("mu1 rdo0_nb=%d; rdo1_nb=%d\n", rdo0_nb1, rdo1_nb1);
        printf("lm0 up_nb=%d; dn_nb=%d\n", up_nb0, dn_nb0);
        printf("lm1 up_nb=%d; dn_nb=%d\n", up_nb1, dn_nb1);
        printf("lm2 up_nb=%d; dn_nb=%d\n", up_nb2, dn_nb2);
        printf("lm3 up_nb=%d; dn_nb=%d\n", up_nb3, dn_nb3);
        printf("AB mu0_wri_nb=%d; mu0_rdi_nb=%d; mu0_rdo_nb=%d\n", mu0_wri_nb, mu0_rdi_nb, mu0_rdo_nb);
        printf("   mu1_wri_nb=%d; mu1_rdi_nb=%d; mu1_rdo_nb=%d\n", mu1_wri_nb, mu1_rdi_nb, mu1_rdo_nb);
        printf("   hbm_rd_nb=%d; hbm_wr_nb=%d;\n", hbm_rd_nb, hbm_wr_nb);
    }

    assert(rdo0_nb0==16);
    assert(rdo1_nb0==16);
    assert(rd0err_nb0==0);
    assert(rd1err_nb0==0);

    assert(rdo0_nb1==64);
    assert(rdo1_nb1==64);
    assert(rd0err_nb1==0);
    assert(rd1err_nb1==0);

    std::cout << "TEST OK!" << std::endl;
    return 0;
}