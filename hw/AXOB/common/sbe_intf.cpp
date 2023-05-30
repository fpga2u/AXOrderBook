#include "sbe_intf.hpp"
#include "endian.hpp"



void sbe_intf::price_level_t_unpack(price_level_t_packed &src,
                          price_level_t &dest)
{
#pragma HLS INLINE

    dest.Price = SBE_ENDIAN::reverse<32>(src.range(95, 64));
    dest.Qty = SBE_ENDIAN::reverse<64>(src.range(63, 0));
}
void sbe_intf::price_level_t_pack(price_level_t &src,
                          price_level_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(95, 64) = SBE_ENDIAN::reverse<32>(src.Price);
    dest.range(63, 0) = SBE_ENDIAN::reverse<64>(src.Qty);
}


void sbe_intf::QtyQueue_level_t_unpack(QtyQueue_level_t_packed &src,
                          QtyQueue_level_t &dest)
{
#pragma HLS INLINE

    dest.NoOrders = src.range(807, 800);
    dest.QtyQueue[0] = SBE_ENDIAN::reverse<16>(src.range(799, 784));
    dest.QtyQueue[1] = SBE_ENDIAN::reverse<16>(src.range(783, 768));
    dest.QtyQueue[2] = SBE_ENDIAN::reverse<16>(src.range(767, 752));
    dest.QtyQueue[3] = SBE_ENDIAN::reverse<16>(src.range(751, 736));
    dest.QtyQueue[4] = SBE_ENDIAN::reverse<16>(src.range(735, 720));
    dest.QtyQueue[5] = SBE_ENDIAN::reverse<16>(src.range(719, 704));
    dest.QtyQueue[6] = SBE_ENDIAN::reverse<16>(src.range(703, 688));
    dest.QtyQueue[7] = SBE_ENDIAN::reverse<16>(src.range(687, 672));
    dest.QtyQueue[8] = SBE_ENDIAN::reverse<16>(src.range(671, 656));
    dest.QtyQueue[9] = SBE_ENDIAN::reverse<16>(src.range(655, 640));
    dest.QtyQueue[10] = SBE_ENDIAN::reverse<16>(src.range(639, 624));
    dest.QtyQueue[11] = SBE_ENDIAN::reverse<16>(src.range(623, 608));
    dest.QtyQueue[12] = SBE_ENDIAN::reverse<16>(src.range(607, 592));
    dest.QtyQueue[13] = SBE_ENDIAN::reverse<16>(src.range(591, 576));
    dest.QtyQueue[14] = SBE_ENDIAN::reverse<16>(src.range(575, 560));
    dest.QtyQueue[15] = SBE_ENDIAN::reverse<16>(src.range(559, 544));
    dest.QtyQueue[16] = SBE_ENDIAN::reverse<16>(src.range(543, 528));
    dest.QtyQueue[17] = SBE_ENDIAN::reverse<16>(src.range(527, 512));
    dest.QtyQueue[18] = SBE_ENDIAN::reverse<16>(src.range(511, 496));
    dest.QtyQueue[19] = SBE_ENDIAN::reverse<16>(src.range(495, 480));
    dest.QtyQueue[20] = SBE_ENDIAN::reverse<16>(src.range(479, 464));
    dest.QtyQueue[21] = SBE_ENDIAN::reverse<16>(src.range(463, 448));
    dest.QtyQueue[22] = SBE_ENDIAN::reverse<16>(src.range(447, 432));
    dest.QtyQueue[23] = SBE_ENDIAN::reverse<16>(src.range(431, 416));
    dest.QtyQueue[24] = SBE_ENDIAN::reverse<16>(src.range(415, 400));
    dest.QtyQueue[25] = SBE_ENDIAN::reverse<16>(src.range(399, 384));
    dest.QtyQueue[26] = SBE_ENDIAN::reverse<16>(src.range(383, 368));
    dest.QtyQueue[27] = SBE_ENDIAN::reverse<16>(src.range(367, 352));
    dest.QtyQueue[28] = SBE_ENDIAN::reverse<16>(src.range(351, 336));
    dest.QtyQueue[29] = SBE_ENDIAN::reverse<16>(src.range(335, 320));
    dest.QtyQueue[30] = SBE_ENDIAN::reverse<16>(src.range(319, 304));
    dest.QtyQueue[31] = SBE_ENDIAN::reverse<16>(src.range(303, 288));
    dest.QtyQueue[32] = SBE_ENDIAN::reverse<16>(src.range(287, 272));
    dest.QtyQueue[33] = SBE_ENDIAN::reverse<16>(src.range(271, 256));
    dest.QtyQueue[34] = SBE_ENDIAN::reverse<16>(src.range(255, 240));
    dest.QtyQueue[35] = SBE_ENDIAN::reverse<16>(src.range(239, 224));
    dest.QtyQueue[36] = SBE_ENDIAN::reverse<16>(src.range(223, 208));
    dest.QtyQueue[37] = SBE_ENDIAN::reverse<16>(src.range(207, 192));
    dest.QtyQueue[38] = SBE_ENDIAN::reverse<16>(src.range(191, 176));
    dest.QtyQueue[39] = SBE_ENDIAN::reverse<16>(src.range(175, 160));
    dest.QtyQueue[40] = SBE_ENDIAN::reverse<16>(src.range(159, 144));
    dest.QtyQueue[41] = SBE_ENDIAN::reverse<16>(src.range(143, 128));
    dest.QtyQueue[42] = SBE_ENDIAN::reverse<16>(src.range(127, 112));
    dest.QtyQueue[43] = SBE_ENDIAN::reverse<16>(src.range(111, 96));
    dest.QtyQueue[44] = SBE_ENDIAN::reverse<16>(src.range(95, 80));
    dest.QtyQueue[45] = SBE_ENDIAN::reverse<16>(src.range(79, 64));
    dest.QtyQueue[46] = SBE_ENDIAN::reverse<16>(src.range(63, 48));
    dest.QtyQueue[47] = SBE_ENDIAN::reverse<16>(src.range(47, 32));
    dest.QtyQueue[48] = SBE_ENDIAN::reverse<16>(src.range(31, 16));
    dest.QtyQueue[49] = SBE_ENDIAN::reverse<16>(src.range(15, 0));
}
void sbe_intf::QtyQueue_level_t_pack(QtyQueue_level_t &src,
                          QtyQueue_level_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(807, 800) = src.NoOrders;
    dest.range(799, 784) = SBE_ENDIAN::reverse<16>(src.QtyQueue[0]);
    dest.range(783, 768) = SBE_ENDIAN::reverse<16>(src.QtyQueue[1]);
    dest.range(767, 752) = SBE_ENDIAN::reverse<16>(src.QtyQueue[2]);
    dest.range(751, 736) = SBE_ENDIAN::reverse<16>(src.QtyQueue[3]);
    dest.range(735, 720) = SBE_ENDIAN::reverse<16>(src.QtyQueue[4]);
    dest.range(719, 704) = SBE_ENDIAN::reverse<16>(src.QtyQueue[5]);
    dest.range(703, 688) = SBE_ENDIAN::reverse<16>(src.QtyQueue[6]);
    dest.range(687, 672) = SBE_ENDIAN::reverse<16>(src.QtyQueue[7]);
    dest.range(671, 656) = SBE_ENDIAN::reverse<16>(src.QtyQueue[8]);
    dest.range(655, 640) = SBE_ENDIAN::reverse<16>(src.QtyQueue[9]);
    dest.range(639, 624) = SBE_ENDIAN::reverse<16>(src.QtyQueue[10]);
    dest.range(623, 608) = SBE_ENDIAN::reverse<16>(src.QtyQueue[11]);
    dest.range(607, 592) = SBE_ENDIAN::reverse<16>(src.QtyQueue[12]);
    dest.range(591, 576) = SBE_ENDIAN::reverse<16>(src.QtyQueue[13]);
    dest.range(575, 560) = SBE_ENDIAN::reverse<16>(src.QtyQueue[14]);
    dest.range(559, 544) = SBE_ENDIAN::reverse<16>(src.QtyQueue[15]);
    dest.range(543, 528) = SBE_ENDIAN::reverse<16>(src.QtyQueue[16]);
    dest.range(527, 512) = SBE_ENDIAN::reverse<16>(src.QtyQueue[17]);
    dest.range(511, 496) = SBE_ENDIAN::reverse<16>(src.QtyQueue[18]);
    dest.range(495, 480) = SBE_ENDIAN::reverse<16>(src.QtyQueue[19]);
    dest.range(479, 464) = SBE_ENDIAN::reverse<16>(src.QtyQueue[20]);
    dest.range(463, 448) = SBE_ENDIAN::reverse<16>(src.QtyQueue[21]);
    dest.range(447, 432) = SBE_ENDIAN::reverse<16>(src.QtyQueue[22]);
    dest.range(431, 416) = SBE_ENDIAN::reverse<16>(src.QtyQueue[23]);
    dest.range(415, 400) = SBE_ENDIAN::reverse<16>(src.QtyQueue[24]);
    dest.range(399, 384) = SBE_ENDIAN::reverse<16>(src.QtyQueue[25]);
    dest.range(383, 368) = SBE_ENDIAN::reverse<16>(src.QtyQueue[26]);
    dest.range(367, 352) = SBE_ENDIAN::reverse<16>(src.QtyQueue[27]);
    dest.range(351, 336) = SBE_ENDIAN::reverse<16>(src.QtyQueue[28]);
    dest.range(335, 320) = SBE_ENDIAN::reverse<16>(src.QtyQueue[29]);
    dest.range(319, 304) = SBE_ENDIAN::reverse<16>(src.QtyQueue[30]);
    dest.range(303, 288) = SBE_ENDIAN::reverse<16>(src.QtyQueue[31]);
    dest.range(287, 272) = SBE_ENDIAN::reverse<16>(src.QtyQueue[32]);
    dest.range(271, 256) = SBE_ENDIAN::reverse<16>(src.QtyQueue[33]);
    dest.range(255, 240) = SBE_ENDIAN::reverse<16>(src.QtyQueue[34]);
    dest.range(239, 224) = SBE_ENDIAN::reverse<16>(src.QtyQueue[35]);
    dest.range(223, 208) = SBE_ENDIAN::reverse<16>(src.QtyQueue[36]);
    dest.range(207, 192) = SBE_ENDIAN::reverse<16>(src.QtyQueue[37]);
    dest.range(191, 176) = SBE_ENDIAN::reverse<16>(src.QtyQueue[38]);
    dest.range(175, 160) = SBE_ENDIAN::reverse<16>(src.QtyQueue[39]);
    dest.range(159, 144) = SBE_ENDIAN::reverse<16>(src.QtyQueue[40]);
    dest.range(143, 128) = SBE_ENDIAN::reverse<16>(src.QtyQueue[41]);
    dest.range(127, 112) = SBE_ENDIAN::reverse<16>(src.QtyQueue[42]);
    dest.range(111, 96) = SBE_ENDIAN::reverse<16>(src.QtyQueue[43]);
    dest.range(95, 80) = SBE_ENDIAN::reverse<16>(src.QtyQueue[44]);
    dest.range(79, 64) = SBE_ENDIAN::reverse<16>(src.QtyQueue[45]);
    dest.range(63, 48) = SBE_ENDIAN::reverse<16>(src.QtyQueue[46]);
    dest.range(47, 32) = SBE_ENDIAN::reverse<16>(src.QtyQueue[47]);
    dest.range(31, 16) = SBE_ENDIAN::reverse<16>(src.QtyQueue[48]);
    dest.range(15, 0) = SBE_ENDIAN::reverse<16>(src.QtyQueue[49]);
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
    dest.MsgLen = SBE_ENDIAN::reverse<16>(src.range(175, 160));
    dest.SecurityID[0] = src.range(159, 152);
    dest.SecurityID[1] = src.range(151, 144);
    dest.SecurityID[2] = src.range(143, 136);
    dest.SecurityID[3] = src.range(135, 128);
    dest.SecurityID[4] = src.range(127, 120);
    dest.SecurityID[5] = src.range(119, 112);
    dest.SecurityID[6] = src.range(111, 104);
    dest.SecurityID[7] = src.range(103, 96);
    dest.SecurityID[8] = src.range(95, 88);
    dest.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(87, 72));
    dest.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(71, 8));
    dest.TradingPhase.Code0 = src.range(7, 4);
    dest.TradingPhase.Code1 = src.range(3, 0);
}
void sbe_intf::SBE_SSZ_header_t_pack(SBE_SSZ_header_t &src,
                          SBE_SSZ_header_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(191, 184) = src.SecurityIDSource;
    dest.range(183, 176) = src.MsgType;
    dest.range(175, 160) = SBE_ENDIAN::reverse<16>(src.MsgLen);
    dest.range(159, 152) = src.SecurityID[0];
    dest.range(151, 144) = src.SecurityID[1];
    dest.range(143, 136) = src.SecurityID[2];
    dest.range(135, 128) = src.SecurityID[3];
    dest.range(127, 120) = src.SecurityID[4];
    dest.range(119, 112) = src.SecurityID[5];
    dest.range(111, 104) = src.SecurityID[6];
    dest.range(103, 96) = src.SecurityID[7];
    dest.range(95, 88) = src.SecurityID[8];
    dest.range(87, 72) = SBE_ENDIAN::reverse<16>(src.ChannelNo);
    dest.range(71, 8) = SBE_ENDIAN::reverse<64>(src.ApplSeqNum);
    dest.range(7, 4) = src.TradingPhase.Code0;
    dest.range(3, 0) = src.TradingPhase.Code1;
}


void sbe_intf::SBE_SSZ_instrument_snap_t_unpack(SBE_SSZ_instrument_snap_t_packed &src,
                          SBE_SSZ_instrument_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(2815, 2808);
    dest.Header.MsgType = src.range(2807, 2800);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(2799, 2784));
    dest.Header.SecurityID[0] = src.range(2783, 2776);
    dest.Header.SecurityID[1] = src.range(2775, 2768);
    dest.Header.SecurityID[2] = src.range(2767, 2760);
    dest.Header.SecurityID[3] = src.range(2759, 2752);
    dest.Header.SecurityID[4] = src.range(2751, 2744);
    dest.Header.SecurityID[5] = src.range(2743, 2736);
    dest.Header.SecurityID[6] = src.range(2735, 2728);
    dest.Header.SecurityID[7] = src.range(2727, 2720);
    dest.Header.SecurityID[8] = src.range(2719, 2712);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(2711, 2696));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(2695, 2632));
    dest.Header.TradingPhase.Code0 = src.range(2631, 2628);
    dest.Header.TradingPhase.Code1 = src.range(2627, 2624);
    dest.NumTrades = SBE_ENDIAN::reverse<64>(src.range(2623, 2560));
    dest.TotalVolumeTrade = SBE_ENDIAN::reverse<64>(src.range(2559, 2496));
    dest.TotalValueTrade = SBE_ENDIAN::reverse<64>(src.range(2495, 2432));
    dest.PrevClosePx = SBE_ENDIAN::reverse<32>(src.range(2431, 2400));
    dest.LastPx = SBE_ENDIAN::reverse<32>(src.range(2399, 2368));
    dest.OpenPx = SBE_ENDIAN::reverse<32>(src.range(2367, 2336));
    dest.HighPx = SBE_ENDIAN::reverse<32>(src.range(2335, 2304));
    dest.LowPx = SBE_ENDIAN::reverse<32>(src.range(2303, 2272));
    dest.BidWeightPx = SBE_ENDIAN::reverse<32>(src.range(2271, 2240));
    dest.BidWeightSize = SBE_ENDIAN::reverse<64>(src.range(2239, 2176));
    dest.AskWeightPx = SBE_ENDIAN::reverse<32>(src.range(2175, 2144));
    dest.AskWeightSize = SBE_ENDIAN::reverse<64>(src.range(2143, 2080));
    dest.UpLimitPx = SBE_ENDIAN::reverse<32>(src.range(2079, 2048));
    dest.DnLimitPx = SBE_ENDIAN::reverse<32>(src.range(2047, 2016));
    dest.BidLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(2015, 1984));
    dest.BidLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(1983, 1920));
    dest.BidLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(1919, 1888));
    dest.BidLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(1887, 1824));
    dest.BidLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(1823, 1792));
    dest.BidLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(1791, 1728));
    dest.BidLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(1727, 1696));
    dest.BidLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(1695, 1632));
    dest.BidLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(1631, 1600));
    dest.BidLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(1599, 1536));
    dest.BidLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(1535, 1504));
    dest.BidLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(1503, 1440));
    dest.BidLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(1439, 1408));
    dest.BidLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(1407, 1344));
    dest.BidLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(1343, 1312));
    dest.BidLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(1311, 1248));
    dest.BidLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(1247, 1216));
    dest.BidLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(1215, 1152));
    dest.BidLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(1151, 1120));
    dest.BidLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(1119, 1056));
    dest.AskLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(1055, 1024));
    dest.AskLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(1023, 960));
    dest.AskLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(959, 928));
    dest.AskLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(927, 864));
    dest.AskLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(863, 832));
    dest.AskLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(831, 768));
    dest.AskLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(767, 736));
    dest.AskLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(735, 672));
    dest.AskLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(671, 640));
    dest.AskLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(639, 576));
    dest.AskLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(575, 544));
    dest.AskLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(543, 480));
    dest.AskLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(479, 448));
    dest.AskLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(447, 384));
    dest.AskLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(383, 352));
    dest.AskLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(351, 288));
    dest.AskLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(287, 256));
    dest.AskLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(255, 192));
    dest.AskLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(191, 160));
    dest.AskLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(159, 96));
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(95, 32));
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
    dest.range(2799, 2784) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(2783, 2776) = src.Header.SecurityID[0];
    dest.range(2775, 2768) = src.Header.SecurityID[1];
    dest.range(2767, 2760) = src.Header.SecurityID[2];
    dest.range(2759, 2752) = src.Header.SecurityID[3];
    dest.range(2751, 2744) = src.Header.SecurityID[4];
    dest.range(2743, 2736) = src.Header.SecurityID[5];
    dest.range(2735, 2728) = src.Header.SecurityID[6];
    dest.range(2727, 2720) = src.Header.SecurityID[7];
    dest.range(2719, 2712) = src.Header.SecurityID[8];
    dest.range(2711, 2696) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(2695, 2632) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(2631, 2628) = src.Header.TradingPhase.Code0;
    dest.range(2627, 2624) = src.Header.TradingPhase.Code1;
    dest.range(2623, 2560) = SBE_ENDIAN::reverse<64>(src.NumTrades);
    dest.range(2559, 2496) = SBE_ENDIAN::reverse<64>(src.TotalVolumeTrade);
    dest.range(2495, 2432) = SBE_ENDIAN::reverse<64>(src.TotalValueTrade);
    dest.range(2431, 2400) = SBE_ENDIAN::reverse<32>(src.PrevClosePx);
    dest.range(2399, 2368) = SBE_ENDIAN::reverse<32>(src.LastPx);
    dest.range(2367, 2336) = SBE_ENDIAN::reverse<32>(src.OpenPx);
    dest.range(2335, 2304) = SBE_ENDIAN::reverse<32>(src.HighPx);
    dest.range(2303, 2272) = SBE_ENDIAN::reverse<32>(src.LowPx);
    dest.range(2271, 2240) = SBE_ENDIAN::reverse<32>(src.BidWeightPx);
    dest.range(2239, 2176) = SBE_ENDIAN::reverse<64>(src.BidWeightSize);
    dest.range(2175, 2144) = SBE_ENDIAN::reverse<32>(src.AskWeightPx);
    dest.range(2143, 2080) = SBE_ENDIAN::reverse<64>(src.AskWeightSize);
    dest.range(2079, 2048) = SBE_ENDIAN::reverse<32>(src.UpLimitPx);
    dest.range(2047, 2016) = SBE_ENDIAN::reverse<32>(src.DnLimitPx);
    dest.range(2015, 1984) = SBE_ENDIAN::reverse<32>(src.BidLevel[0].Price);
    dest.range(1983, 1920) = SBE_ENDIAN::reverse<64>(src.BidLevel[0].Qty);
    dest.range(1919, 1888) = SBE_ENDIAN::reverse<32>(src.BidLevel[1].Price);
    dest.range(1887, 1824) = SBE_ENDIAN::reverse<64>(src.BidLevel[1].Qty);
    dest.range(1823, 1792) = SBE_ENDIAN::reverse<32>(src.BidLevel[2].Price);
    dest.range(1791, 1728) = SBE_ENDIAN::reverse<64>(src.BidLevel[2].Qty);
    dest.range(1727, 1696) = SBE_ENDIAN::reverse<32>(src.BidLevel[3].Price);
    dest.range(1695, 1632) = SBE_ENDIAN::reverse<64>(src.BidLevel[3].Qty);
    dest.range(1631, 1600) = SBE_ENDIAN::reverse<32>(src.BidLevel[4].Price);
    dest.range(1599, 1536) = SBE_ENDIAN::reverse<64>(src.BidLevel[4].Qty);
    dest.range(1535, 1504) = SBE_ENDIAN::reverse<32>(src.BidLevel[5].Price);
    dest.range(1503, 1440) = SBE_ENDIAN::reverse<64>(src.BidLevel[5].Qty);
    dest.range(1439, 1408) = SBE_ENDIAN::reverse<32>(src.BidLevel[6].Price);
    dest.range(1407, 1344) = SBE_ENDIAN::reverse<64>(src.BidLevel[6].Qty);
    dest.range(1343, 1312) = SBE_ENDIAN::reverse<32>(src.BidLevel[7].Price);
    dest.range(1311, 1248) = SBE_ENDIAN::reverse<64>(src.BidLevel[7].Qty);
    dest.range(1247, 1216) = SBE_ENDIAN::reverse<32>(src.BidLevel[8].Price);
    dest.range(1215, 1152) = SBE_ENDIAN::reverse<64>(src.BidLevel[8].Qty);
    dest.range(1151, 1120) = SBE_ENDIAN::reverse<32>(src.BidLevel[9].Price);
    dest.range(1119, 1056) = SBE_ENDIAN::reverse<64>(src.BidLevel[9].Qty);
    dest.range(1055, 1024) = SBE_ENDIAN::reverse<32>(src.AskLevel[0].Price);
    dest.range(1023, 960) = SBE_ENDIAN::reverse<64>(src.AskLevel[0].Qty);
    dest.range(959, 928) = SBE_ENDIAN::reverse<32>(src.AskLevel[1].Price);
    dest.range(927, 864) = SBE_ENDIAN::reverse<64>(src.AskLevel[1].Qty);
    dest.range(863, 832) = SBE_ENDIAN::reverse<32>(src.AskLevel[2].Price);
    dest.range(831, 768) = SBE_ENDIAN::reverse<64>(src.AskLevel[2].Qty);
    dest.range(767, 736) = SBE_ENDIAN::reverse<32>(src.AskLevel[3].Price);
    dest.range(735, 672) = SBE_ENDIAN::reverse<64>(src.AskLevel[3].Qty);
    dest.range(671, 640) = SBE_ENDIAN::reverse<32>(src.AskLevel[4].Price);
    dest.range(639, 576) = SBE_ENDIAN::reverse<64>(src.AskLevel[4].Qty);
    dest.range(575, 544) = SBE_ENDIAN::reverse<32>(src.AskLevel[5].Price);
    dest.range(543, 480) = SBE_ENDIAN::reverse<64>(src.AskLevel[5].Qty);
    dest.range(479, 448) = SBE_ENDIAN::reverse<32>(src.AskLevel[6].Price);
    dest.range(447, 384) = SBE_ENDIAN::reverse<64>(src.AskLevel[6].Qty);
    dest.range(383, 352) = SBE_ENDIAN::reverse<32>(src.AskLevel[7].Price);
    dest.range(351, 288) = SBE_ENDIAN::reverse<64>(src.AskLevel[7].Qty);
    dest.range(287, 256) = SBE_ENDIAN::reverse<32>(src.AskLevel[8].Price);
    dest.range(255, 192) = SBE_ENDIAN::reverse<64>(src.AskLevel[8].Qty);
    dest.range(191, 160) = SBE_ENDIAN::reverse<32>(src.AskLevel[9].Price);
    dest.range(159, 96) = SBE_ENDIAN::reverse<64>(src.AskLevel[9].Qty);
    dest.range(95, 32) = SBE_ENDIAN::reverse<64>(src.TransactTime);
    dest.range(31, 24) = src.Resv[0];
    dest.range(23, 16) = src.Resv[1];
    dest.range(15, 8) = src.Resv[2];
    dest.range(7, 0) = src.Resv[3];
}


void sbe_intf::SBE_SSZ_index_snap_t_unpack(SBE_SSZ_index_snap_t_packed &src,
                          SBE_SSZ_index_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(767, 760);
    dest.Header.MsgType = src.range(759, 752);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(751, 736));
    dest.Header.SecurityID[0] = src.range(735, 728);
    dest.Header.SecurityID[1] = src.range(727, 720);
    dest.Header.SecurityID[2] = src.range(719, 712);
    dest.Header.SecurityID[3] = src.range(711, 704);
    dest.Header.SecurityID[4] = src.range(703, 696);
    dest.Header.SecurityID[5] = src.range(695, 688);
    dest.Header.SecurityID[6] = src.range(687, 680);
    dest.Header.SecurityID[7] = src.range(679, 672);
    dest.Header.SecurityID[8] = src.range(671, 664);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(663, 648));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(647, 584));
    dest.Header.TradingPhase.Code0 = src.range(583, 580);
    dest.Header.TradingPhase.Code1 = src.range(579, 576);
    dest.NumTrades = SBE_ENDIAN::reverse<64>(src.range(575, 512));
    dest.TotalVolumeTrade = SBE_ENDIAN::reverse<64>(src.range(511, 448));
    dest.TotalValueTrade = SBE_ENDIAN::reverse<64>(src.range(447, 384));
    dest.PrevClosePx = SBE_ENDIAN::reverse<64>(src.range(383, 320));
    dest.LastPx = SBE_ENDIAN::reverse<64>(src.range(319, 256));
    dest.OpenPx = SBE_ENDIAN::reverse<64>(src.range(255, 192));
    dest.HighPx = SBE_ENDIAN::reverse<64>(src.range(191, 128));
    dest.LowPx = SBE_ENDIAN::reverse<64>(src.range(127, 64));
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(63, 0));
}
void sbe_intf::SBE_SSZ_index_snap_t_pack(SBE_SSZ_index_snap_t &src,
                          SBE_SSZ_index_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(767, 760) = src.Header.SecurityIDSource;
    dest.range(759, 752) = src.Header.MsgType;
    dest.range(751, 736) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(735, 728) = src.Header.SecurityID[0];
    dest.range(727, 720) = src.Header.SecurityID[1];
    dest.range(719, 712) = src.Header.SecurityID[2];
    dest.range(711, 704) = src.Header.SecurityID[3];
    dest.range(703, 696) = src.Header.SecurityID[4];
    dest.range(695, 688) = src.Header.SecurityID[5];
    dest.range(687, 680) = src.Header.SecurityID[6];
    dest.range(679, 672) = src.Header.SecurityID[7];
    dest.range(671, 664) = src.Header.SecurityID[8];
    dest.range(663, 648) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(647, 584) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(583, 580) = src.Header.TradingPhase.Code0;
    dest.range(579, 576) = src.Header.TradingPhase.Code1;
    dest.range(575, 512) = SBE_ENDIAN::reverse<64>(src.NumTrades);
    dest.range(511, 448) = SBE_ENDIAN::reverse<64>(src.TotalVolumeTrade);
    dest.range(447, 384) = SBE_ENDIAN::reverse<64>(src.TotalValueTrade);
    dest.range(383, 320) = SBE_ENDIAN::reverse<64>(src.PrevClosePx);
    dest.range(319, 256) = SBE_ENDIAN::reverse<64>(src.LastPx);
    dest.range(255, 192) = SBE_ENDIAN::reverse<64>(src.OpenPx);
    dest.range(191, 128) = SBE_ENDIAN::reverse<64>(src.HighPx);
    dest.range(127, 64) = SBE_ENDIAN::reverse<64>(src.LowPx);
    dest.range(63, 0) = SBE_ENDIAN::reverse<64>(src.TransactTime);
}


void sbe_intf::SBE_SSZ_ord_t_unpack(SBE_SSZ_ord_t_packed &src,
                          SBE_SSZ_ord_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(383, 376);
    dest.Header.MsgType = src.range(375, 368);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(367, 352));
    dest.Header.SecurityID[0] = src.range(351, 344);
    dest.Header.SecurityID[1] = src.range(343, 336);
    dest.Header.SecurityID[2] = src.range(335, 328);
    dest.Header.SecurityID[3] = src.range(327, 320);
    dest.Header.SecurityID[4] = src.range(319, 312);
    dest.Header.SecurityID[5] = src.range(311, 304);
    dest.Header.SecurityID[6] = src.range(303, 296);
    dest.Header.SecurityID[7] = src.range(295, 288);
    dest.Header.SecurityID[8] = src.range(287, 280);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(279, 264));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(263, 200));
    dest.Header.TradingPhase.Code0 = src.range(199, 196);
    dest.Header.TradingPhase.Code1 = src.range(195, 192);
    dest.Price = SBE_ENDIAN::reverse<32>(src.range(191, 160));
    dest.OrderQty = SBE_ENDIAN::reverse<64>(src.range(159, 96));
    dest.Side = src.range(95, 88);
    dest.OrdType = src.range(87, 80);
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(79, 16));
    dest.Resv[0] = src.range(15, 8);
    dest.Resv[1] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_ord_t_pack(SBE_SSZ_ord_t &src,
                          SBE_SSZ_ord_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(383, 376) = src.Header.SecurityIDSource;
    dest.range(375, 368) = src.Header.MsgType;
    dest.range(367, 352) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(351, 344) = src.Header.SecurityID[0];
    dest.range(343, 336) = src.Header.SecurityID[1];
    dest.range(335, 328) = src.Header.SecurityID[2];
    dest.range(327, 320) = src.Header.SecurityID[3];
    dest.range(319, 312) = src.Header.SecurityID[4];
    dest.range(311, 304) = src.Header.SecurityID[5];
    dest.range(303, 296) = src.Header.SecurityID[6];
    dest.range(295, 288) = src.Header.SecurityID[7];
    dest.range(287, 280) = src.Header.SecurityID[8];
    dest.range(279, 264) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(263, 200) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(199, 196) = src.Header.TradingPhase.Code0;
    dest.range(195, 192) = src.Header.TradingPhase.Code1;
    dest.range(191, 160) = SBE_ENDIAN::reverse<32>(src.Price);
    dest.range(159, 96) = SBE_ENDIAN::reverse<64>(src.OrderQty);
    dest.range(95, 88) = src.Side;
    dest.range(87, 80) = src.OrdType;
    dest.range(79, 16) = SBE_ENDIAN::reverse<64>(src.TransactTime);
    dest.range(15, 8) = src.Resv[0];
    dest.range(7, 0) = src.Resv[1];
}


void sbe_intf::SBE_SSZ_exe_t_unpack(SBE_SSZ_exe_t_packed &src,
                          SBE_SSZ_exe_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(511, 504);
    dest.Header.MsgType = src.range(503, 496);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(495, 480));
    dest.Header.SecurityID[0] = src.range(479, 472);
    dest.Header.SecurityID[1] = src.range(471, 464);
    dest.Header.SecurityID[2] = src.range(463, 456);
    dest.Header.SecurityID[3] = src.range(455, 448);
    dest.Header.SecurityID[4] = src.range(447, 440);
    dest.Header.SecurityID[5] = src.range(439, 432);
    dest.Header.SecurityID[6] = src.range(431, 424);
    dest.Header.SecurityID[7] = src.range(423, 416);
    dest.Header.SecurityID[8] = src.range(415, 408);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(407, 392));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(391, 328));
    dest.Header.TradingPhase.Code0 = src.range(327, 324);
    dest.Header.TradingPhase.Code1 = src.range(323, 320);
    dest.BidApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(319, 256));
    dest.OfferApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(255, 192));
    dest.LastPx = SBE_ENDIAN::reverse<32>(src.range(191, 160));
    dest.LastQty = SBE_ENDIAN::reverse<64>(src.range(159, 96));
    dest.ExecType = src.range(95, 88);
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(87, 24));
    dest.Resv[0] = src.range(23, 16);
    dest.Resv[1] = src.range(15, 8);
    dest.Resv[2] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_exe_t_pack(SBE_SSZ_exe_t &src,
                          SBE_SSZ_exe_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(511, 504) = src.Header.SecurityIDSource;
    dest.range(503, 496) = src.Header.MsgType;
    dest.range(495, 480) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(479, 472) = src.Header.SecurityID[0];
    dest.range(471, 464) = src.Header.SecurityID[1];
    dest.range(463, 456) = src.Header.SecurityID[2];
    dest.range(455, 448) = src.Header.SecurityID[3];
    dest.range(447, 440) = src.Header.SecurityID[4];
    dest.range(439, 432) = src.Header.SecurityID[5];
    dest.range(431, 424) = src.Header.SecurityID[6];
    dest.range(423, 416) = src.Header.SecurityID[7];
    dest.range(415, 408) = src.Header.SecurityID[8];
    dest.range(407, 392) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(391, 328) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(327, 324) = src.Header.TradingPhase.Code0;
    dest.range(323, 320) = src.Header.TradingPhase.Code1;
    dest.range(319, 256) = SBE_ENDIAN::reverse<64>(src.BidApplSeqNum);
    dest.range(255, 192) = SBE_ENDIAN::reverse<64>(src.OfferApplSeqNum);
    dest.range(191, 160) = SBE_ENDIAN::reverse<32>(src.LastPx);
    dest.range(159, 96) = SBE_ENDIAN::reverse<64>(src.LastQty);
    dest.range(95, 88) = src.ExecType;
    dest.range(87, 24) = SBE_ENDIAN::reverse<64>(src.TransactTime);
    dest.range(23, 16) = src.Resv[0];
    dest.range(15, 8) = src.Resv[1];
    dest.range(7, 0) = src.Resv[2];
}


void sbe_intf::SBE_SSZ_option_snap_t_unpack(SBE_SSZ_option_snap_t_packed &src,
                          SBE_SSZ_option_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(2879, 2872);
    dest.Header.MsgType = src.range(2871, 2864);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(2863, 2848));
    dest.Header.SecurityID[0] = src.range(2847, 2840);
    dest.Header.SecurityID[1] = src.range(2839, 2832);
    dest.Header.SecurityID[2] = src.range(2831, 2824);
    dest.Header.SecurityID[3] = src.range(2823, 2816);
    dest.Header.SecurityID[4] = src.range(2815, 2808);
    dest.Header.SecurityID[5] = src.range(2807, 2800);
    dest.Header.SecurityID[6] = src.range(2799, 2792);
    dest.Header.SecurityID[7] = src.range(2791, 2784);
    dest.Header.SecurityID[8] = src.range(2783, 2776);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(2775, 2760));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(2759, 2696));
    dest.Header.TradingPhase.Code0 = src.range(2695, 2692);
    dest.Header.TradingPhase.Code1 = src.range(2691, 2688);
    dest.NumTrades = SBE_ENDIAN::reverse<64>(src.range(2687, 2624));
    dest.TotalVolumeTrade = SBE_ENDIAN::reverse<64>(src.range(2623, 2560));
    dest.TotalValueTrade = SBE_ENDIAN::reverse<64>(src.range(2559, 2496));
    dest.PrevClosePx = SBE_ENDIAN::reverse<32>(src.range(2495, 2464));
    dest.LastPx = SBE_ENDIAN::reverse<32>(src.range(2463, 2432));
    dest.OpenPx = SBE_ENDIAN::reverse<32>(src.range(2431, 2400));
    dest.HighPx = SBE_ENDIAN::reverse<32>(src.range(2399, 2368));
    dest.LowPx = SBE_ENDIAN::reverse<32>(src.range(2367, 2336));
    dest.BidWeightPx = SBE_ENDIAN::reverse<32>(src.range(2335, 2304));
    dest.BidWeightSize = SBE_ENDIAN::reverse<64>(src.range(2303, 2240));
    dest.AskWeightPx = SBE_ENDIAN::reverse<32>(src.range(2239, 2208));
    dest.AskWeightSize = SBE_ENDIAN::reverse<64>(src.range(2207, 2144));
    dest.UpLimitPx = SBE_ENDIAN::reverse<32>(src.range(2143, 2112));
    dest.DnLimitPx = SBE_ENDIAN::reverse<32>(src.range(2111, 2080));
    dest.ContractPos = SBE_ENDIAN::reverse<64>(src.range(2079, 2016));
    dest.RefPx = SBE_ENDIAN::reverse<32>(src.range(2015, 1984));
    dest.BidLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(1983, 1952));
    dest.BidLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(1951, 1888));
    dest.BidLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(1887, 1856));
    dest.BidLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(1855, 1792));
    dest.BidLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(1791, 1760));
    dest.BidLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(1759, 1696));
    dest.BidLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(1695, 1664));
    dest.BidLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(1663, 1600));
    dest.BidLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(1599, 1568));
    dest.BidLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(1567, 1504));
    dest.BidLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(1503, 1472));
    dest.BidLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(1471, 1408));
    dest.BidLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(1407, 1376));
    dest.BidLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(1375, 1312));
    dest.BidLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(1311, 1280));
    dest.BidLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(1279, 1216));
    dest.BidLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(1215, 1184));
    dest.BidLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(1183, 1120));
    dest.BidLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(1119, 1088));
    dest.BidLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(1087, 1024));
    dest.AskLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(1023, 992));
    dest.AskLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(991, 928));
    dest.AskLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(927, 896));
    dest.AskLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(895, 832));
    dest.AskLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(831, 800));
    dest.AskLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(799, 736));
    dest.AskLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(735, 704));
    dest.AskLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(703, 640));
    dest.AskLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(639, 608));
    dest.AskLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(607, 544));
    dest.AskLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(543, 512));
    dest.AskLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(511, 448));
    dest.AskLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(447, 416));
    dest.AskLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(415, 352));
    dest.AskLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(351, 320));
    dest.AskLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(319, 256));
    dest.AskLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(255, 224));
    dest.AskLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(223, 160));
    dest.AskLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(159, 128));
    dest.AskLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(127, 64));
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(63, 0));
}
void sbe_intf::SBE_SSZ_option_snap_t_pack(SBE_SSZ_option_snap_t &src,
                          SBE_SSZ_option_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(2879, 2872) = src.Header.SecurityIDSource;
    dest.range(2871, 2864) = src.Header.MsgType;
    dest.range(2863, 2848) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(2847, 2840) = src.Header.SecurityID[0];
    dest.range(2839, 2832) = src.Header.SecurityID[1];
    dest.range(2831, 2824) = src.Header.SecurityID[2];
    dest.range(2823, 2816) = src.Header.SecurityID[3];
    dest.range(2815, 2808) = src.Header.SecurityID[4];
    dest.range(2807, 2800) = src.Header.SecurityID[5];
    dest.range(2799, 2792) = src.Header.SecurityID[6];
    dest.range(2791, 2784) = src.Header.SecurityID[7];
    dest.range(2783, 2776) = src.Header.SecurityID[8];
    dest.range(2775, 2760) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(2759, 2696) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(2695, 2692) = src.Header.TradingPhase.Code0;
    dest.range(2691, 2688) = src.Header.TradingPhase.Code1;
    dest.range(2687, 2624) = SBE_ENDIAN::reverse<64>(src.NumTrades);
    dest.range(2623, 2560) = SBE_ENDIAN::reverse<64>(src.TotalVolumeTrade);
    dest.range(2559, 2496) = SBE_ENDIAN::reverse<64>(src.TotalValueTrade);
    dest.range(2495, 2464) = SBE_ENDIAN::reverse<32>(src.PrevClosePx);
    dest.range(2463, 2432) = SBE_ENDIAN::reverse<32>(src.LastPx);
    dest.range(2431, 2400) = SBE_ENDIAN::reverse<32>(src.OpenPx);
    dest.range(2399, 2368) = SBE_ENDIAN::reverse<32>(src.HighPx);
    dest.range(2367, 2336) = SBE_ENDIAN::reverse<32>(src.LowPx);
    dest.range(2335, 2304) = SBE_ENDIAN::reverse<32>(src.BidWeightPx);
    dest.range(2303, 2240) = SBE_ENDIAN::reverse<64>(src.BidWeightSize);
    dest.range(2239, 2208) = SBE_ENDIAN::reverse<32>(src.AskWeightPx);
    dest.range(2207, 2144) = SBE_ENDIAN::reverse<64>(src.AskWeightSize);
    dest.range(2143, 2112) = SBE_ENDIAN::reverse<32>(src.UpLimitPx);
    dest.range(2111, 2080) = SBE_ENDIAN::reverse<32>(src.DnLimitPx);
    dest.range(2079, 2016) = SBE_ENDIAN::reverse<64>(src.ContractPos);
    dest.range(2015, 1984) = SBE_ENDIAN::reverse<32>(src.RefPx);
    dest.range(1983, 1952) = SBE_ENDIAN::reverse<32>(src.BidLevel[0].Price);
    dest.range(1951, 1888) = SBE_ENDIAN::reverse<64>(src.BidLevel[0].Qty);
    dest.range(1887, 1856) = SBE_ENDIAN::reverse<32>(src.BidLevel[1].Price);
    dest.range(1855, 1792) = SBE_ENDIAN::reverse<64>(src.BidLevel[1].Qty);
    dest.range(1791, 1760) = SBE_ENDIAN::reverse<32>(src.BidLevel[2].Price);
    dest.range(1759, 1696) = SBE_ENDIAN::reverse<64>(src.BidLevel[2].Qty);
    dest.range(1695, 1664) = SBE_ENDIAN::reverse<32>(src.BidLevel[3].Price);
    dest.range(1663, 1600) = SBE_ENDIAN::reverse<64>(src.BidLevel[3].Qty);
    dest.range(1599, 1568) = SBE_ENDIAN::reverse<32>(src.BidLevel[4].Price);
    dest.range(1567, 1504) = SBE_ENDIAN::reverse<64>(src.BidLevel[4].Qty);
    dest.range(1503, 1472) = SBE_ENDIAN::reverse<32>(src.BidLevel[5].Price);
    dest.range(1471, 1408) = SBE_ENDIAN::reverse<64>(src.BidLevel[5].Qty);
    dest.range(1407, 1376) = SBE_ENDIAN::reverse<32>(src.BidLevel[6].Price);
    dest.range(1375, 1312) = SBE_ENDIAN::reverse<64>(src.BidLevel[6].Qty);
    dest.range(1311, 1280) = SBE_ENDIAN::reverse<32>(src.BidLevel[7].Price);
    dest.range(1279, 1216) = SBE_ENDIAN::reverse<64>(src.BidLevel[7].Qty);
    dest.range(1215, 1184) = SBE_ENDIAN::reverse<32>(src.BidLevel[8].Price);
    dest.range(1183, 1120) = SBE_ENDIAN::reverse<64>(src.BidLevel[8].Qty);
    dest.range(1119, 1088) = SBE_ENDIAN::reverse<32>(src.BidLevel[9].Price);
    dest.range(1087, 1024) = SBE_ENDIAN::reverse<64>(src.BidLevel[9].Qty);
    dest.range(1023, 992) = SBE_ENDIAN::reverse<32>(src.AskLevel[0].Price);
    dest.range(991, 928) = SBE_ENDIAN::reverse<64>(src.AskLevel[0].Qty);
    dest.range(927, 896) = SBE_ENDIAN::reverse<32>(src.AskLevel[1].Price);
    dest.range(895, 832) = SBE_ENDIAN::reverse<64>(src.AskLevel[1].Qty);
    dest.range(831, 800) = SBE_ENDIAN::reverse<32>(src.AskLevel[2].Price);
    dest.range(799, 736) = SBE_ENDIAN::reverse<64>(src.AskLevel[2].Qty);
    dest.range(735, 704) = SBE_ENDIAN::reverse<32>(src.AskLevel[3].Price);
    dest.range(703, 640) = SBE_ENDIAN::reverse<64>(src.AskLevel[3].Qty);
    dest.range(639, 608) = SBE_ENDIAN::reverse<32>(src.AskLevel[4].Price);
    dest.range(607, 544) = SBE_ENDIAN::reverse<64>(src.AskLevel[4].Qty);
    dest.range(543, 512) = SBE_ENDIAN::reverse<32>(src.AskLevel[5].Price);
    dest.range(511, 448) = SBE_ENDIAN::reverse<64>(src.AskLevel[5].Qty);
    dest.range(447, 416) = SBE_ENDIAN::reverse<32>(src.AskLevel[6].Price);
    dest.range(415, 352) = SBE_ENDIAN::reverse<64>(src.AskLevel[6].Qty);
    dest.range(351, 320) = SBE_ENDIAN::reverse<32>(src.AskLevel[7].Price);
    dest.range(319, 256) = SBE_ENDIAN::reverse<64>(src.AskLevel[7].Qty);
    dest.range(255, 224) = SBE_ENDIAN::reverse<32>(src.AskLevel[8].Price);
    dest.range(223, 160) = SBE_ENDIAN::reverse<64>(src.AskLevel[8].Qty);
    dest.range(159, 128) = SBE_ENDIAN::reverse<32>(src.AskLevel[9].Price);
    dest.range(127, 64) = SBE_ENDIAN::reverse<64>(src.AskLevel[9].Qty);
    dest.range(63, 0) = SBE_ENDIAN::reverse<64>(src.TransactTime);
}


void sbe_intf::SBE_SSZ_fund_snap_t_unpack(SBE_SSZ_fund_snap_t_packed &src,
                          SBE_SSZ_fund_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(2815, 2808);
    dest.Header.MsgType = src.range(2807, 2800);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(2799, 2784));
    dest.Header.SecurityID[0] = src.range(2783, 2776);
    dest.Header.SecurityID[1] = src.range(2775, 2768);
    dest.Header.SecurityID[2] = src.range(2767, 2760);
    dest.Header.SecurityID[3] = src.range(2759, 2752);
    dest.Header.SecurityID[4] = src.range(2751, 2744);
    dest.Header.SecurityID[5] = src.range(2743, 2736);
    dest.Header.SecurityID[6] = src.range(2735, 2728);
    dest.Header.SecurityID[7] = src.range(2727, 2720);
    dest.Header.SecurityID[8] = src.range(2719, 2712);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(2711, 2696));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(2695, 2632));
    dest.Header.TradingPhase.Code0 = src.range(2631, 2628);
    dest.Header.TradingPhase.Code1 = src.range(2627, 2624);
    dest.NumTrades = SBE_ENDIAN::reverse<64>(src.range(2623, 2560));
    dest.TotalVolumeTrade = SBE_ENDIAN::reverse<64>(src.range(2559, 2496));
    dest.TotalValueTrade = SBE_ENDIAN::reverse<64>(src.range(2495, 2432));
    dest.PrevClosePx = SBE_ENDIAN::reverse<32>(src.range(2431, 2400));
    dest.LastPx = SBE_ENDIAN::reverse<32>(src.range(2399, 2368));
    dest.OpenPx = SBE_ENDIAN::reverse<32>(src.range(2367, 2336));
    dest.HighPx = SBE_ENDIAN::reverse<32>(src.range(2335, 2304));
    dest.LowPx = SBE_ENDIAN::reverse<32>(src.range(2303, 2272));
    dest.BidWeightPx = SBE_ENDIAN::reverse<32>(src.range(2271, 2240));
    dest.BidWeightSize = SBE_ENDIAN::reverse<64>(src.range(2239, 2176));
    dest.AskWeightPx = SBE_ENDIAN::reverse<32>(src.range(2175, 2144));
    dest.AskWeightSize = SBE_ENDIAN::reverse<64>(src.range(2143, 2080));
    dest.UpLimitPx = SBE_ENDIAN::reverse<32>(src.range(2079, 2048));
    dest.DnLimitPx = SBE_ENDIAN::reverse<32>(src.range(2047, 2016));
    dest.BidLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(2015, 1984));
    dest.BidLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(1983, 1920));
    dest.BidLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(1919, 1888));
    dest.BidLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(1887, 1824));
    dest.BidLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(1823, 1792));
    dest.BidLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(1791, 1728));
    dest.BidLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(1727, 1696));
    dest.BidLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(1695, 1632));
    dest.BidLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(1631, 1600));
    dest.BidLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(1599, 1536));
    dest.BidLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(1535, 1504));
    dest.BidLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(1503, 1440));
    dest.BidLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(1439, 1408));
    dest.BidLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(1407, 1344));
    dest.BidLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(1343, 1312));
    dest.BidLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(1311, 1248));
    dest.BidLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(1247, 1216));
    dest.BidLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(1215, 1152));
    dest.BidLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(1151, 1120));
    dest.BidLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(1119, 1056));
    dest.AskLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(1055, 1024));
    dest.AskLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(1023, 960));
    dest.AskLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(959, 928));
    dest.AskLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(927, 864));
    dest.AskLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(863, 832));
    dest.AskLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(831, 768));
    dest.AskLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(767, 736));
    dest.AskLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(735, 672));
    dest.AskLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(671, 640));
    dest.AskLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(639, 576));
    dest.AskLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(575, 544));
    dest.AskLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(543, 480));
    dest.AskLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(479, 448));
    dest.AskLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(447, 384));
    dest.AskLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(383, 352));
    dest.AskLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(351, 288));
    dest.AskLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(287, 256));
    dest.AskLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(255, 192));
    dest.AskLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(191, 160));
    dest.AskLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(159, 96));
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(95, 32));
    dest.IOPV = SBE_ENDIAN::reverse<32>(src.range(31, 0));
}
void sbe_intf::SBE_SSZ_fund_snap_t_pack(SBE_SSZ_fund_snap_t &src,
                          SBE_SSZ_fund_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(2815, 2808) = src.Header.SecurityIDSource;
    dest.range(2807, 2800) = src.Header.MsgType;
    dest.range(2799, 2784) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(2783, 2776) = src.Header.SecurityID[0];
    dest.range(2775, 2768) = src.Header.SecurityID[1];
    dest.range(2767, 2760) = src.Header.SecurityID[2];
    dest.range(2759, 2752) = src.Header.SecurityID[3];
    dest.range(2751, 2744) = src.Header.SecurityID[4];
    dest.range(2743, 2736) = src.Header.SecurityID[5];
    dest.range(2735, 2728) = src.Header.SecurityID[6];
    dest.range(2727, 2720) = src.Header.SecurityID[7];
    dest.range(2719, 2712) = src.Header.SecurityID[8];
    dest.range(2711, 2696) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(2695, 2632) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(2631, 2628) = src.Header.TradingPhase.Code0;
    dest.range(2627, 2624) = src.Header.TradingPhase.Code1;
    dest.range(2623, 2560) = SBE_ENDIAN::reverse<64>(src.NumTrades);
    dest.range(2559, 2496) = SBE_ENDIAN::reverse<64>(src.TotalVolumeTrade);
    dest.range(2495, 2432) = SBE_ENDIAN::reverse<64>(src.TotalValueTrade);
    dest.range(2431, 2400) = SBE_ENDIAN::reverse<32>(src.PrevClosePx);
    dest.range(2399, 2368) = SBE_ENDIAN::reverse<32>(src.LastPx);
    dest.range(2367, 2336) = SBE_ENDIAN::reverse<32>(src.OpenPx);
    dest.range(2335, 2304) = SBE_ENDIAN::reverse<32>(src.HighPx);
    dest.range(2303, 2272) = SBE_ENDIAN::reverse<32>(src.LowPx);
    dest.range(2271, 2240) = SBE_ENDIAN::reverse<32>(src.BidWeightPx);
    dest.range(2239, 2176) = SBE_ENDIAN::reverse<64>(src.BidWeightSize);
    dest.range(2175, 2144) = SBE_ENDIAN::reverse<32>(src.AskWeightPx);
    dest.range(2143, 2080) = SBE_ENDIAN::reverse<64>(src.AskWeightSize);
    dest.range(2079, 2048) = SBE_ENDIAN::reverse<32>(src.UpLimitPx);
    dest.range(2047, 2016) = SBE_ENDIAN::reverse<32>(src.DnLimitPx);
    dest.range(2015, 1984) = SBE_ENDIAN::reverse<32>(src.BidLevel[0].Price);
    dest.range(1983, 1920) = SBE_ENDIAN::reverse<64>(src.BidLevel[0].Qty);
    dest.range(1919, 1888) = SBE_ENDIAN::reverse<32>(src.BidLevel[1].Price);
    dest.range(1887, 1824) = SBE_ENDIAN::reverse<64>(src.BidLevel[1].Qty);
    dest.range(1823, 1792) = SBE_ENDIAN::reverse<32>(src.BidLevel[2].Price);
    dest.range(1791, 1728) = SBE_ENDIAN::reverse<64>(src.BidLevel[2].Qty);
    dest.range(1727, 1696) = SBE_ENDIAN::reverse<32>(src.BidLevel[3].Price);
    dest.range(1695, 1632) = SBE_ENDIAN::reverse<64>(src.BidLevel[3].Qty);
    dest.range(1631, 1600) = SBE_ENDIAN::reverse<32>(src.BidLevel[4].Price);
    dest.range(1599, 1536) = SBE_ENDIAN::reverse<64>(src.BidLevel[4].Qty);
    dest.range(1535, 1504) = SBE_ENDIAN::reverse<32>(src.BidLevel[5].Price);
    dest.range(1503, 1440) = SBE_ENDIAN::reverse<64>(src.BidLevel[5].Qty);
    dest.range(1439, 1408) = SBE_ENDIAN::reverse<32>(src.BidLevel[6].Price);
    dest.range(1407, 1344) = SBE_ENDIAN::reverse<64>(src.BidLevel[6].Qty);
    dest.range(1343, 1312) = SBE_ENDIAN::reverse<32>(src.BidLevel[7].Price);
    dest.range(1311, 1248) = SBE_ENDIAN::reverse<64>(src.BidLevel[7].Qty);
    dest.range(1247, 1216) = SBE_ENDIAN::reverse<32>(src.BidLevel[8].Price);
    dest.range(1215, 1152) = SBE_ENDIAN::reverse<64>(src.BidLevel[8].Qty);
    dest.range(1151, 1120) = SBE_ENDIAN::reverse<32>(src.BidLevel[9].Price);
    dest.range(1119, 1056) = SBE_ENDIAN::reverse<64>(src.BidLevel[9].Qty);
    dest.range(1055, 1024) = SBE_ENDIAN::reverse<32>(src.AskLevel[0].Price);
    dest.range(1023, 960) = SBE_ENDIAN::reverse<64>(src.AskLevel[0].Qty);
    dest.range(959, 928) = SBE_ENDIAN::reverse<32>(src.AskLevel[1].Price);
    dest.range(927, 864) = SBE_ENDIAN::reverse<64>(src.AskLevel[1].Qty);
    dest.range(863, 832) = SBE_ENDIAN::reverse<32>(src.AskLevel[2].Price);
    dest.range(831, 768) = SBE_ENDIAN::reverse<64>(src.AskLevel[2].Qty);
    dest.range(767, 736) = SBE_ENDIAN::reverse<32>(src.AskLevel[3].Price);
    dest.range(735, 672) = SBE_ENDIAN::reverse<64>(src.AskLevel[3].Qty);
    dest.range(671, 640) = SBE_ENDIAN::reverse<32>(src.AskLevel[4].Price);
    dest.range(639, 576) = SBE_ENDIAN::reverse<64>(src.AskLevel[4].Qty);
    dest.range(575, 544) = SBE_ENDIAN::reverse<32>(src.AskLevel[5].Price);
    dest.range(543, 480) = SBE_ENDIAN::reverse<64>(src.AskLevel[5].Qty);
    dest.range(479, 448) = SBE_ENDIAN::reverse<32>(src.AskLevel[6].Price);
    dest.range(447, 384) = SBE_ENDIAN::reverse<64>(src.AskLevel[6].Qty);
    dest.range(383, 352) = SBE_ENDIAN::reverse<32>(src.AskLevel[7].Price);
    dest.range(351, 288) = SBE_ENDIAN::reverse<64>(src.AskLevel[7].Qty);
    dest.range(287, 256) = SBE_ENDIAN::reverse<32>(src.AskLevel[8].Price);
    dest.range(255, 192) = SBE_ENDIAN::reverse<64>(src.AskLevel[8].Qty);
    dest.range(191, 160) = SBE_ENDIAN::reverse<32>(src.AskLevel[9].Price);
    dest.range(159, 96) = SBE_ENDIAN::reverse<64>(src.AskLevel[9].Qty);
    dest.range(95, 32) = SBE_ENDIAN::reverse<64>(src.TransactTime);
    dest.range(31, 0) = SBE_ENDIAN::reverse<32>(src.IOPV);
}


void sbe_intf::SBE_SSZ_bond_snap_t_unpack(SBE_SSZ_bond_snap_t_packed &src,
                          SBE_SSZ_bond_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(2943, 2936);
    dest.Header.MsgType = src.range(2935, 2928);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(2927, 2912));
    dest.Header.SecurityID[0] = src.range(2911, 2904);
    dest.Header.SecurityID[1] = src.range(2903, 2896);
    dest.Header.SecurityID[2] = src.range(2895, 2888);
    dest.Header.SecurityID[3] = src.range(2887, 2880);
    dest.Header.SecurityID[4] = src.range(2879, 2872);
    dest.Header.SecurityID[5] = src.range(2871, 2864);
    dest.Header.SecurityID[6] = src.range(2863, 2856);
    dest.Header.SecurityID[7] = src.range(2855, 2848);
    dest.Header.SecurityID[8] = src.range(2847, 2840);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(2839, 2824));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(2823, 2760));
    dest.Header.TradingPhase.Code0 = src.range(2759, 2756);
    dest.Header.TradingPhase.Code1 = src.range(2755, 2752);
    dest.NumTrades = SBE_ENDIAN::reverse<64>(src.range(2751, 2688));
    dest.TotalVolumeTrade = SBE_ENDIAN::reverse<64>(src.range(2687, 2624));
    dest.TotalValueTrade = SBE_ENDIAN::reverse<64>(src.range(2623, 2560));
    dest.PrevClosePx = SBE_ENDIAN::reverse<32>(src.range(2559, 2528));
    dest.LastPx = SBE_ENDIAN::reverse<32>(src.range(2527, 2496));
    dest.OpenPx = SBE_ENDIAN::reverse<32>(src.range(2495, 2464));
    dest.HighPx = SBE_ENDIAN::reverse<32>(src.range(2463, 2432));
    dest.LowPx = SBE_ENDIAN::reverse<32>(src.range(2431, 2400));
    dest.BidWeightPx = SBE_ENDIAN::reverse<32>(src.range(2399, 2368));
    dest.BidWeightSize = SBE_ENDIAN::reverse<64>(src.range(2367, 2304));
    dest.AskWeightPx = SBE_ENDIAN::reverse<32>(src.range(2303, 2272));
    dest.AskWeightSize = SBE_ENDIAN::reverse<64>(src.range(2271, 2208));
    dest.LastPxTradeType = SBE_ENDIAN::reverse<32>(src.range(2207, 2176));
    dest.MatchTradeLastPx = SBE_ENDIAN::reverse<32>(src.range(2175, 2144));
    dest.AuctionVolumeTrade = SBE_ENDIAN::reverse<64>(src.range(2143, 2080));
    dest.AuctionValueTrade = SBE_ENDIAN::reverse<64>(src.range(2079, 2016));
    dest.BidLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(2015, 1984));
    dest.BidLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(1983, 1920));
    dest.BidLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(1919, 1888));
    dest.BidLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(1887, 1824));
    dest.BidLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(1823, 1792));
    dest.BidLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(1791, 1728));
    dest.BidLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(1727, 1696));
    dest.BidLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(1695, 1632));
    dest.BidLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(1631, 1600));
    dest.BidLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(1599, 1536));
    dest.BidLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(1535, 1504));
    dest.BidLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(1503, 1440));
    dest.BidLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(1439, 1408));
    dest.BidLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(1407, 1344));
    dest.BidLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(1343, 1312));
    dest.BidLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(1311, 1248));
    dest.BidLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(1247, 1216));
    dest.BidLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(1215, 1152));
    dest.BidLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(1151, 1120));
    dest.BidLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(1119, 1056));
    dest.AskLevel[0].Price = SBE_ENDIAN::reverse<32>(src.range(1055, 1024));
    dest.AskLevel[0].Qty = SBE_ENDIAN::reverse<64>(src.range(1023, 960));
    dest.AskLevel[1].Price = SBE_ENDIAN::reverse<32>(src.range(959, 928));
    dest.AskLevel[1].Qty = SBE_ENDIAN::reverse<64>(src.range(927, 864));
    dest.AskLevel[2].Price = SBE_ENDIAN::reverse<32>(src.range(863, 832));
    dest.AskLevel[2].Qty = SBE_ENDIAN::reverse<64>(src.range(831, 768));
    dest.AskLevel[3].Price = SBE_ENDIAN::reverse<32>(src.range(767, 736));
    dest.AskLevel[3].Qty = SBE_ENDIAN::reverse<64>(src.range(735, 672));
    dest.AskLevel[4].Price = SBE_ENDIAN::reverse<32>(src.range(671, 640));
    dest.AskLevel[4].Qty = SBE_ENDIAN::reverse<64>(src.range(639, 576));
    dest.AskLevel[5].Price = SBE_ENDIAN::reverse<32>(src.range(575, 544));
    dest.AskLevel[5].Qty = SBE_ENDIAN::reverse<64>(src.range(543, 480));
    dest.AskLevel[6].Price = SBE_ENDIAN::reverse<32>(src.range(479, 448));
    dest.AskLevel[6].Qty = SBE_ENDIAN::reverse<64>(src.range(447, 384));
    dest.AskLevel[7].Price = SBE_ENDIAN::reverse<32>(src.range(383, 352));
    dest.AskLevel[7].Qty = SBE_ENDIAN::reverse<64>(src.range(351, 288));
    dest.AskLevel[8].Price = SBE_ENDIAN::reverse<32>(src.range(287, 256));
    dest.AskLevel[8].Qty = SBE_ENDIAN::reverse<64>(src.range(255, 192));
    dest.AskLevel[9].Price = SBE_ENDIAN::reverse<32>(src.range(191, 160));
    dest.AskLevel[9].Qty = SBE_ENDIAN::reverse<64>(src.range(159, 96));
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(95, 32));
    dest.Resv[0] = src.range(31, 24);
    dest.Resv[1] = src.range(23, 16);
    dest.Resv[2] = src.range(15, 8);
    dest.Resv[3] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_bond_snap_t_pack(SBE_SSZ_bond_snap_t &src,
                          SBE_SSZ_bond_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(2943, 2936) = src.Header.SecurityIDSource;
    dest.range(2935, 2928) = src.Header.MsgType;
    dest.range(2927, 2912) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(2911, 2904) = src.Header.SecurityID[0];
    dest.range(2903, 2896) = src.Header.SecurityID[1];
    dest.range(2895, 2888) = src.Header.SecurityID[2];
    dest.range(2887, 2880) = src.Header.SecurityID[3];
    dest.range(2879, 2872) = src.Header.SecurityID[4];
    dest.range(2871, 2864) = src.Header.SecurityID[5];
    dest.range(2863, 2856) = src.Header.SecurityID[6];
    dest.range(2855, 2848) = src.Header.SecurityID[7];
    dest.range(2847, 2840) = src.Header.SecurityID[8];
    dest.range(2839, 2824) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(2823, 2760) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(2759, 2756) = src.Header.TradingPhase.Code0;
    dest.range(2755, 2752) = src.Header.TradingPhase.Code1;
    dest.range(2751, 2688) = SBE_ENDIAN::reverse<64>(src.NumTrades);
    dest.range(2687, 2624) = SBE_ENDIAN::reverse<64>(src.TotalVolumeTrade);
    dest.range(2623, 2560) = SBE_ENDIAN::reverse<64>(src.TotalValueTrade);
    dest.range(2559, 2528) = SBE_ENDIAN::reverse<32>(src.PrevClosePx);
    dest.range(2527, 2496) = SBE_ENDIAN::reverse<32>(src.LastPx);
    dest.range(2495, 2464) = SBE_ENDIAN::reverse<32>(src.OpenPx);
    dest.range(2463, 2432) = SBE_ENDIAN::reverse<32>(src.HighPx);
    dest.range(2431, 2400) = SBE_ENDIAN::reverse<32>(src.LowPx);
    dest.range(2399, 2368) = SBE_ENDIAN::reverse<32>(src.BidWeightPx);
    dest.range(2367, 2304) = SBE_ENDIAN::reverse<64>(src.BidWeightSize);
    dest.range(2303, 2272) = SBE_ENDIAN::reverse<32>(src.AskWeightPx);
    dest.range(2271, 2208) = SBE_ENDIAN::reverse<64>(src.AskWeightSize);
    dest.range(2207, 2176) = SBE_ENDIAN::reverse<32>(src.LastPxTradeType);
    dest.range(2175, 2144) = SBE_ENDIAN::reverse<32>(src.MatchTradeLastPx);
    dest.range(2143, 2080) = SBE_ENDIAN::reverse<64>(src.AuctionVolumeTrade);
    dest.range(2079, 2016) = SBE_ENDIAN::reverse<64>(src.AuctionValueTrade);
    dest.range(2015, 1984) = SBE_ENDIAN::reverse<32>(src.BidLevel[0].Price);
    dest.range(1983, 1920) = SBE_ENDIAN::reverse<64>(src.BidLevel[0].Qty);
    dest.range(1919, 1888) = SBE_ENDIAN::reverse<32>(src.BidLevel[1].Price);
    dest.range(1887, 1824) = SBE_ENDIAN::reverse<64>(src.BidLevel[1].Qty);
    dest.range(1823, 1792) = SBE_ENDIAN::reverse<32>(src.BidLevel[2].Price);
    dest.range(1791, 1728) = SBE_ENDIAN::reverse<64>(src.BidLevel[2].Qty);
    dest.range(1727, 1696) = SBE_ENDIAN::reverse<32>(src.BidLevel[3].Price);
    dest.range(1695, 1632) = SBE_ENDIAN::reverse<64>(src.BidLevel[3].Qty);
    dest.range(1631, 1600) = SBE_ENDIAN::reverse<32>(src.BidLevel[4].Price);
    dest.range(1599, 1536) = SBE_ENDIAN::reverse<64>(src.BidLevel[4].Qty);
    dest.range(1535, 1504) = SBE_ENDIAN::reverse<32>(src.BidLevel[5].Price);
    dest.range(1503, 1440) = SBE_ENDIAN::reverse<64>(src.BidLevel[5].Qty);
    dest.range(1439, 1408) = SBE_ENDIAN::reverse<32>(src.BidLevel[6].Price);
    dest.range(1407, 1344) = SBE_ENDIAN::reverse<64>(src.BidLevel[6].Qty);
    dest.range(1343, 1312) = SBE_ENDIAN::reverse<32>(src.BidLevel[7].Price);
    dest.range(1311, 1248) = SBE_ENDIAN::reverse<64>(src.BidLevel[7].Qty);
    dest.range(1247, 1216) = SBE_ENDIAN::reverse<32>(src.BidLevel[8].Price);
    dest.range(1215, 1152) = SBE_ENDIAN::reverse<64>(src.BidLevel[8].Qty);
    dest.range(1151, 1120) = SBE_ENDIAN::reverse<32>(src.BidLevel[9].Price);
    dest.range(1119, 1056) = SBE_ENDIAN::reverse<64>(src.BidLevel[9].Qty);
    dest.range(1055, 1024) = SBE_ENDIAN::reverse<32>(src.AskLevel[0].Price);
    dest.range(1023, 960) = SBE_ENDIAN::reverse<64>(src.AskLevel[0].Qty);
    dest.range(959, 928) = SBE_ENDIAN::reverse<32>(src.AskLevel[1].Price);
    dest.range(927, 864) = SBE_ENDIAN::reverse<64>(src.AskLevel[1].Qty);
    dest.range(863, 832) = SBE_ENDIAN::reverse<32>(src.AskLevel[2].Price);
    dest.range(831, 768) = SBE_ENDIAN::reverse<64>(src.AskLevel[2].Qty);
    dest.range(767, 736) = SBE_ENDIAN::reverse<32>(src.AskLevel[3].Price);
    dest.range(735, 672) = SBE_ENDIAN::reverse<64>(src.AskLevel[3].Qty);
    dest.range(671, 640) = SBE_ENDIAN::reverse<32>(src.AskLevel[4].Price);
    dest.range(639, 576) = SBE_ENDIAN::reverse<64>(src.AskLevel[4].Qty);
    dest.range(575, 544) = SBE_ENDIAN::reverse<32>(src.AskLevel[5].Price);
    dest.range(543, 480) = SBE_ENDIAN::reverse<64>(src.AskLevel[5].Qty);
    dest.range(479, 448) = SBE_ENDIAN::reverse<32>(src.AskLevel[6].Price);
    dest.range(447, 384) = SBE_ENDIAN::reverse<64>(src.AskLevel[6].Qty);
    dest.range(383, 352) = SBE_ENDIAN::reverse<32>(src.AskLevel[7].Price);
    dest.range(351, 288) = SBE_ENDIAN::reverse<64>(src.AskLevel[7].Qty);
    dest.range(287, 256) = SBE_ENDIAN::reverse<32>(src.AskLevel[8].Price);
    dest.range(255, 192) = SBE_ENDIAN::reverse<64>(src.AskLevel[8].Qty);
    dest.range(191, 160) = SBE_ENDIAN::reverse<32>(src.AskLevel[9].Price);
    dest.range(159, 96) = SBE_ENDIAN::reverse<64>(src.AskLevel[9].Qty);
    dest.range(95, 32) = SBE_ENDIAN::reverse<64>(src.TransactTime);
    dest.range(31, 24) = src.Resv[0];
    dest.range(23, 16) = src.Resv[1];
    dest.range(15, 8) = src.Resv[2];
    dest.range(7, 0) = src.Resv[3];
}


void sbe_intf::SBE_SSZ_bond_ord_t_unpack(SBE_SSZ_bond_ord_t_packed &src,
                          SBE_SSZ_bond_ord_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(383, 376);
    dest.Header.MsgType = src.range(375, 368);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(367, 352));
    dest.Header.SecurityID[0] = src.range(351, 344);
    dest.Header.SecurityID[1] = src.range(343, 336);
    dest.Header.SecurityID[2] = src.range(335, 328);
    dest.Header.SecurityID[3] = src.range(327, 320);
    dest.Header.SecurityID[4] = src.range(319, 312);
    dest.Header.SecurityID[5] = src.range(311, 304);
    dest.Header.SecurityID[6] = src.range(303, 296);
    dest.Header.SecurityID[7] = src.range(295, 288);
    dest.Header.SecurityID[8] = src.range(287, 280);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(279, 264));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(263, 200));
    dest.Header.TradingPhase.Code0 = src.range(199, 196);
    dest.Header.TradingPhase.Code1 = src.range(195, 192);
    dest.Price = SBE_ENDIAN::reverse<32>(src.range(191, 160));
    dest.OrderQty = SBE_ENDIAN::reverse<64>(src.range(159, 96));
    dest.Side = src.range(95, 88);
    dest.OrdType = src.range(87, 80);
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(79, 16));
    dest.Resv[0] = src.range(15, 8);
    dest.Resv[1] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_bond_ord_t_pack(SBE_SSZ_bond_ord_t &src,
                          SBE_SSZ_bond_ord_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(383, 376) = src.Header.SecurityIDSource;
    dest.range(375, 368) = src.Header.MsgType;
    dest.range(367, 352) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(351, 344) = src.Header.SecurityID[0];
    dest.range(343, 336) = src.Header.SecurityID[1];
    dest.range(335, 328) = src.Header.SecurityID[2];
    dest.range(327, 320) = src.Header.SecurityID[3];
    dest.range(319, 312) = src.Header.SecurityID[4];
    dest.range(311, 304) = src.Header.SecurityID[5];
    dest.range(303, 296) = src.Header.SecurityID[6];
    dest.range(295, 288) = src.Header.SecurityID[7];
    dest.range(287, 280) = src.Header.SecurityID[8];
    dest.range(279, 264) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(263, 200) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(199, 196) = src.Header.TradingPhase.Code0;
    dest.range(195, 192) = src.Header.TradingPhase.Code1;
    dest.range(191, 160) = SBE_ENDIAN::reverse<32>(src.Price);
    dest.range(159, 96) = SBE_ENDIAN::reverse<64>(src.OrderQty);
    dest.range(95, 88) = src.Side;
    dest.range(87, 80) = src.OrdType;
    dest.range(79, 16) = SBE_ENDIAN::reverse<64>(src.TransactTime);
    dest.range(15, 8) = src.Resv[0];
    dest.range(7, 0) = src.Resv[1];
}


void sbe_intf::SBE_SSZ_bond_exe_t_unpack(SBE_SSZ_bond_exe_t_packed &src,
                          SBE_SSZ_bond_exe_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(511, 504);
    dest.Header.MsgType = src.range(503, 496);
    dest.Header.MsgLen = SBE_ENDIAN::reverse<16>(src.range(495, 480));
    dest.Header.SecurityID[0] = src.range(479, 472);
    dest.Header.SecurityID[1] = src.range(471, 464);
    dest.Header.SecurityID[2] = src.range(463, 456);
    dest.Header.SecurityID[3] = src.range(455, 448);
    dest.Header.SecurityID[4] = src.range(447, 440);
    dest.Header.SecurityID[5] = src.range(439, 432);
    dest.Header.SecurityID[6] = src.range(431, 424);
    dest.Header.SecurityID[7] = src.range(423, 416);
    dest.Header.SecurityID[8] = src.range(415, 408);
    dest.Header.ChannelNo = SBE_ENDIAN::reverse<16>(src.range(407, 392));
    dest.Header.ApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(391, 328));
    dest.Header.TradingPhase.Code0 = src.range(327, 324);
    dest.Header.TradingPhase.Code1 = src.range(323, 320);
    dest.BidApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(319, 256));
    dest.OfferApplSeqNum = SBE_ENDIAN::reverse<64>(src.range(255, 192));
    dest.LastPx = SBE_ENDIAN::reverse<32>(src.range(191, 160));
    dest.LastQty = SBE_ENDIAN::reverse<64>(src.range(159, 96));
    dest.ExecType = src.range(95, 88);
    dest.TransactTime = SBE_ENDIAN::reverse<64>(src.range(87, 24));
    dest.Resv[0] = src.range(23, 16);
    dest.Resv[1] = src.range(15, 8);
    dest.Resv[2] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_bond_exe_t_pack(SBE_SSZ_bond_exe_t &src,
                          SBE_SSZ_bond_exe_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(511, 504) = src.Header.SecurityIDSource;
    dest.range(503, 496) = src.Header.MsgType;
    dest.range(495, 480) = SBE_ENDIAN::reverse<16>(src.Header.MsgLen);
    dest.range(479, 472) = src.Header.SecurityID[0];
    dest.range(471, 464) = src.Header.SecurityID[1];
    dest.range(463, 456) = src.Header.SecurityID[2];
    dest.range(455, 448) = src.Header.SecurityID[3];
    dest.range(447, 440) = src.Header.SecurityID[4];
    dest.range(439, 432) = src.Header.SecurityID[5];
    dest.range(431, 424) = src.Header.SecurityID[6];
    dest.range(423, 416) = src.Header.SecurityID[7];
    dest.range(415, 408) = src.Header.SecurityID[8];
    dest.range(407, 392) = SBE_ENDIAN::reverse<16>(src.Header.ChannelNo);
    dest.range(391, 328) = SBE_ENDIAN::reverse<64>(src.Header.ApplSeqNum);
    dest.range(327, 324) = src.Header.TradingPhase.Code0;
    dest.range(323, 320) = src.Header.TradingPhase.Code1;
    dest.range(319, 256) = SBE_ENDIAN::reverse<64>(src.BidApplSeqNum);
    dest.range(255, 192) = SBE_ENDIAN::reverse<64>(src.OfferApplSeqNum);
    dest.range(191, 160) = SBE_ENDIAN::reverse<32>(src.LastPx);
    dest.range(159, 96) = SBE_ENDIAN::reverse<64>(src.LastQty);
    dest.range(95, 88) = src.ExecType;
    dest.range(87, 24) = SBE_ENDIAN::reverse<64>(src.TransactTime);
    dest.range(23, 16) = src.Resv[0];
    dest.range(15, 8) = src.Resv[1];
    dest.range(7, 0) = src.Resv[2];
}

bool operator==(const price_level_t& A, const price_level_t& B){
    return A.Price == B.Price
        && A.Qty == B.Qty
        ;
}
bool operator==(const QtyQueue_level_t& A, const QtyQueue_level_t& B){
    return A.NoOrders == B.NoOrders
        && A.QtyQueue[0] == B.QtyQueue[0]
        && A.QtyQueue[1] == B.QtyQueue[1]
        && A.QtyQueue[2] == B.QtyQueue[2]
        && A.QtyQueue[3] == B.QtyQueue[3]
        && A.QtyQueue[4] == B.QtyQueue[4]
        && A.QtyQueue[5] == B.QtyQueue[5]
        && A.QtyQueue[6] == B.QtyQueue[6]
        && A.QtyQueue[7] == B.QtyQueue[7]
        && A.QtyQueue[8] == B.QtyQueue[8]
        && A.QtyQueue[9] == B.QtyQueue[9]
        && A.QtyQueue[10] == B.QtyQueue[10]
        && A.QtyQueue[11] == B.QtyQueue[11]
        && A.QtyQueue[12] == B.QtyQueue[12]
        && A.QtyQueue[13] == B.QtyQueue[13]
        && A.QtyQueue[14] == B.QtyQueue[14]
        && A.QtyQueue[15] == B.QtyQueue[15]
        && A.QtyQueue[16] == B.QtyQueue[16]
        && A.QtyQueue[17] == B.QtyQueue[17]
        && A.QtyQueue[18] == B.QtyQueue[18]
        && A.QtyQueue[19] == B.QtyQueue[19]
        && A.QtyQueue[20] == B.QtyQueue[20]
        && A.QtyQueue[21] == B.QtyQueue[21]
        && A.QtyQueue[22] == B.QtyQueue[22]
        && A.QtyQueue[23] == B.QtyQueue[23]
        && A.QtyQueue[24] == B.QtyQueue[24]
        && A.QtyQueue[25] == B.QtyQueue[25]
        && A.QtyQueue[26] == B.QtyQueue[26]
        && A.QtyQueue[27] == B.QtyQueue[27]
        && A.QtyQueue[28] == B.QtyQueue[28]
        && A.QtyQueue[29] == B.QtyQueue[29]
        && A.QtyQueue[30] == B.QtyQueue[30]
        && A.QtyQueue[31] == B.QtyQueue[31]
        && A.QtyQueue[32] == B.QtyQueue[32]
        && A.QtyQueue[33] == B.QtyQueue[33]
        && A.QtyQueue[34] == B.QtyQueue[34]
        && A.QtyQueue[35] == B.QtyQueue[35]
        && A.QtyQueue[36] == B.QtyQueue[36]
        && A.QtyQueue[37] == B.QtyQueue[37]
        && A.QtyQueue[38] == B.QtyQueue[38]
        && A.QtyQueue[39] == B.QtyQueue[39]
        && A.QtyQueue[40] == B.QtyQueue[40]
        && A.QtyQueue[41] == B.QtyQueue[41]
        && A.QtyQueue[42] == B.QtyQueue[42]
        && A.QtyQueue[43] == B.QtyQueue[43]
        && A.QtyQueue[44] == B.QtyQueue[44]
        && A.QtyQueue[45] == B.QtyQueue[45]
        && A.QtyQueue[46] == B.QtyQueue[46]
        && A.QtyQueue[47] == B.QtyQueue[47]
        && A.QtyQueue[48] == B.QtyQueue[48]
        && A.QtyQueue[49] == B.QtyQueue[49]
        ;
}
bool operator==(const SSZ_TradingPhaseCodePack_t& A, const SSZ_TradingPhaseCodePack_t& B){
    return A.Code0 == B.Code0
        && A.Code1 == B.Code1
        ;
}
bool operator==(const SBE_SSZ_header_t& A, const SBE_SSZ_header_t& B){
    return A.SecurityIDSource == B.SecurityIDSource
        && A.MsgType == B.MsgType
        && A.MsgLen == B.MsgLen
        && A.SecurityID[0] == B.SecurityID[0]
        && A.SecurityID[1] == B.SecurityID[1]
        && A.SecurityID[2] == B.SecurityID[2]
        && A.SecurityID[3] == B.SecurityID[3]
        && A.SecurityID[4] == B.SecurityID[4]
        && A.SecurityID[5] == B.SecurityID[5]
        && A.SecurityID[6] == B.SecurityID[6]
        && A.SecurityID[7] == B.SecurityID[7]
        && A.SecurityID[8] == B.SecurityID[8]
        && A.ChannelNo == B.ChannelNo
        && A.ApplSeqNum == B.ApplSeqNum
        && A.TradingPhase.Code0 == B.TradingPhase.Code0
        && A.TradingPhase.Code1 == B.TradingPhase.Code1
        ;
}
bool operator==(const SBE_SSZ_instrument_snap_t& A, const SBE_SSZ_instrument_snap_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.NumTrades == B.NumTrades
        && A.TotalVolumeTrade == B.TotalVolumeTrade
        && A.TotalValueTrade == B.TotalValueTrade
        && A.PrevClosePx == B.PrevClosePx
        && A.LastPx == B.LastPx
        && A.OpenPx == B.OpenPx
        && A.HighPx == B.HighPx
        && A.LowPx == B.LowPx
        && A.BidWeightPx == B.BidWeightPx
        && A.BidWeightSize == B.BidWeightSize
        && A.AskWeightPx == B.AskWeightPx
        && A.AskWeightSize == B.AskWeightSize
        && A.UpLimitPx == B.UpLimitPx
        && A.DnLimitPx == B.DnLimitPx
        && A.BidLevel[0].Price == B.BidLevel[0].Price
        && A.BidLevel[0].Qty == B.BidLevel[0].Qty
        && A.BidLevel[1].Price == B.BidLevel[1].Price
        && A.BidLevel[1].Qty == B.BidLevel[1].Qty
        && A.BidLevel[2].Price == B.BidLevel[2].Price
        && A.BidLevel[2].Qty == B.BidLevel[2].Qty
        && A.BidLevel[3].Price == B.BidLevel[3].Price
        && A.BidLevel[3].Qty == B.BidLevel[3].Qty
        && A.BidLevel[4].Price == B.BidLevel[4].Price
        && A.BidLevel[4].Qty == B.BidLevel[4].Qty
        && A.BidLevel[5].Price == B.BidLevel[5].Price
        && A.BidLevel[5].Qty == B.BidLevel[5].Qty
        && A.BidLevel[6].Price == B.BidLevel[6].Price
        && A.BidLevel[6].Qty == B.BidLevel[6].Qty
        && A.BidLevel[7].Price == B.BidLevel[7].Price
        && A.BidLevel[7].Qty == B.BidLevel[7].Qty
        && A.BidLevel[8].Price == B.BidLevel[8].Price
        && A.BidLevel[8].Qty == B.BidLevel[8].Qty
        && A.BidLevel[9].Price == B.BidLevel[9].Price
        && A.BidLevel[9].Qty == B.BidLevel[9].Qty
        && A.AskLevel[0].Price == B.AskLevel[0].Price
        && A.AskLevel[0].Qty == B.AskLevel[0].Qty
        && A.AskLevel[1].Price == B.AskLevel[1].Price
        && A.AskLevel[1].Qty == B.AskLevel[1].Qty
        && A.AskLevel[2].Price == B.AskLevel[2].Price
        && A.AskLevel[2].Qty == B.AskLevel[2].Qty
        && A.AskLevel[3].Price == B.AskLevel[3].Price
        && A.AskLevel[3].Qty == B.AskLevel[3].Qty
        && A.AskLevel[4].Price == B.AskLevel[4].Price
        && A.AskLevel[4].Qty == B.AskLevel[4].Qty
        && A.AskLevel[5].Price == B.AskLevel[5].Price
        && A.AskLevel[5].Qty == B.AskLevel[5].Qty
        && A.AskLevel[6].Price == B.AskLevel[6].Price
        && A.AskLevel[6].Qty == B.AskLevel[6].Qty
        && A.AskLevel[7].Price == B.AskLevel[7].Price
        && A.AskLevel[7].Qty == B.AskLevel[7].Qty
        && A.AskLevel[8].Price == B.AskLevel[8].Price
        && A.AskLevel[8].Qty == B.AskLevel[8].Qty
        && A.AskLevel[9].Price == B.AskLevel[9].Price
        && A.AskLevel[9].Qty == B.AskLevel[9].Qty
        && A.TransactTime == B.TransactTime
        && A.Resv[0] == B.Resv[0]
        && A.Resv[1] == B.Resv[1]
        && A.Resv[2] == B.Resv[2]
        && A.Resv[3] == B.Resv[3]
        ;
}
bool operator==(const SBE_SSZ_index_snap_t& A, const SBE_SSZ_index_snap_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.NumTrades == B.NumTrades
        && A.TotalVolumeTrade == B.TotalVolumeTrade
        && A.TotalValueTrade == B.TotalValueTrade
        && A.PrevClosePx == B.PrevClosePx
        && A.LastPx == B.LastPx
        && A.OpenPx == B.OpenPx
        && A.HighPx == B.HighPx
        && A.LowPx == B.LowPx
        && A.TransactTime == B.TransactTime
        ;
}
bool operator==(const SBE_SSZ_ord_t& A, const SBE_SSZ_ord_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.Price == B.Price
        && A.OrderQty == B.OrderQty
        && A.Side == B.Side
        && A.OrdType == B.OrdType
        && A.TransactTime == B.TransactTime
        && A.Resv[0] == B.Resv[0]
        && A.Resv[1] == B.Resv[1]
        ;
}
bool operator==(const SBE_SSZ_exe_t& A, const SBE_SSZ_exe_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.BidApplSeqNum == B.BidApplSeqNum
        && A.OfferApplSeqNum == B.OfferApplSeqNum
        && A.LastPx == B.LastPx
        && A.LastQty == B.LastQty
        && A.ExecType == B.ExecType
        && A.TransactTime == B.TransactTime
        && A.Resv[0] == B.Resv[0]
        && A.Resv[1] == B.Resv[1]
        && A.Resv[2] == B.Resv[2]
        ;
}
bool operator==(const SBE_SSZ_option_snap_t& A, const SBE_SSZ_option_snap_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.NumTrades == B.NumTrades
        && A.TotalVolumeTrade == B.TotalVolumeTrade
        && A.TotalValueTrade == B.TotalValueTrade
        && A.PrevClosePx == B.PrevClosePx
        && A.LastPx == B.LastPx
        && A.OpenPx == B.OpenPx
        && A.HighPx == B.HighPx
        && A.LowPx == B.LowPx
        && A.BidWeightPx == B.BidWeightPx
        && A.BidWeightSize == B.BidWeightSize
        && A.AskWeightPx == B.AskWeightPx
        && A.AskWeightSize == B.AskWeightSize
        && A.UpLimitPx == B.UpLimitPx
        && A.DnLimitPx == B.DnLimitPx
        && A.ContractPos == B.ContractPos
        && A.RefPx == B.RefPx
        && A.BidLevel[0].Price == B.BidLevel[0].Price
        && A.BidLevel[0].Qty == B.BidLevel[0].Qty
        && A.BidLevel[1].Price == B.BidLevel[1].Price
        && A.BidLevel[1].Qty == B.BidLevel[1].Qty
        && A.BidLevel[2].Price == B.BidLevel[2].Price
        && A.BidLevel[2].Qty == B.BidLevel[2].Qty
        && A.BidLevel[3].Price == B.BidLevel[3].Price
        && A.BidLevel[3].Qty == B.BidLevel[3].Qty
        && A.BidLevel[4].Price == B.BidLevel[4].Price
        && A.BidLevel[4].Qty == B.BidLevel[4].Qty
        && A.BidLevel[5].Price == B.BidLevel[5].Price
        && A.BidLevel[5].Qty == B.BidLevel[5].Qty
        && A.BidLevel[6].Price == B.BidLevel[6].Price
        && A.BidLevel[6].Qty == B.BidLevel[6].Qty
        && A.BidLevel[7].Price == B.BidLevel[7].Price
        && A.BidLevel[7].Qty == B.BidLevel[7].Qty
        && A.BidLevel[8].Price == B.BidLevel[8].Price
        && A.BidLevel[8].Qty == B.BidLevel[8].Qty
        && A.BidLevel[9].Price == B.BidLevel[9].Price
        && A.BidLevel[9].Qty == B.BidLevel[9].Qty
        && A.AskLevel[0].Price == B.AskLevel[0].Price
        && A.AskLevel[0].Qty == B.AskLevel[0].Qty
        && A.AskLevel[1].Price == B.AskLevel[1].Price
        && A.AskLevel[1].Qty == B.AskLevel[1].Qty
        && A.AskLevel[2].Price == B.AskLevel[2].Price
        && A.AskLevel[2].Qty == B.AskLevel[2].Qty
        && A.AskLevel[3].Price == B.AskLevel[3].Price
        && A.AskLevel[3].Qty == B.AskLevel[3].Qty
        && A.AskLevel[4].Price == B.AskLevel[4].Price
        && A.AskLevel[4].Qty == B.AskLevel[4].Qty
        && A.AskLevel[5].Price == B.AskLevel[5].Price
        && A.AskLevel[5].Qty == B.AskLevel[5].Qty
        && A.AskLevel[6].Price == B.AskLevel[6].Price
        && A.AskLevel[6].Qty == B.AskLevel[6].Qty
        && A.AskLevel[7].Price == B.AskLevel[7].Price
        && A.AskLevel[7].Qty == B.AskLevel[7].Qty
        && A.AskLevel[8].Price == B.AskLevel[8].Price
        && A.AskLevel[8].Qty == B.AskLevel[8].Qty
        && A.AskLevel[9].Price == B.AskLevel[9].Price
        && A.AskLevel[9].Qty == B.AskLevel[9].Qty
        && A.TransactTime == B.TransactTime
        ;
}
bool operator==(const SBE_SSZ_fund_snap_t& A, const SBE_SSZ_fund_snap_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.NumTrades == B.NumTrades
        && A.TotalVolumeTrade == B.TotalVolumeTrade
        && A.TotalValueTrade == B.TotalValueTrade
        && A.PrevClosePx == B.PrevClosePx
        && A.LastPx == B.LastPx
        && A.OpenPx == B.OpenPx
        && A.HighPx == B.HighPx
        && A.LowPx == B.LowPx
        && A.BidWeightPx == B.BidWeightPx
        && A.BidWeightSize == B.BidWeightSize
        && A.AskWeightPx == B.AskWeightPx
        && A.AskWeightSize == B.AskWeightSize
        && A.UpLimitPx == B.UpLimitPx
        && A.DnLimitPx == B.DnLimitPx
        && A.BidLevel[0].Price == B.BidLevel[0].Price
        && A.BidLevel[0].Qty == B.BidLevel[0].Qty
        && A.BidLevel[1].Price == B.BidLevel[1].Price
        && A.BidLevel[1].Qty == B.BidLevel[1].Qty
        && A.BidLevel[2].Price == B.BidLevel[2].Price
        && A.BidLevel[2].Qty == B.BidLevel[2].Qty
        && A.BidLevel[3].Price == B.BidLevel[3].Price
        && A.BidLevel[3].Qty == B.BidLevel[3].Qty
        && A.BidLevel[4].Price == B.BidLevel[4].Price
        && A.BidLevel[4].Qty == B.BidLevel[4].Qty
        && A.BidLevel[5].Price == B.BidLevel[5].Price
        && A.BidLevel[5].Qty == B.BidLevel[5].Qty
        && A.BidLevel[6].Price == B.BidLevel[6].Price
        && A.BidLevel[6].Qty == B.BidLevel[6].Qty
        && A.BidLevel[7].Price == B.BidLevel[7].Price
        && A.BidLevel[7].Qty == B.BidLevel[7].Qty
        && A.BidLevel[8].Price == B.BidLevel[8].Price
        && A.BidLevel[8].Qty == B.BidLevel[8].Qty
        && A.BidLevel[9].Price == B.BidLevel[9].Price
        && A.BidLevel[9].Qty == B.BidLevel[9].Qty
        && A.AskLevel[0].Price == B.AskLevel[0].Price
        && A.AskLevel[0].Qty == B.AskLevel[0].Qty
        && A.AskLevel[1].Price == B.AskLevel[1].Price
        && A.AskLevel[1].Qty == B.AskLevel[1].Qty
        && A.AskLevel[2].Price == B.AskLevel[2].Price
        && A.AskLevel[2].Qty == B.AskLevel[2].Qty
        && A.AskLevel[3].Price == B.AskLevel[3].Price
        && A.AskLevel[3].Qty == B.AskLevel[3].Qty
        && A.AskLevel[4].Price == B.AskLevel[4].Price
        && A.AskLevel[4].Qty == B.AskLevel[4].Qty
        && A.AskLevel[5].Price == B.AskLevel[5].Price
        && A.AskLevel[5].Qty == B.AskLevel[5].Qty
        && A.AskLevel[6].Price == B.AskLevel[6].Price
        && A.AskLevel[6].Qty == B.AskLevel[6].Qty
        && A.AskLevel[7].Price == B.AskLevel[7].Price
        && A.AskLevel[7].Qty == B.AskLevel[7].Qty
        && A.AskLevel[8].Price == B.AskLevel[8].Price
        && A.AskLevel[8].Qty == B.AskLevel[8].Qty
        && A.AskLevel[9].Price == B.AskLevel[9].Price
        && A.AskLevel[9].Qty == B.AskLevel[9].Qty
        && A.TransactTime == B.TransactTime
        && A.IOPV == B.IOPV
        ;
}
bool operator==(const SBE_SSZ_bond_snap_t& A, const SBE_SSZ_bond_snap_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.NumTrades == B.NumTrades
        && A.TotalVolumeTrade == B.TotalVolumeTrade
        && A.TotalValueTrade == B.TotalValueTrade
        && A.PrevClosePx == B.PrevClosePx
        && A.LastPx == B.LastPx
        && A.OpenPx == B.OpenPx
        && A.HighPx == B.HighPx
        && A.LowPx == B.LowPx
        && A.BidWeightPx == B.BidWeightPx
        && A.BidWeightSize == B.BidWeightSize
        && A.AskWeightPx == B.AskWeightPx
        && A.AskWeightSize == B.AskWeightSize
        && A.LastPxTradeType == B.LastPxTradeType
        && A.MatchTradeLastPx == B.MatchTradeLastPx
        && A.AuctionVolumeTrade == B.AuctionVolumeTrade
        && A.AuctionValueTrade == B.AuctionValueTrade
        && A.BidLevel[0].Price == B.BidLevel[0].Price
        && A.BidLevel[0].Qty == B.BidLevel[0].Qty
        && A.BidLevel[1].Price == B.BidLevel[1].Price
        && A.BidLevel[1].Qty == B.BidLevel[1].Qty
        && A.BidLevel[2].Price == B.BidLevel[2].Price
        && A.BidLevel[2].Qty == B.BidLevel[2].Qty
        && A.BidLevel[3].Price == B.BidLevel[3].Price
        && A.BidLevel[3].Qty == B.BidLevel[3].Qty
        && A.BidLevel[4].Price == B.BidLevel[4].Price
        && A.BidLevel[4].Qty == B.BidLevel[4].Qty
        && A.BidLevel[5].Price == B.BidLevel[5].Price
        && A.BidLevel[5].Qty == B.BidLevel[5].Qty
        && A.BidLevel[6].Price == B.BidLevel[6].Price
        && A.BidLevel[6].Qty == B.BidLevel[6].Qty
        && A.BidLevel[7].Price == B.BidLevel[7].Price
        && A.BidLevel[7].Qty == B.BidLevel[7].Qty
        && A.BidLevel[8].Price == B.BidLevel[8].Price
        && A.BidLevel[8].Qty == B.BidLevel[8].Qty
        && A.BidLevel[9].Price == B.BidLevel[9].Price
        && A.BidLevel[9].Qty == B.BidLevel[9].Qty
        && A.AskLevel[0].Price == B.AskLevel[0].Price
        && A.AskLevel[0].Qty == B.AskLevel[0].Qty
        && A.AskLevel[1].Price == B.AskLevel[1].Price
        && A.AskLevel[1].Qty == B.AskLevel[1].Qty
        && A.AskLevel[2].Price == B.AskLevel[2].Price
        && A.AskLevel[2].Qty == B.AskLevel[2].Qty
        && A.AskLevel[3].Price == B.AskLevel[3].Price
        && A.AskLevel[3].Qty == B.AskLevel[3].Qty
        && A.AskLevel[4].Price == B.AskLevel[4].Price
        && A.AskLevel[4].Qty == B.AskLevel[4].Qty
        && A.AskLevel[5].Price == B.AskLevel[5].Price
        && A.AskLevel[5].Qty == B.AskLevel[5].Qty
        && A.AskLevel[6].Price == B.AskLevel[6].Price
        && A.AskLevel[6].Qty == B.AskLevel[6].Qty
        && A.AskLevel[7].Price == B.AskLevel[7].Price
        && A.AskLevel[7].Qty == B.AskLevel[7].Qty
        && A.AskLevel[8].Price == B.AskLevel[8].Price
        && A.AskLevel[8].Qty == B.AskLevel[8].Qty
        && A.AskLevel[9].Price == B.AskLevel[9].Price
        && A.AskLevel[9].Qty == B.AskLevel[9].Qty
        && A.TransactTime == B.TransactTime
        && A.Resv[0] == B.Resv[0]
        && A.Resv[1] == B.Resv[1]
        && A.Resv[2] == B.Resv[2]
        && A.Resv[3] == B.Resv[3]
        ;
}
bool operator==(const SBE_SSZ_bond_ord_t& A, const SBE_SSZ_bond_ord_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.Price == B.Price
        && A.OrderQty == B.OrderQty
        && A.Side == B.Side
        && A.OrdType == B.OrdType
        && A.TransactTime == B.TransactTime
        && A.Resv[0] == B.Resv[0]
        && A.Resv[1] == B.Resv[1]
        ;
}
bool operator==(const SBE_SSZ_bond_exe_t& A, const SBE_SSZ_bond_exe_t& B){
    return A.Header.SecurityIDSource == B.Header.SecurityIDSource
        && A.Header.MsgType == B.Header.MsgType
        && A.Header.MsgLen == B.Header.MsgLen
        && A.Header.SecurityID[0] == B.Header.SecurityID[0]
        && A.Header.SecurityID[1] == B.Header.SecurityID[1]
        && A.Header.SecurityID[2] == B.Header.SecurityID[2]
        && A.Header.SecurityID[3] == B.Header.SecurityID[3]
        && A.Header.SecurityID[4] == B.Header.SecurityID[4]
        && A.Header.SecurityID[5] == B.Header.SecurityID[5]
        && A.Header.SecurityID[6] == B.Header.SecurityID[6]
        && A.Header.SecurityID[7] == B.Header.SecurityID[7]
        && A.Header.SecurityID[8] == B.Header.SecurityID[8]
        && A.Header.ChannelNo == B.Header.ChannelNo
        && A.Header.ApplSeqNum == B.Header.ApplSeqNum
        && A.Header.TradingPhase.Code0 == B.Header.TradingPhase.Code0
        && A.Header.TradingPhase.Code1 == B.Header.TradingPhase.Code1
        && A.BidApplSeqNum == B.BidApplSeqNum
        && A.OfferApplSeqNum == B.OfferApplSeqNum
        && A.LastPx == B.LastPx
        && A.LastQty == B.LastQty
        && A.ExecType == B.ExecType
        && A.TransactTime == B.TransactTime
        && A.Resv[0] == B.Resv[0]
        && A.Resv[1] == B.Resv[1]
        && A.Resv[2] == B.Resv[2]
        ;
}
