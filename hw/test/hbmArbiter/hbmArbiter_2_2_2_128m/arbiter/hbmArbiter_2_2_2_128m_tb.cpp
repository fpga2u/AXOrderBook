#include "hbmArbiter_2_2_2_128m_top.h"

#include <iostream>

using namespace hbmArbiter_2_2_2_128m;

//MU Write Request
#define MU_WR(MI, PI, A, V)\
{\
    wi_st wd;\
    wd.data.range(255, 0) = V;\
    wd.data.range(256+21-1, 256) = A;\
    if (MI==0){\
        if(PI==0){\
            mu0_wri0.write(wd); printf("MU0 write0 to A=%d V=%s\n", A, ap_uint<256>(V).to_string(16,false).c_str());\
        }else{\
            mu0_wri1.write(wd); printf("MU0 write1 to A=%d V=%s\n", A, ap_uint<256>(V).to_string(16,false).c_str());\
        }\
    }else{\
        if(PI==0){\
            mu1_wri0.write(wd); printf("MU1 write0 to A=%d V=%s\n", A, ap_uint<256>(V).to_string(16,false).c_str());\
        }else{\
            mu1_wri1.write(wd); printf("MU1 write1 to A=%d V=%s\n", A, ap_uint<256>(V).to_string(16,false).c_str());\
        }\
    }\
}

//MU Read Request
#define MU_RR(MI, PI, A)\
{\
    raddr_st rd;\
    rd.data.range(21-1, 0) = A;\
    if (MI==0){\
        if(PI==0){\
            mu0_rdi0.write(rd); printf("MU0 read0 from A=%d\n", A);\
        }else{\
            mu0_rdi1.write(rd); printf("MU0 read1 from A=%d\n", A);\
        }\
    }else{\
        if(PI==0){\
            mu1_rdi0.write(rd); printf("MU1 read0 from A=%d\n", A);\
        }else{\
            mu1_rdi1.write(rd); printf("MU1 read1 from A=%d\n", A);\
        }\
    }\
}

int main()
{
    /* register-to-host */
    unsigned int reg_guard_bgn;
    //mu0
    unsigned int mu0_rdi_nb;
    unsigned int mu0_wri_nb;
    unsigned int mu0_rdo_nb;
    unsigned int mu0_max_addr;
    //mu1
    unsigned int mu1_rdi_nb;
    unsigned int mu1_wri_nb;
    unsigned int mu1_rdo_nb;
    unsigned int mu1_max_addr;
    //hbm
    unsigned int hbm_rd_nb;
    unsigned int hbm_wr_nb;

    unsigned int reg_guard_end;

    /* mu0 */
    //rd0
    rdiStream_t mu0_rdi0("mu0_rdi0");
    rdoStream_t mu0_rdo0("mu0_rdo0");
    //rd1
    rdiStream_t mu0_rdi1("mu0_rdi1");
    rdoStream_t mu0_rdo1("mu0_rdo1");
    //wr0
    wriStream_t mu0_wri0("mu0_wri0");
    //wr1
    wriStream_t mu0_wri1("mu0_wri1");

    /* mu1 */
    //rd0
    rdiStream_t mu1_rdi0("mu1_rdi0");
    rdoStream_t mu1_rdo0("mu1_rdo0");
    //rd1
    rdiStream_t mu1_rdi1("mu1_rdi1");
    rdoStream_t mu1_rdo1("mu1_rdo1");
    //wr0
    wriStream_t mu1_wri0("mu1_wri0");
    //wr1
    wriStream_t mu1_wri1("mu1_wri1");

    //hbm
    ap_uint<256> hbm[HBM_ENTRIES_256MB_256w];
    for (int i=0; i<HBM_ENTRIES_256MB_256w;++i){
        hbm[i] = 0;
    }


    /* test write */
    MU_WR(0, 0, 0, 2);  //mu0.wr0(0, 0)
    MU_WR(0, 1, 1, 3);  //mu0.wr1(1, 1)
    MU_WR(1, 0, 0, 2);
    MU_WR(1, 1, 1, 3);

    MU_WR(0, 1, 17, 7);  //mu0.wr1(17, 7)
    MU_WR(1, 0, 23, ap_uint<256>(-1));

    for (int i=0; i<3; ++i){    //each time process one pair of mu0+mu1
        hbmArbiter_2_2_2_128m_top(
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

    assert(hbm[0]==2);
    assert(hbm[1]==3);
    assert(hbm[17]==7);
    assert(hbm[arbiter::c_mu_entries]==2);
    assert(hbm[arbiter::c_mu_entries+1]==3);
    assert(hbm[arbiter::c_mu_entries+23].to_string()==ap_uint<256>(-1).to_string());
    assert(mu0_rdi_nb==0);
    assert(mu0_wri_nb==3);
    assert(mu0_rdo_nb==0);
    assert(mu1_rdi_nb==0);
    assert(mu1_wri_nb==3);
    assert(mu1_rdo_nb==0);

    /* test read */
    MU_RR(0, 1, 0);  //mu0.rd1(0)
    MU_RR(1, 1, 0);
    for (int i=0; i<2; ++i){
        hbmArbiter_2_2_2_128m_top(
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

    assert(!mu0_rdo1.empty());
    {
        rdata_st rdat = mu0_rdo1.read();
        assert(rdat.data == 2);
    }
    assert(mu0_rdo1.empty());
    
    assert(!mu1_rdo1.empty());
    {
        rdata_st rdat = mu1_rdo1.read();
        assert(rdat.data == 2);
    }
    assert(mu1_rdo1.empty());

    MU_RR(0, 0, 1);  //mu0.rd0(1)
    MU_RR(1, 0, 1);
    for (int i=0; i<2; ++i){
        hbmArbiter_2_2_2_128m_top(
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

    assert(!mu0_rdo0.empty());
    {
        rdata_st rdat = mu0_rdo0.read();
        assert(rdat.data == 3);
    }
    assert(mu0_rdo0.empty());
    
    assert(!mu1_rdo0.empty());
    {
        rdata_st rdat = mu1_rdo0.read();
        assert(rdat.data == 3);
    }
    assert(mu1_rdo0.empty());

    MU_RR(0, 0, 17);  //mu0.rd0(17)
    MU_RR(1, 1, 23);
    for (int i=0; i<2; ++i){
        hbmArbiter_2_2_2_128m_top(
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

    assert(!mu0_rdo0.empty());
    {
        rdata_st rdat = mu0_rdo0.read();
        assert(rdat.data == 7);
    }
    assert(mu0_rdo0.empty());
    
    assert(!mu1_rdo1.empty());
    {
        rdata_st rdat = mu1_rdo1.read();
        assert(rdat.data == ap_uint<256>(-1));
    }
    assert(mu1_rdo1.empty());


    std::cout << "TEST OK!" << std::endl;

    return 0;
}
