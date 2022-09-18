#ifndef __LM_2_2_2_128M_TOP_H__
#define __LM_2_2_2_128M_TOP_H__

#include "hbmArbiter_2_2_2_128m.h"

extern "C"
void lm_2_2_2_128m_top(
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
);

#endif
