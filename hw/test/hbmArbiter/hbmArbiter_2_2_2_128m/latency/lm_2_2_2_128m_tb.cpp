#include "lm_2_2_2_128m_top.h"

using namespace hbmArbiter_2_2_2_128m;


int main()
{
    rdiStream_t          up_in;
    rdiStream_t          up_out;
    rdoStream_t          dn_in;
    rdoStream_t          dn_out;
    unsigned int         reg_guard_bgn;
    unsigned int         reg_guard_end;
    unsigned int         free_cnt;
    unsigned int         up_nb;
    unsigned int         dn_nb;
    unsigned int         up_last_tick;
    unsigned int         dn_last_tick;
    unsigned int         history_id = 0;
    unsigned int         up_history_tick;
    unsigned int         dn_history_tick;
    bool                 reset_reg = false;

    raddr_st raddr;
    raddr.data = 10;
    raddr.last = 1;
    up_in.write(raddr);
    raddr.data = 11;
    raddr.last = 1;
    up_in.write(raddr);

    rdata_st rdat;
    rdat.data = 20;
    rdat.last = 1;
    dn_in.write(rdat);
    rdat.data = 21;
    rdat.last = 1;
    dn_in.write(rdat);

    for (int i=0; i<2; ++i){
        lm_2_2_2_128m_top(
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
            reg_guard_end,
            up_in,
            up_out,
            dn_in,
            dn_out
        );
    }

    assert(up_out.size()==2);
    raddr = up_out.read();
    assert(raddr.data==10);
    raddr = up_out.read();
    assert(raddr.data==11);

    assert(dn_out.size()==2);
    rdat = dn_out.read();
    assert(rdat.data==20);
    rdat = dn_out.read();
    assert(rdat.data==21);

    assert(up_nb==2);
    assert(dn_nb==2);

    printf("up_last_tick=%d  dn_last_tick=%d\n", up_last_tick, dn_last_tick);
    printf("up_history_tick[%d]=%d  dn_history_tick[%d]=%d\n", history_id, up_history_tick, history_id, dn_history_tick);

    assert(up_history_tick < up_last_tick);
    assert(dn_history_tick < dn_last_tick);

    std::cout << "TEST OK!" << std::endl;
    return 0;

}

