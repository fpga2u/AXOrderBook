
#ifndef __HBMARBITER_2_2_2_128M_H__
#define __HBMARBITER_2_2_2_128M_H__


#include "ap_axi_sdata.h"
#include "hls_stream.h"

#ifndef HBM_ENTRIES_256MB_256w
#define HBM_ENTRIES_256MB_256w (((256*8/256) << 20))   //单地址256b，单bank 256MB容量=256*8*2^20bit，即8M个地址
#endif

namespace hbmArbiter_2_2_2_128m
{

typedef ap_axiu<21, 0, 0, 0> raddr_st;       //128MB = 21b
typedef hls::stream<raddr_st> rdiStream_t;
typedef ap_axiu<256, 0, 0, 0> rdata_st;
typedef hls::stream<rdata_st> rdoStream_t;

typedef ap_axiu<21+256, 0, 0, 0> wi_st;       //128MB = 21b
typedef hls::stream<wi_st> wriStream_t;

typedef ap_uint<21> raddr_t;
typedef ap_uint<256> rdata_t;
typedef ap_uint<21+256> wi_t;

class arbiter
{
public:
    static const int c_mu_entries = (1<<22);     //128MB

typedef struct cmdtype { 
    bool isRd;
    ap_uint<1> src;
    ap_uint<21> addr;
    ap_uint<256> data;
} cmd_t;
typedef ap_uint<1+1+21+256> cmd_st;

static
void cmdPack(cmd_t* cmd, cmd_st* cmd_pack)
{
#pragma HLS INLINE
    cmd_pack->range(256+21+1+1-1, 256+21+1) = cmd->isRd;
    cmd_pack->range(256+21+1-1, 256+21) = cmd->src;
    cmd_pack->range(256+21-1, 256) = cmd->addr;
    cmd_pack->range(256-1, 0) = cmd->data;
}


static
void cmdUnPack(cmd_st* cmd_pack, cmd_t* cmd)
{
#pragma HLS INLINE
    cmd->isRd = cmd_pack->range(256+21+1+1-1, 256+21+1);
    cmd->src = cmd_pack->range(256+21+1-1, 256+21);
    cmd->addr = cmd_pack->range(256+21-1, 256);
    cmd->data = cmd_pack->range(256-1, 0);
}

typedef struct acktype { 
    ap_uint<1> src;
    ap_uint<256> data;
} ack_t;
typedef ap_uint<1+256> ack_st;

static
void ackPack(ack_t* ack, ack_st* ack_pack)
{
#pragma HLS INLINE
    ack_pack->range(256+1-1, 256) = ack->src;
    ack_pack->range(256-1, 0) = ack->data;
}


static
void ackUnPack(ack_st* ack_pack, ack_t* ack)
{
#pragma HLS INLINE
    ack->src = ack_pack->range(256+1-1, 256);
    ack->data = ack_pack->range(256-1, 0);
}


template<int id>
static void mum(
    /* register-to-host */
    unsigned int& rdi_nb,
    unsigned int& wri_nb,
    unsigned int& rdo_nb,
    unsigned int& max_addr,

    /* mu */
    //rd0
    rdiStream_t& rdi0,
    rdoStream_t& rdo0,
    //rd1
    rdiStream_t& rdi1,
    rdoStream_t& rdo1,
    //wr0
    wriStream_t& wri0,
    //wr1
    wriStream_t& wri1,

    hls::stream<cmd_st>& cmd_stream,
    hls::stream<ack_st>& ack_stream
)
{
#pragma HLS INLINE off

    /* registers */
    static unsigned int r_rdi_nb=0;
    static unsigned int r_wri_nb=0;
    static unsigned int r_rdo_nb=0;
    static unsigned int r_max_addr=0;


    cmd_t cmd;
    bool cmd_rdy = false;
    if (!wri0.empty()){
        wi_st wi = wri0.read();
        cmd.addr = wi.data.range(256+21-1, 256);
        cmd.data = wi.data.range(255, 0);
        cmd.isRd = false;
        cmd.src = 0;
        cmd_rdy = true;
        r_wri_nb++;
    }else 
    if (!wri1.empty()){
        wi_st wi = wri1.read();
        cmd.addr = wi.data.range(256+21-1, 256);
        cmd.data = wi.data.range(255, 0);
        cmd.isRd = false;
        cmd.src = 1;
        cmd_rdy = true;
        r_wri_nb++;
    }else
    if (!rdi0.empty()){
        raddr_st ra = rdi0.read();
        cmd.addr = ra.data;
        cmd.data = 0;
        cmd.isRd = true;
        cmd.src = 0;
        cmd_rdy = true;
        r_rdi_nb++;
    }else
    if (!rdi1.empty()){
        raddr_st ra = rdi1.read();
        cmd.addr = ra.data;
        cmd.data = 0;
        cmd.isRd = true;
        cmd.src = 1;
        cmd_rdy = true;
        r_rdi_nb++;
    }

    if (cmd_rdy){
        cmd_st cmd_pack;
        cmdPack(&cmd, &cmd_pack);
        cmd_stream.write(cmd_pack);
        if (cmd.addr>r_max_addr) {
            r_max_addr = cmd.addr;
        }
    }

    if (!ack_stream.empty()){
        ack_st ack_pack = ack_stream.read();
        ack_t ack;
        ackUnPack(&ack_pack, &ack);

        rdata_st wb;
        wb.data = ack.data;
        wb.last = 1;
        if (ack.src==0){
            rdo0.write(wb);
        }else{
            rdo1.write(wb);
        }
        r_rdo_nb++;
    }

    rdi_nb = r_rdi_nb;
    wri_nb = r_wri_nb;
    rdo_nb = r_rdo_nb;
    max_addr = r_max_addr;


}

static void rr(
    /* register-to-host */
    unsigned int& hbm_rd_nb,
    unsigned int& hbm_wr_nb,
    //mu0
    hls::stream<cmd_st>& mu0_cmd_stream,
    hls::stream<ack_st>& mu0_ack_stream,
    //mu1
    hls::stream<cmd_st>& mu1_cmd_stream,
    hls::stream<ack_st>& mu1_ack_stream,
    //hbm
    ap_uint<256> hbm[HBM_ENTRIES_256MB_256w]
)
{
    /* registers */
    static unsigned int r_hbm_rd_nb=0;
    static unsigned int r_hbm_wr_nb=0;

    static ap_uint<1> r_rr_id = 0;
    cmd_t tempc[8];
    ack_t tempr[8];

    ap_uint<4> cmd_size;

    loop_rr:
    for (int l=0; l<2; ++l){
        #pragma HLS PIPELINE II = 1
    
        ap_uint<4> mu0_cmd_size = mu0_cmd_stream.size();    //max size = 8  //require vitis_hls>=2022.1
        ap_uint<4> mu1_cmd_size = mu1_cmd_stream.size();
        ap_uint<4> tempr_size = 0;
        
        if ((r_rr_id==0 && mu0_cmd_size) || (r_rr_id==1 && !mu1_cmd_size)){
            cmd_size = mu0_cmd_size;
            r_rr_id = 0;
        }else{
            cmd_size = mu1_cmd_size;
            r_rr_id = 1;
        }

        if (cmd_size>8)
            cmd_size = 8;

        loop_load:
        for (int i=0; i<cmd_size; ++i){
        #pragma HLS PIPELINE II = 1
        #pragma HLS loop_tripcount min=0 max=8
            cmd_st cmd_pack;
            if (r_rr_id==0){
                mu0_cmd_stream.read(cmd_pack);
            }else{
                mu1_cmd_stream.read(cmd_pack);
            }
            cmdUnPack(&cmd_pack, &tempc[i]);
        }

        loop_act:
        for (int i=0; i<cmd_size; ++i){
        #pragma HLS PIPELINE II = 8
        #pragma HLS loop_tripcount min=0 max=8
            ap_uint<23> hbm_addr;
            if (r_rr_id==0){
                hbm_addr = tempc[i].addr;
            }else{
                hbm_addr = tempc[i].addr + c_mu_entries;
            }
            if (tempc[i].isRd){
                tempr[i].data = hbm[hbm_addr];
                tempr[i].src = tempc[i].src;
                tempr_size++;
                r_hbm_rd_nb++;
            }else{
                hbm[hbm_addr] = tempc[i].data;
                r_hbm_wr_nb++;
            }
        }

        loop_wb:
        for (int i=0; i<tempr_size; ++i){
        #pragma HLS PIPELINE II = 1
        #pragma HLS loop_tripcount min=0 max=8
            ack_st ack_pack;
            ackPack(&tempr[i], &ack_pack);
            if (r_rr_id==0){
                mu0_ack_stream.write(ack_pack);
            }else{
                mu1_ack_stream.write(ack_pack);
            }
        }

        r_rr_id++;

        hbm_rd_nb = r_hbm_rd_nb;
        hbm_wr_nb = r_hbm_wr_nb;
    }

}


template<int id>
static void mainRun(
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
    rdiStream_t& mu0_rdi0,
    rdoStream_t& mu0_rdo0,
    //rd1
    rdiStream_t& mu0_rdi1,
    rdoStream_t& mu0_rdo1,
    //wr0
    wriStream_t& mu0_wri0,
    //wr1
    wriStream_t& mu0_wri1,

    /* mu1 */
    //rd0
    rdiStream_t& mu1_rdi0,
    rdoStream_t& mu1_rdo0,
    //rd1
    rdiStream_t& mu1_rdi1,
    rdoStream_t& mu1_rdo1,
    //wr0
    wriStream_t& mu1_wri0,
    //wr1
    wriStream_t& mu1_wri1,

    /* hbm */
    ap_uint<256> hbm[HBM_ENTRIES_256MB_256w]
)
{
#pragma HLS INLINE off
    static unsigned int _reg_guard_bgn = 0xA222128B;
    static unsigned int _reg_guard_end = 0xA222128E;

    //mu0 MUM
    static hls::stream<cmd_st> mu0_cmd_stream("mu0_cmd_stream");
    static hls::stream<ack_st> mu0_ack_stream("mu0_ack_stream");

#pragma HLS STREAM variable = mu0_cmd_stream depth=8      //must be <=15
#pragma HLS BIND_STORAGE variable = mu0_cmd_stream type = FIFO impl = SRL
#pragma HLS STREAM variable = mu0_ack_stream depth=8
#pragma HLS BIND_STORAGE variable = mu0_ack_stream type = FIFO impl = SRL

    //mu1 MUM
    static hls::stream<cmd_st> mu1_cmd_stream("mu1_cmd_stream");
    static hls::stream<ack_st> mu1_ack_stream("mu1_ack_stream");

#pragma HLS STREAM variable = mu1_cmd_stream depth=8      //must be <=15
#pragma HLS BIND_STORAGE variable = mu1_cmd_stream type = FIFO impl = SRL
#pragma HLS STREAM variable = mu1_ack_stream depth=8
#pragma HLS BIND_STORAGE variable = mu1_ack_stream type = FIFO impl = SRL

#pragma HLS dataflow
    mum<0>(
        mu0_rdi_nb,
        mu0_wri_nb,
        mu0_rdo_nb,
        mu0_max_addr,
        mu0_rdi0,
        mu0_rdo0,
        mu0_rdi1,
        mu0_rdo1,
        mu0_wri0,
        mu0_wri1,
        mu0_cmd_stream,
        mu0_ack_stream
    );

    mum<1>(
        mu1_rdi_nb,
        mu1_wri_nb,
        mu1_rdo_nb,
        mu1_max_addr,
        mu1_rdi0,
        mu1_rdo0,
        mu1_rdi1,
        mu1_rdo1,
        mu1_wri0,
        mu1_wri1,
        mu1_cmd_stream,
        mu1_ack_stream
    );


    rr(
        hbm_rd_nb,
        hbm_wr_nb,
        mu0_cmd_stream,
        mu0_ack_stream,
        mu1_cmd_stream,
        mu1_ack_stream,
        hbm
    );


    reg_guard_bgn = _reg_guard_bgn;
    reg_guard_end = _reg_guard_end;

}



};

} // namespace hbmArbiter_2_2_2_128m


#endif
