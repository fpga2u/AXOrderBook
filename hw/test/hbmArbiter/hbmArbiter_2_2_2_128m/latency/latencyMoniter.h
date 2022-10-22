#include "ap_axi_sdata.h"
#include "ap_int.h"
#include "hls_stream.h"


template<typename upType, typename dnType, unsigned int regGuardB, unsigned int regGuardE>
class latencyMoniter{
public:

static
void mainRun(
               hls::stream<upType>& up_in,
               hls::stream<upType>& up_out,
               hls::stream<dnType>& dn_in,
               hls::stream<dnType>& dn_out,
               unsigned int&        reg_guard_bgn,
               unsigned int&        free_cnt,
               unsigned int&        up_nb,
               unsigned int&        dn_nb,
               unsigned int&        up_last_tick,
               unsigned int&        dn_last_tick,
               unsigned int         history_id,
               unsigned int&        up_history_tick,
               unsigned int&        dn_history_tick,
               bool                 reset_reg,
               unsigned int&        reg_guard_end
               ) 
{
#pragma HLS PIPELINE II=1

    static ap_uint<32> up_tick_history[64];
    static ap_uint<32> dn_tick_history[64];
#pragma HLS BIND_STORAGE variable = up_tick_history type = ram_2p impl = lutram
#pragma HLS BIND_STORAGE variable = dn_tick_history type = ram_2p impl = lutram

    upType up_word;
    dnType dn_word;

    static ap_uint<32> reg_freeCount = 0;
    static ap_uint<32> reg_up_last_tick = 0;
    static ap_uint<32> reg_dn_last_tick = 0;
    const unsigned int guard_bgn = regGuardB;
    const unsigned int guard_end = regGuardE;
    static unsigned int reg_up_nb = 0;
    static unsigned int reg_dn_nb = 0;
    static bool reset_d1 = 0;
    static bool up_in_idle_d1 = 1;
    static bool dn_in_idle_d1 = 1;

    bool up_in_idle = up_in.empty();
    if (!up_in_idle){
        up_in.read(up_word);
        up_out.write(up_word);
        if (up_in_idle_d1) {
            reg_up_last_tick = reg_freeCount;
            up_tick_history[reg_up_nb%64] = reg_freeCount;
            reg_up_nb++;
        }
        if (up_word.last){
            up_in_idle = true;
        }
    }
    // Only reset counters when rising edge
    else if (reset_reg && !reset_d1) {
        reg_up_nb = 0;
    }

    bool dn_in_idle = dn_in.empty();
    if (!dn_in_idle){
        dn_in.read(dn_word);
        dn_out.write(dn_word);
        if (dn_in_idle_d1) {
            reg_dn_last_tick = reg_freeCount;
            dn_tick_history[reg_dn_nb%64] = reg_freeCount;
            reg_dn_nb++;
        }
        if (dn_word.last){
            dn_in_idle = true;
        }
    }
    // Only reset counters when rising edge
    else if (reset_reg && !reset_d1) {
        reg_dn_nb = 0;
    }

    free_cnt = ++reg_freeCount; //TODO: 实机被ap_vld同步后才映射到寄存器，如果卡在前面的write，则此值在寄存器界面也卡卡住了，应该有个pragma取消寄存器的ap_vld
    up_nb = reg_up_nb;
    dn_nb = reg_dn_nb;
    up_last_tick = reg_up_last_tick;
    dn_last_tick = reg_dn_last_tick;

    up_history_tick = up_tick_history[history_id%64];
    dn_history_tick = dn_tick_history[history_id%64];

    reset_d1 = reset_reg;
    up_in_idle_d1 = up_in_idle;
    dn_in_idle_d1 = dn_in_idle;

    reg_guard_bgn = guard_bgn;  //TODO: 实机的实现形式很奇怪，不是将常亮给寄存器界面，可能原因与free_cnt一样
    reg_guard_end = guard_end;
}

};

