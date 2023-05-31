#include "dbg_info.hpp"
#include "dbg_util.hpp"
#include "xv_storer_top.h"
#include "sbe_intf.hpp"

int main()
{

    signal_stream_t signal_stream_i; // Internal Stream: signal
    sbe_stream::stream_t snap_stream_i; // Internal Stream: snapGen
    /* data-to-host */
    ap_uint<DWIDTH>  host_frame_o[64];
    /* reg-to-host */
    unsigned int reg_frame_nb_o; // nb of host_frame_o
    unsigned int reg_signal_nb_o; // nb of signal_stream_i


    SBE_SSZ_instrument_snap_t_packed snapPack;
    signal_stream_word_t signal;

    
    //create snap
    SBE_SSZ_instrument_snap_t snap;
    snap.Header.SecurityIDSource = 102;
    snap.Header.MsgType = __MsgType_SSZ_INSTRUMENT_SNAP__;
    snap.Header.MsgLen = BITSIZE_SBE_SSZ_instrument_snap_t_packed / 8;
    setSecurityID(snap.Header.SecurityID, "000997");
    snap.Header.ChannelNo = 1013;
    snap.Header.ApplSeqNum = 0;
    snap.Header.TradingPhase.Code0 = 2;
    snap.Header.TradingPhase.Code1 = 0;

    snap.NumTrades = 0;
    snap.TotalVolumeTrade = 0;
    snap.TotalValueTrade = 0;
    snap.PrevClosePx = 184000;
    snap.LastPx = 0;
    snap.OpenPx = 0;
    snap.HighPx = 0;
    snap.LowPx = 0;
    snap.BidWeightPx = 0;
    snap.BidWeightSize = 0;
    snap.AskWeightPx = 0;
    snap.AskWeightSize = 0;
    snap.UpLimitPx = 20240000;
    snap.DnLimitPx = 16560000;

    snap.BidLevel[0].Price = 0;
    snap.BidLevel[0].Qty = 0;

    snap.BidLevel[1].Price = 0;
    snap.BidLevel[1].Qty = 0;

    snap.BidLevel[2].Price = 0;
    snap.BidLevel[2].Qty = 0;

    snap.BidLevel[3].Price = 0;
    snap.BidLevel[3].Qty = 0;

    snap.BidLevel[4].Price = 0;
    snap.BidLevel[4].Qty = 0;

    snap.BidLevel[5].Price = 0;
    snap.BidLevel[5].Qty = 0;

    snap.BidLevel[6].Price = 0;
    snap.BidLevel[6].Qty = 0;

    snap.BidLevel[7].Price = 0;
    snap.BidLevel[7].Qty = 0;

    snap.BidLevel[8].Price = 0;
    snap.BidLevel[8].Qty = 0;

    snap.BidLevel[9].Price = 0;
    snap.BidLevel[9].Qty = 0;

    snap.AskLevel[0].Price = 0;
    snap.AskLevel[0].Qty = 0;

    snap.AskLevel[1].Price = 0;
    snap.AskLevel[1].Qty = 0;

    snap.AskLevel[2].Price = 0;
    snap.AskLevel[2].Qty = 0;

    snap.AskLevel[3].Price = 0;
    snap.AskLevel[3].Qty = 0;

    snap.AskLevel[4].Price = 0;
    snap.AskLevel[4].Qty = 0;

    snap.AskLevel[5].Price = 0;
    snap.AskLevel[5].Qty = 0;

    snap.AskLevel[6].Price = 0;
    snap.AskLevel[6].Qty = 0;

    snap.AskLevel[7].Price = 0;
    snap.AskLevel[7].Qty = 0;

    snap.AskLevel[8].Price = 0;
    snap.AskLevel[8].Qty = 0;

    snap.AskLevel[9].Price = 0;
    snap.AskLevel[9].Qty = 0;

    snap.TransactTime = 20190311083500000;
    snap.Resv[0] = 0;
    snap.Resv[1] = 0;
    snap.Resv[2] = 0;
    snap.Resv[3] = 0;


    /* test begin */
    for (int t=0; t<3; ++t){
        printf("------ %d ------\n", t);
        int snap_n = 3;
        //n snap
        std::vector<SBE_SSZ_instrument_snap_t> sent_snaps;
        for (int n=0; n<snap_n; ++n){
            signal.user = SIGNAL_MSGTYPE;
            signal.data = __MsgType_SSZ_INSTRUMENT_SNAP__;
            signal_stream_i.write(signal);

            snap.TransactTime += 10;
            sbe_intf::SBE_SSZ_instrument_snap_t_pack(snap, snapPack);
            sbe_stream::write(snapPack, snap_stream_i);
            sent_snaps.push_back(snap);
        }
        //end of sbe_stream
        signal.user = SIGNAL_CMD;
        signal.data = CMD_STREAM_IDLE;
        signal_stream_i.write(signal);

        xv_storer_top(
            /* from OB */
            signal_stream_i,    // Internal Stream: signal
            snap_stream_i,      // Internal Stream: snapGen
            /* data-to-host */
            host_frame_o,
            /* reg-to-host */
            reg_frame_nb_o,     // nb of host_frame_o
            reg_signal_nb_o     // nb of signal_stream_i
        );

        assert(reg_frame_nb_o==snap_n);
        assert(reg_signal_nb_o==reg_frame_nb_o+(1));

        for (int i=0; i<snap_n; ++i){
            SBE_SSZ_instrument_snap_t_packed snapPack_o;
            snapPack_o = host_frame_o[i].range(DWIDTH-1, DWIDTH-BITSIZE_SBE_SSZ_instrument_snap_t_packed);
            SBE_SSZ_instrument_snap_t snap_o;
            sbe_intf::SBE_SSZ_instrument_snap_t_unpack(snapPack_o, snap_o);
            INFO("#"<< i << " msgType=" << snap_o.Header.MsgType << " TransactTime=" << snap_o.TransactTime);
            assert(snap_o==sent_snaps[i]);
        }
    }

    return 0;
}