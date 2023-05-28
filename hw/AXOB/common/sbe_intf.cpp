#include "sbe_intf.hpp"
#include "endian.hpp"

void sbe_intf::price_level_t_unpack(price_level_t_packed &src,
                          price_level_t &dest)
{
#pragma HLS INLINE

    dest.Price = reverse<32>(src.range(95, 64));
    dest.Qty = reverse<64>(src.range(63, 0));
}
void sbe_intf::price_level_t_pack(price_level_t &src,
                          price_level_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(95, 64) = reverse<32>(src.Price);
    dest.range(63, 0) = reverse<64>(src.Qty);
}
void sbe_intf::SSZ_TradingPhaseCodePack_t_unpack(SSZ_TradingPhaseCodePack_t_packed &src,
                          SSZ_TradingPhaseCodePack_t &dest)
{
#pragma HLS INLINE

    dest.Code0 = src.range(7, 4);
    dest.Code1 = src.range(3, 0);
}
void sbe_intf::SSZ_TradingPhaseCodePack_t_pack(SSZ_TradingPhaseCodePack_t &src,
                          SSZ_TradingPhaseCodePack_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(7, 4) = src.Code0;
    dest.range(3, 0) = src.Code1;
}
void sbe_intf::SBE_SSZ_header_t_unpack(SBE_SSZ_header_t_packed &src,
                          SBE_SSZ_header_t &dest)
{
#pragma HLS INLINE

    dest.SecurityIDSource = src.range(191, 184);
    dest.MsgType = src.range(183, 176);
    dest.MsgLen = reverse<16>(src.range(175, 160));
    dest.SecurityID[0] = src.range(159, 152);
    dest.SecurityID[1] = src.range(151, 144);
    dest.SecurityID[2] = src.range(143, 136);
    dest.SecurityID[3] = src.range(135, 128);
    dest.SecurityID[4] = src.range(127, 120);
    dest.SecurityID[5] = src.range(119, 112);
    dest.SecurityID[6] = src.range(111, 104);
    dest.SecurityID[7] = src.range(103, 96);
    dest.SecurityID[8] = src.range(95, 88);
    dest.ChannelNo = reverse<16>(src.range(87, 72));
    dest.ApplSeqNum = reverse<64>(src.range(71, 8));
    dest.TradingPhase.Code0 = src.range(7, 4);
    dest.TradingPhase.Code1 = src.range(3, 0);
}
void sbe_intf::SBE_SSZ_header_t_pack(SBE_SSZ_header_t &src,
                          SBE_SSZ_header_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(191, 184) = src.SecurityIDSource;
    dest.range(183, 176) = src.MsgType;
    dest.range(175, 160) = reverse<16>(src.MsgLen);
    dest.range(159, 152) = src.SecurityID[0];
    dest.range(151, 144) = src.SecurityID[1];
    dest.range(143, 136) = src.SecurityID[2];
    dest.range(135, 128) = src.SecurityID[3];
    dest.range(127, 120) = src.SecurityID[4];
    dest.range(119, 112) = src.SecurityID[5];
    dest.range(111, 104) = src.SecurityID[6];
    dest.range(103, 96) = src.SecurityID[7];
    dest.range(95, 88) = src.SecurityID[8];
    dest.range(87, 72) = reverse<16>(src.ChannelNo);
    dest.range(71, 8) = reverse<64>(src.ApplSeqNum);
    dest.range(7, 4) = src.TradingPhase.Code0;
    dest.range(3, 0) = src.TradingPhase.Code1;
}
void sbe_intf::SBE_SSZ_instrument_snap_t_unpack(SBE_SSZ_instrument_snap_t_packed &src,
                          SBE_SSZ_instrument_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(2815, 2808);
    dest.Header.MsgType = src.range(2807, 2800);
    dest.Header.MsgLen = reverse<16>(src.range(2799, 2784));
    dest.Header.SecurityID[0] = src.range(2783, 2776);
    dest.Header.SecurityID[1] = src.range(2775, 2768);
    dest.Header.SecurityID[2] = src.range(2767, 2760);
    dest.Header.SecurityID[3] = src.range(2759, 2752);
    dest.Header.SecurityID[4] = src.range(2751, 2744);
    dest.Header.SecurityID[5] = src.range(2743, 2736);
    dest.Header.SecurityID[6] = src.range(2735, 2728);
    dest.Header.SecurityID[7] = src.range(2727, 2720);
    dest.Header.SecurityID[8] = src.range(2719, 2712);
    dest.Header.ChannelNo = reverse<16>(src.range(2711, 2696));
    dest.Header.ApplSeqNum = reverse<64>(src.range(2695, 2632));
    dest.Header.TradingPhase.Code0 = src.range(2631, 2628);
    dest.Header.TradingPhase.Code1 = src.range(2627, 2624);
    dest.NumTrades = reverse<64>(src.range(2623, 2560));
    dest.TotalVolumeTrade = reverse<64>(src.range(2559, 2496));
    dest.TotalValueTrade = reverse<64>(src.range(2495, 2432));
    dest.PrevClosePx = reverse<32>(src.range(2431, 2400));
    dest.LastPx = reverse<32>(src.range(2399, 2368));
    dest.OpenPx = reverse<32>(src.range(2367, 2336));
    dest.HighPx = reverse<32>(src.range(2335, 2304));
    dest.LowPx = reverse<32>(src.range(2303, 2272));
    dest.BidWeightPx = reverse<32>(src.range(2271, 2240));
    dest.BidWeightSize = reverse<64>(src.range(2239, 2176));
    dest.AskWeightPx = reverse<32>(src.range(2175, 2144));
    dest.AskWeightSize = reverse<64>(src.range(2143, 2080));
    dest.UpLimitPx = reverse<32>(src.range(2079, 2048));
    dest.DnLimitPx = reverse<32>(src.range(2047, 2016));
    dest.BidLevel[0].Price = reverse<32>(src.range(2015, 1984));
    dest.BidLevel[0].Qty = reverse<64>(src.range(1983, 1920));
    dest.BidLevel[1].Price = reverse<32>(src.range(1919, 1888));
    dest.BidLevel[1].Qty = reverse<64>(src.range(1887, 1824));
    dest.BidLevel[2].Price = reverse<32>(src.range(1823, 1792));
    dest.BidLevel[2].Qty = reverse<64>(src.range(1791, 1728));
    dest.BidLevel[3].Price = reverse<32>(src.range(1727, 1696));
    dest.BidLevel[3].Qty = reverse<64>(src.range(1695, 1632));
    dest.BidLevel[4].Price = reverse<32>(src.range(1631, 1600));
    dest.BidLevel[4].Qty = reverse<64>(src.range(1599, 1536));
    dest.BidLevel[5].Price = reverse<32>(src.range(1535, 1504));
    dest.BidLevel[5].Qty = reverse<64>(src.range(1503, 1440));
    dest.BidLevel[6].Price = reverse<32>(src.range(1439, 1408));
    dest.BidLevel[6].Qty = reverse<64>(src.range(1407, 1344));
    dest.BidLevel[7].Price = reverse<32>(src.range(1343, 1312));
    dest.BidLevel[7].Qty = reverse<64>(src.range(1311, 1248));
    dest.BidLevel[8].Price = reverse<32>(src.range(1247, 1216));
    dest.BidLevel[8].Qty = reverse<64>(src.range(1215, 1152));
    dest.BidLevel[9].Price = reverse<32>(src.range(1151, 1120));
    dest.BidLevel[9].Qty = reverse<64>(src.range(1119, 1056));
    dest.AskLevel[0].Price = reverse<32>(src.range(1055, 1024));
    dest.AskLevel[0].Qty = reverse<64>(src.range(1023, 960));
    dest.AskLevel[1].Price = reverse<32>(src.range(959, 928));
    dest.AskLevel[1].Qty = reverse<64>(src.range(927, 864));
    dest.AskLevel[2].Price = reverse<32>(src.range(863, 832));
    dest.AskLevel[2].Qty = reverse<64>(src.range(831, 768));
    dest.AskLevel[3].Price = reverse<32>(src.range(767, 736));
    dest.AskLevel[3].Qty = reverse<64>(src.range(735, 672));
    dest.AskLevel[4].Price = reverse<32>(src.range(671, 640));
    dest.AskLevel[4].Qty = reverse<64>(src.range(639, 576));
    dest.AskLevel[5].Price = reverse<32>(src.range(575, 544));
    dest.AskLevel[5].Qty = reverse<64>(src.range(543, 480));
    dest.AskLevel[6].Price = reverse<32>(src.range(479, 448));
    dest.AskLevel[6].Qty = reverse<64>(src.range(447, 384));
    dest.AskLevel[7].Price = reverse<32>(src.range(383, 352));
    dest.AskLevel[7].Qty = reverse<64>(src.range(351, 288));
    dest.AskLevel[8].Price = reverse<32>(src.range(287, 256));
    dest.AskLevel[8].Qty = reverse<64>(src.range(255, 192));
    dest.AskLevel[9].Price = reverse<32>(src.range(191, 160));
    dest.AskLevel[9].Qty = reverse<64>(src.range(159, 96));
    dest.TransactTime = reverse<64>(src.range(95, 32));
    dest.Resv[0] = src.range(31, 24);
    dest.Resv[1] = src.range(23, 16);
    dest.Resv[2] = src.range(15, 8);
    dest.Resv[3] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_instrument_snap_t_pack(SBE_SSZ_instrument_snap_t &src,
                          SBE_SSZ_instrument_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(2815, 2808) = src.Header.SecurityIDSource;
    dest.range(2807, 2800) = src.Header.MsgType;
    dest.range(2799, 2784) = reverse<16>(src.Header.MsgLen);
    dest.range(2783, 2776) = src.Header.SecurityID[0];
    dest.range(2775, 2768) = src.Header.SecurityID[1];
    dest.range(2767, 2760) = src.Header.SecurityID[2];
    dest.range(2759, 2752) = src.Header.SecurityID[3];
    dest.range(2751, 2744) = src.Header.SecurityID[4];
    dest.range(2743, 2736) = src.Header.SecurityID[5];
    dest.range(2735, 2728) = src.Header.SecurityID[6];
    dest.range(2727, 2720) = src.Header.SecurityID[7];
    dest.range(2719, 2712) = src.Header.SecurityID[8];
    dest.range(2711, 2696) = reverse<16>(src.Header.ChannelNo);
    dest.range(2695, 2632) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(2631, 2628) = src.Header.TradingPhase.Code0;
    dest.range(2627, 2624) = src.Header.TradingPhase.Code1;
    dest.range(2623, 2560) = reverse<64>(src.NumTrades);
    dest.range(2559, 2496) = reverse<64>(src.TotalVolumeTrade);
    dest.range(2495, 2432) = reverse<64>(src.TotalValueTrade);
    dest.range(2431, 2400) = reverse<32>(src.PrevClosePx);
    dest.range(2399, 2368) = reverse<32>(src.LastPx);
    dest.range(2367, 2336) = reverse<32>(src.OpenPx);
    dest.range(2335, 2304) = reverse<32>(src.HighPx);
    dest.range(2303, 2272) = reverse<32>(src.LowPx);
    dest.range(2271, 2240) = reverse<32>(src.BidWeightPx);
    dest.range(2239, 2176) = reverse<64>(src.BidWeightSize);
    dest.range(2175, 2144) = reverse<32>(src.AskWeightPx);
    dest.range(2143, 2080) = reverse<64>(src.AskWeightSize);
    dest.range(2079, 2048) = reverse<32>(src.UpLimitPx);
    dest.range(2047, 2016) = reverse<32>(src.DnLimitPx);
    dest.range(2015, 1984) = reverse<32>(src.BidLevel[0].Price);
    dest.range(1983, 1920) = reverse<64>(src.BidLevel[0].Qty);
    dest.range(1919, 1888) = reverse<32>(src.BidLevel[1].Price);
    dest.range(1887, 1824) = reverse<64>(src.BidLevel[1].Qty);
    dest.range(1823, 1792) = reverse<32>(src.BidLevel[2].Price);
    dest.range(1791, 1728) = reverse<64>(src.BidLevel[2].Qty);
    dest.range(1727, 1696) = reverse<32>(src.BidLevel[3].Price);
    dest.range(1695, 1632) = reverse<64>(src.BidLevel[3].Qty);
    dest.range(1631, 1600) = reverse<32>(src.BidLevel[4].Price);
    dest.range(1599, 1536) = reverse<64>(src.BidLevel[4].Qty);
    dest.range(1535, 1504) = reverse<32>(src.BidLevel[5].Price);
    dest.range(1503, 1440) = reverse<64>(src.BidLevel[5].Qty);
    dest.range(1439, 1408) = reverse<32>(src.BidLevel[6].Price);
    dest.range(1407, 1344) = reverse<64>(src.BidLevel[6].Qty);
    dest.range(1343, 1312) = reverse<32>(src.BidLevel[7].Price);
    dest.range(1311, 1248) = reverse<64>(src.BidLevel[7].Qty);
    dest.range(1247, 1216) = reverse<32>(src.BidLevel[8].Price);
    dest.range(1215, 1152) = reverse<64>(src.BidLevel[8].Qty);
    dest.range(1151, 1120) = reverse<32>(src.BidLevel[9].Price);
    dest.range(1119, 1056) = reverse<64>(src.BidLevel[9].Qty);
    dest.range(1055, 1024) = reverse<32>(src.AskLevel[0].Price);
    dest.range(1023, 960) = reverse<64>(src.AskLevel[0].Qty);
    dest.range(959, 928) = reverse<32>(src.AskLevel[1].Price);
    dest.range(927, 864) = reverse<64>(src.AskLevel[1].Qty);
    dest.range(863, 832) = reverse<32>(src.AskLevel[2].Price);
    dest.range(831, 768) = reverse<64>(src.AskLevel[2].Qty);
    dest.range(767, 736) = reverse<32>(src.AskLevel[3].Price);
    dest.range(735, 672) = reverse<64>(src.AskLevel[3].Qty);
    dest.range(671, 640) = reverse<32>(src.AskLevel[4].Price);
    dest.range(639, 576) = reverse<64>(src.AskLevel[4].Qty);
    dest.range(575, 544) = reverse<32>(src.AskLevel[5].Price);
    dest.range(543, 480) = reverse<64>(src.AskLevel[5].Qty);
    dest.range(479, 448) = reverse<32>(src.AskLevel[6].Price);
    dest.range(447, 384) = reverse<64>(src.AskLevel[6].Qty);
    dest.range(383, 352) = reverse<32>(src.AskLevel[7].Price);
    dest.range(351, 288) = reverse<64>(src.AskLevel[7].Qty);
    dest.range(287, 256) = reverse<32>(src.AskLevel[8].Price);
    dest.range(255, 192) = reverse<64>(src.AskLevel[8].Qty);
    dest.range(191, 160) = reverse<32>(src.AskLevel[9].Price);
    dest.range(159, 96) = reverse<64>(src.AskLevel[9].Qty);
    dest.range(95, 32) = reverse<64>(src.TransactTime);
    dest.range(31, 24) = src.Resv[0];
    dest.range(23, 16) = src.Resv[1];
    dest.range(15, 8) = src.Resv[2];
    dest.range(7, 0) = src.Resv[3];
}