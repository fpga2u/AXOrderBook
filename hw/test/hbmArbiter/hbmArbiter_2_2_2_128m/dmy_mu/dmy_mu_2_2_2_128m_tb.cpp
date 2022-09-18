#include "dmy_mu_2_2_2_128m_top.h"

using namespace hbmArbiter_2_2_2_128m;

int main()
{
    unsigned int reg_guard_bgn;

    unsigned int wk_nb;
    unsigned int min_addr;
    unsigned int max_addr;
    unsigned int min_data;
    unsigned int gap_nb;

    unsigned int rdo0_nb;
    unsigned int rdo1_nb;
    unsigned int rd0err_nb;
    unsigned int rd1err_nb;

    unsigned int reg_guard_end;

    //rd0
    hbmArbiter_2_2_2_128m::rdiStream_t rdi0("rdi0");
    hbmArbiter_2_2_2_128m::rdoStream_t rdo0("rdo0");
    //rd1
    hbmArbiter_2_2_2_128m::rdiStream_t rdi1("rdi1");
    hbmArbiter_2_2_2_128m::rdoStream_t rdo1("rdo1");
    //wr0
    hbmArbiter_2_2_2_128m::wriStream_t wri0("wri0");
    //wr1
    hbmArbiter_2_2_2_128m::wriStream_t wri1("wri1");


    wk_nb = 16;

    min_addr = 0;
    max_addr = 128;

    min_data = 100;

    gap_nb = 16;

    dmy_mu_2_2_2_128m_top(
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

    ap_uint<256> mem[1024];

    while (!wri0.empty()){
        wi_st wi = wri0.read();
        mem[wi.data.range(256+21-1, 256)] = wi.data.range(255, 0);
        assert(wi.data.range(255, 0) == wi.data.range(256+21-1, 256) + min_data);
    }

    while (!wri1.empty()){
        wi_st wi = wri1.read();
        mem[wi.data.range(256+21-1, 256)] = wi.data.range(255, 0);
        assert(wi.data.range(255, 0) == wi.data.range(256+21-1, 256) + min_data);
    }


    while (!rdi0.empty()){
        raddr_st ra = rdi0.read();
        rdata_st rdat;
        rdat.data = mem[ra.data];
        rdo0.write(rdat);
    }

    while (!rdi1.empty()){
        raddr_st ra = rdi1.read();
        rdata_st rdat;
        rdat.data = mem[ra.data];
        rdo1.write(rdat);
    }

    min_data = 200;
    while (!rdo0.empty() && !rdo1.empty())
    {
        dmy_mu_2_2_2_128m_top(
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
    }

    while (!wri0.empty()){
        wi_st wi = wri0.read();
        mem[wi.data.range(256+21-1, 256)] = wi.data.range(255, 0);
        assert(wi.data.range(255, 0) == wi.data.range(256+21-1, 256) + min_data);
    }

    while (!wri1.empty()){
        wi_st wi = wri1.read();
        mem[wi.data.range(256+21-1, 256)] = wi.data.range(255, 0);
        assert(wi.data.range(255, 0) == wi.data.range(256+21-1, 256) + min_data);
    }

    while (!rdi0.empty()){
        raddr_st ra = rdi0.read();
    }

    while (!rdi1.empty()){
        raddr_st ra = rdi1.read();
    }

    assert(rdo0_nb==wk_nb);
    assert(rdo1_nb==wk_nb);
    assert(rd0err_nb==0);
    assert(rd1err_nb==0);
    

    std::cout << "TEST OK!" << std::endl;
    return 0;
}