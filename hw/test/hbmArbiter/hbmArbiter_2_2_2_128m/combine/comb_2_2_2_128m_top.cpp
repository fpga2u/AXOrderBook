

#include "comb_2_2_2_128m_top.h"
#include "dmy_mu_2_2_2_128m.h"
#include "latencyMoniter.h"

using namespace hbmArbiter_2_2_2_128m;


void mu0(
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
    dmy_mu_2_2_2_128m<0>::mainRun(
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
        rdi0,
        rdo0,
        rdi1,
        rdo1,
        wri0,
        wri1
    );
};

void mu1(
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
    dmy_mu_2_2_2_128m<1>::mainRun(
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
        rdi0,
        rdo0,
        rdi1,
        rdo1,
        wri0,
        wri1
    );
};


void lm_mu0_rd0(
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
    latencyMoniter<raddr_st, rdata_st, 0x222128B0, 0x222128E0>::mainRun(
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
};

void lm_mu0_rd1(
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
    latencyMoniter<raddr_st, rdata_st, 0x222128B1, 0x222128E1>::mainRun(
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
};

void lm_mu1_rd0(
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
    latencyMoniter<raddr_st, rdata_st, 0x222128B2, 0x222128E2>::mainRun(
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
};

void lm_mu1_rd1(
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
    latencyMoniter<raddr_st, rdata_st, 0x222128B3, 0x222128E3>::mainRun(
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
};

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
)
{

/*register dmy MU0*/
#pragma HLS INTERFACE s_axilite port=MUreg_guard_bgn0  bundle=control
#pragma HLS INTERFACE s_axilite port=MUreg_guard_end0  bundle=control

#pragma HLS INTERFACE s_axilite port=wk_nb0  bundle=control
#pragma HLS INTERFACE s_axilite port=min_addr0  bundle=control
#pragma HLS INTERFACE s_axilite port=max_addr0  bundle=control
#pragma HLS INTERFACE s_axilite port=min_data0  bundle=control
#pragma HLS INTERFACE s_axilite port=gap_nb0  bundle=control
#pragma HLS INTERFACE s_axilite port=rdo0_nb0  bundle=control
#pragma HLS INTERFACE s_axilite port=rdo1_nb0  bundle=control
#pragma HLS INTERFACE s_axilite port=rd0err_nb0  bundle=control
#pragma HLS INTERFACE s_axilite port=rd1err_nb0  bundle=control
/*register dmy MU1*/
#pragma HLS INTERFACE s_axilite port=MUreg_guard_bgn1  bundle=control
#pragma HLS INTERFACE s_axilite port=MUreg_guard_end1  bundle=control

#pragma HLS INTERFACE s_axilite port=wk_nb1  bundle=control
#pragma HLS INTERFACE s_axilite port=min_addr1  bundle=control
#pragma HLS INTERFACE s_axilite port=max_addr1  bundle=control
#pragma HLS INTERFACE s_axilite port=min_data1  bundle=control
#pragma HLS INTERFACE s_axilite port=gap_nb1  bundle=control
#pragma HLS INTERFACE s_axilite port=rdo0_nb1  bundle=control
#pragma HLS INTERFACE s_axilite port=rdo1_nb1  bundle=control
#pragma HLS INTERFACE s_axilite port=rd0err_nb1  bundle=control
#pragma HLS INTERFACE s_axilite port=rd1err_nb1  bundle=control

/*register latency 0*/
#pragma HLS INTERFACE s_axilite port=LMreg_guard_bgn0  bundle=control
#pragma HLS INTERFACE s_axilite port=LMreg_guard_end0  bundle=control
#pragma HLS INTERFACE s_axilite port=free_cnt0   bundle=control
#pragma HLS INTERFACE s_axilite port=up_nb0   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_nb0   bundle=control
#pragma HLS INTERFACE s_axilite port=up_last_tick0   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_last_tick0   bundle=control
#pragma HLS INTERFACE s_axilite port=history_id0   bundle=control
#pragma HLS INTERFACE s_axilite port=up_history_tick0   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_history_tick0   bundle=control
#pragma HLS INTERFACE s_axilite port=reset_reg0   bundle=control

/*register latency 1*/
#pragma HLS INTERFACE s_axilite port=LMreg_guard_bgn1  bundle=control
#pragma HLS INTERFACE s_axilite port=LMreg_guard_end1  bundle=control
#pragma HLS INTERFACE s_axilite port=free_cnt1   bundle=control
#pragma HLS INTERFACE s_axilite port=up_nb1   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_nb1   bundle=control
#pragma HLS INTERFACE s_axilite port=up_last_tick1   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_last_tick1   bundle=control
#pragma HLS INTERFACE s_axilite port=history_id1   bundle=control
#pragma HLS INTERFACE s_axilite port=up_history_tick1   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_history_tick1   bundle=control
#pragma HLS INTERFACE s_axilite port=reset_reg1   bundle=control

/*register latency 2*/
#pragma HLS INTERFACE s_axilite port=LMreg_guard_bgn2  bundle=control
#pragma HLS INTERFACE s_axilite port=LMreg_guard_end2  bundle=control
#pragma HLS INTERFACE s_axilite port=free_cnt2   bundle=control
#pragma HLS INTERFACE s_axilite port=up_nb2   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_nb2   bundle=control
#pragma HLS INTERFACE s_axilite port=up_last_tick2   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_last_tick2   bundle=control
#pragma HLS INTERFACE s_axilite port=history_id2   bundle=control
#pragma HLS INTERFACE s_axilite port=up_history_tick2   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_history_tick2   bundle=control
#pragma HLS INTERFACE s_axilite port=reset_reg2   bundle=control

/*register latency 3*/
#pragma HLS INTERFACE s_axilite port=LMreg_guard_bgn3  bundle=control
#pragma HLS INTERFACE s_axilite port=LMreg_guard_end3  bundle=control
#pragma HLS INTERFACE s_axilite port=free_cnt3   bundle=control
#pragma HLS INTERFACE s_axilite port=up_nb3   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_nb3   bundle=control
#pragma HLS INTERFACE s_axilite port=up_last_tick3   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_last_tick3   bundle=control
#pragma HLS INTERFACE s_axilite port=history_id3   bundle=control
#pragma HLS INTERFACE s_axilite port=up_history_tick3   bundle=control
#pragma HLS INTERFACE s_axilite port=dn_history_tick3   bundle=control
#pragma HLS INTERFACE s_axilite port=reset_reg3   bundle=control

/*register arbiter*/
#pragma HLS INTERFACE s_axilite port=ABreg_guard_bgn  bundle=control
#pragma HLS INTERFACE s_axilite port=ABreg_guard_end  bundle=control
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

/*hbm*/
#pragma HLS INTERFACE m_axi port=hbm offset=slave bundle=gmem0 latency=0 num_read_outstanding=4 num_write_outstanding=4 max_read_burst_length=4 max_write_burst_length=1
#pragma HLS INTERFACE s_axilite port=hbm bundle=control

#pragma HLS dataflow

    //rd0
    static hbmArbiter_2_2_2_128m::rdiStream_t mu0_rdi0_up("mu0_rdi0_up");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu0_rdo0_up("mu0_rdo0_up");
    //rd1
    static hbmArbiter_2_2_2_128m::rdiStream_t mu0_rdi1_up("mu0_rdi1_up");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu0_rdo1_up("mu0_rdo1_up");
    //wr0
    static hbmArbiter_2_2_2_128m::wriStream_t mu0_wri0("mu0_wri0");
    //wr1
    static hbmArbiter_2_2_2_128m::wriStream_t mu0_wri1("mu0_wri1");
    

    //rd0
    static hbmArbiter_2_2_2_128m::rdiStream_t mu1_rdi0_up("mu1_rdi0_up");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu1_rdo0_up("mu1_rdo0_up");
    //rd1
    static hbmArbiter_2_2_2_128m::rdiStream_t mu1_rdi1_up("mu1_rdi1_up");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu1_rdo1_up("mu1_rdo1_up");
    //wr0
    static hbmArbiter_2_2_2_128m::wriStream_t mu1_wri0("mu1_wri0");
    //wr1
    static hbmArbiter_2_2_2_128m::wriStream_t mu1_wri1("mu1_wri1");


    //rd0
    static hbmArbiter_2_2_2_128m::rdiStream_t mu0_rdi0_dn("mu0_rdi0_dn");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu0_rdo0_dn("mu0_rdo0_dn");
    //rd1
    static hbmArbiter_2_2_2_128m::rdiStream_t mu0_rdi1_dn("mu0_rdi1_dn");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu0_rdo1_dn("mu0_rdo1_dn");
    //rd0
    static hbmArbiter_2_2_2_128m::rdiStream_t mu1_rdi0_dn("mu1_rdi0_dn");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu1_rdo0_dn("mu1_rdo0_dn");
    //rd1
    static hbmArbiter_2_2_2_128m::rdiStream_t mu1_rdi1_dn("mu1_rdi1_dn");
    static hbmArbiter_2_2_2_128m::rdoStream_t mu1_rdo1_dn("mu1_rdo1_dn");

#pragma HLS STREAM variable = mu0_rdi0_up depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdi0_up type = FIFO
#pragma HLS STREAM variable = mu0_rdo0_up depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdo0_up type = FIFO
#pragma HLS STREAM variable = mu0_rdi1_up depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdi1_up type = FIFO
#pragma HLS STREAM variable = mu0_rdo1_up depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdo1_up type = FIFO
#pragma HLS STREAM variable = mu0_wri0 depth=64
#pragma HLS BIND_STORAGE variable = mu0_wri0 type = FIFO
#pragma HLS STREAM variable = mu0_wri1 depth=64
#pragma HLS BIND_STORAGE variable = mu0_wri1 type = FIFO


#pragma HLS STREAM variable = mu1_rdi0_up depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdi0_up type = FIFO
#pragma HLS STREAM variable = mu1_rdo0_up depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdo0_up type = FIFO
#pragma HLS STREAM variable = mu1_rdi1_up depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdi1_up type = FIFO
#pragma HLS STREAM variable = mu1_rdo1_up depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdo1_up type = FIFO
#pragma HLS STREAM variable = mu1_wri0 depth=64
#pragma HLS BIND_STORAGE variable = mu1_wri0 type = FIFO
#pragma HLS STREAM variable = mu1_wri1 depth=64
#pragma HLS BIND_STORAGE variable = mu1_wri1 type = FIFO

#pragma HLS STREAM variable = mu0_rdi0_dn depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdi0_dn type = FIFO
#pragma HLS STREAM variable = mu0_rdo0_dn depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdo0_dn type = FIFO
#pragma HLS STREAM variable = mu0_rdi1_dn depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdi1_dn type = FIFO
#pragma HLS STREAM variable = mu0_rdo1_dn depth=64
#pragma HLS BIND_STORAGE variable = mu0_rdo1_dn type = FIFO

#pragma HLS STREAM variable = mu1_rdi0_dn depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdi0_dn type = FIFO
#pragma HLS STREAM variable = mu1_rdo0_dn depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdo0_dn type = FIFO
#pragma HLS STREAM variable = mu1_rdi1_dn depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdi1_dn type = FIFO
#pragma HLS STREAM variable = mu1_rdo1_dn depth=64
#pragma HLS BIND_STORAGE variable = mu1_rdo1_dn type = FIFO


        mu0(
            MUreg_guard_bgn0,
            wk_nb0,
            min_addr0,
            max_addr0,
            min_data0,
            gap_nb0,
            rdo0_nb0,
            rdo1_nb0,
            rd0err_nb0,
            rd1err_nb0,
            MUreg_guard_end0,
            mu0_rdi0_up,
            mu0_rdo0_up,
            mu0_rdi1_up,
            mu0_rdo1_up,
            mu0_wri0,
            mu0_wri1
        );

        mu1(
            MUreg_guard_bgn1,
            wk_nb1,
            min_addr1,
            max_addr1,
            min_data1,
            gap_nb1,
            rdo0_nb1,
            rdo1_nb1,
            rd0err_nb1,
            rd1err_nb1,
            MUreg_guard_end1,
            mu1_rdi0_up,
            mu1_rdo0_up,
            mu1_rdi1_up,
            mu1_rdo1_up,
            mu1_wri0,
            mu1_wri1
        );

        lm_mu0_rd0(
            LMreg_guard_bgn0,
            free_cnt0,
            up_nb0,
            dn_nb0,
            up_last_tick0,
            dn_last_tick0,
            history_id0,
            up_history_tick0,
            dn_history_tick0,
            reset_reg0,
            LMreg_guard_end0,
            mu0_rdi0_up,
            mu0_rdi0_dn,
            mu0_rdo0_dn,
            mu0_rdo0_up
        );

        lm_mu0_rd1(
            LMreg_guard_bgn1,
            free_cnt1,
            up_nb1,
            dn_nb1,
            up_last_tick1,
            dn_last_tick1,
            history_id1,
            up_history_tick1,
            dn_history_tick1,
            reset_reg1,
            LMreg_guard_end1,
            mu0_rdi1_up,
            mu0_rdi1_dn,
            mu0_rdo1_dn,
            mu0_rdo1_up
        );

        lm_mu1_rd0(
            LMreg_guard_bgn2,
            free_cnt2,
            up_nb2,
            dn_nb2,
            up_last_tick2,
            dn_last_tick2,
            history_id2,
            up_history_tick2,
            dn_history_tick2,
            reset_reg2,
            LMreg_guard_end2,
            mu1_rdi0_up,
            mu1_rdi0_dn,
            mu1_rdo0_dn,
            mu1_rdo0_up
        );

        lm_mu1_rd1(
            LMreg_guard_bgn3,
            free_cnt3,
            up_nb3,
            dn_nb3,
            up_last_tick3,
            dn_last_tick3,
            history_id3,
            up_history_tick3,
            dn_history_tick3,
            reset_reg3,
            LMreg_guard_end3,
            mu1_rdi1_up,
            mu1_rdi1_dn,
            mu1_rdo1_dn,
            mu1_rdo1_up
        );


        arbiter::mainRun<0>(
            ABreg_guard_bgn,
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
            ABreg_guard_end,
            mu0_rdi0_dn,
            mu0_rdo0_dn,
            mu0_rdi1_dn,
            mu0_rdo1_dn,
            mu0_wri0,
            mu0_wri1,
            mu1_rdi0_dn,
            mu1_rdo0_dn,
            mu1_rdi1_dn,
            mu1_rdo1_dn,
            mu1_wri0,
            mu1_wri1,
            hbm
        );

}