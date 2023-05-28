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
void sbe_intf::QtyQueue_level_t_unpack(QtyQueue_level_t_packed &src,
                          QtyQueue_level_t &dest)
{
#pragma HLS INLINE

    dest.NoOrders = src.range(807, 800);
    dest.QtyQueue[0] = reverse<16>(src.range(799, 784));
    dest.QtyQueue[1] = reverse<16>(src.range(783, 768));
    dest.QtyQueue[2] = reverse<16>(src.range(767, 752));
    dest.QtyQueue[3] = reverse<16>(src.range(751, 736));
    dest.QtyQueue[4] = reverse<16>(src.range(735, 720));
    dest.QtyQueue[5] = reverse<16>(src.range(719, 704));
    dest.QtyQueue[6] = reverse<16>(src.range(703, 688));
    dest.QtyQueue[7] = reverse<16>(src.range(687, 672));
    dest.QtyQueue[8] = reverse<16>(src.range(671, 656));
    dest.QtyQueue[9] = reverse<16>(src.range(655, 640));
    dest.QtyQueue[10] = reverse<16>(src.range(639, 624));
    dest.QtyQueue[11] = reverse<16>(src.range(623, 608));
    dest.QtyQueue[12] = reverse<16>(src.range(607, 592));
    dest.QtyQueue[13] = reverse<16>(src.range(591, 576));
    dest.QtyQueue[14] = reverse<16>(src.range(575, 560));
    dest.QtyQueue[15] = reverse<16>(src.range(559, 544));
    dest.QtyQueue[16] = reverse<16>(src.range(543, 528));
    dest.QtyQueue[17] = reverse<16>(src.range(527, 512));
    dest.QtyQueue[18] = reverse<16>(src.range(511, 496));
    dest.QtyQueue[19] = reverse<16>(src.range(495, 480));
    dest.QtyQueue[20] = reverse<16>(src.range(479, 464));
    dest.QtyQueue[21] = reverse<16>(src.range(463, 448));
    dest.QtyQueue[22] = reverse<16>(src.range(447, 432));
    dest.QtyQueue[23] = reverse<16>(src.range(431, 416));
    dest.QtyQueue[24] = reverse<16>(src.range(415, 400));
    dest.QtyQueue[25] = reverse<16>(src.range(399, 384));
    dest.QtyQueue[26] = reverse<16>(src.range(383, 368));
    dest.QtyQueue[27] = reverse<16>(src.range(367, 352));
    dest.QtyQueue[28] = reverse<16>(src.range(351, 336));
    dest.QtyQueue[29] = reverse<16>(src.range(335, 320));
    dest.QtyQueue[30] = reverse<16>(src.range(319, 304));
    dest.QtyQueue[31] = reverse<16>(src.range(303, 288));
    dest.QtyQueue[32] = reverse<16>(src.range(287, 272));
    dest.QtyQueue[33] = reverse<16>(src.range(271, 256));
    dest.QtyQueue[34] = reverse<16>(src.range(255, 240));
    dest.QtyQueue[35] = reverse<16>(src.range(239, 224));
    dest.QtyQueue[36] = reverse<16>(src.range(223, 208));
    dest.QtyQueue[37] = reverse<16>(src.range(207, 192));
    dest.QtyQueue[38] = reverse<16>(src.range(191, 176));
    dest.QtyQueue[39] = reverse<16>(src.range(175, 160));
    dest.QtyQueue[40] = reverse<16>(src.range(159, 144));
    dest.QtyQueue[41] = reverse<16>(src.range(143, 128));
    dest.QtyQueue[42] = reverse<16>(src.range(127, 112));
    dest.QtyQueue[43] = reverse<16>(src.range(111, 96));
    dest.QtyQueue[44] = reverse<16>(src.range(95, 80));
    dest.QtyQueue[45] = reverse<16>(src.range(79, 64));
    dest.QtyQueue[46] = reverse<16>(src.range(63, 48));
    dest.QtyQueue[47] = reverse<16>(src.range(47, 32));
    dest.QtyQueue[48] = reverse<16>(src.range(31, 16));
    dest.QtyQueue[49] = reverse<16>(src.range(15, 0));
}
void sbe_intf::QtyQueue_level_t_pack(QtyQueue_level_t &src,
                          QtyQueue_level_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(807, 800) = src.NoOrders;
    dest.range(799, 784) = reverse<16>(src.QtyQueue[0]);
    dest.range(783, 768) = reverse<16>(src.QtyQueue[1]);
    dest.range(767, 752) = reverse<16>(src.QtyQueue[2]);
    dest.range(751, 736) = reverse<16>(src.QtyQueue[3]);
    dest.range(735, 720) = reverse<16>(src.QtyQueue[4]);
    dest.range(719, 704) = reverse<16>(src.QtyQueue[5]);
    dest.range(703, 688) = reverse<16>(src.QtyQueue[6]);
    dest.range(687, 672) = reverse<16>(src.QtyQueue[7]);
    dest.range(671, 656) = reverse<16>(src.QtyQueue[8]);
    dest.range(655, 640) = reverse<16>(src.QtyQueue[9]);
    dest.range(639, 624) = reverse<16>(src.QtyQueue[10]);
    dest.range(623, 608) = reverse<16>(src.QtyQueue[11]);
    dest.range(607, 592) = reverse<16>(src.QtyQueue[12]);
    dest.range(591, 576) = reverse<16>(src.QtyQueue[13]);
    dest.range(575, 560) = reverse<16>(src.QtyQueue[14]);
    dest.range(559, 544) = reverse<16>(src.QtyQueue[15]);
    dest.range(543, 528) = reverse<16>(src.QtyQueue[16]);
    dest.range(527, 512) = reverse<16>(src.QtyQueue[17]);
    dest.range(511, 496) = reverse<16>(src.QtyQueue[18]);
    dest.range(495, 480) = reverse<16>(src.QtyQueue[19]);
    dest.range(479, 464) = reverse<16>(src.QtyQueue[20]);
    dest.range(463, 448) = reverse<16>(src.QtyQueue[21]);
    dest.range(447, 432) = reverse<16>(src.QtyQueue[22]);
    dest.range(431, 416) = reverse<16>(src.QtyQueue[23]);
    dest.range(415, 400) = reverse<16>(src.QtyQueue[24]);
    dest.range(399, 384) = reverse<16>(src.QtyQueue[25]);
    dest.range(383, 368) = reverse<16>(src.QtyQueue[26]);
    dest.range(367, 352) = reverse<16>(src.QtyQueue[27]);
    dest.range(351, 336) = reverse<16>(src.QtyQueue[28]);
    dest.range(335, 320) = reverse<16>(src.QtyQueue[29]);
    dest.range(319, 304) = reverse<16>(src.QtyQueue[30]);
    dest.range(303, 288) = reverse<16>(src.QtyQueue[31]);
    dest.range(287, 272) = reverse<16>(src.QtyQueue[32]);
    dest.range(271, 256) = reverse<16>(src.QtyQueue[33]);
    dest.range(255, 240) = reverse<16>(src.QtyQueue[34]);
    dest.range(239, 224) = reverse<16>(src.QtyQueue[35]);
    dest.range(223, 208) = reverse<16>(src.QtyQueue[36]);
    dest.range(207, 192) = reverse<16>(src.QtyQueue[37]);
    dest.range(191, 176) = reverse<16>(src.QtyQueue[38]);
    dest.range(175, 160) = reverse<16>(src.QtyQueue[39]);
    dest.range(159, 144) = reverse<16>(src.QtyQueue[40]);
    dest.range(143, 128) = reverse<16>(src.QtyQueue[41]);
    dest.range(127, 112) = reverse<16>(src.QtyQueue[42]);
    dest.range(111, 96) = reverse<16>(src.QtyQueue[43]);
    dest.range(95, 80) = reverse<16>(src.QtyQueue[44]);
    dest.range(79, 64) = reverse<16>(src.QtyQueue[45]);
    dest.range(63, 48) = reverse<16>(src.QtyQueue[46]);
    dest.range(47, 32) = reverse<16>(src.QtyQueue[47]);
    dest.range(31, 16) = reverse<16>(src.QtyQueue[48]);
    dest.range(15, 0) = reverse<16>(src.QtyQueue[49]);
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
void sbe_intf::SBE_SSZ_index_snap_t_unpack(SBE_SSZ_index_snap_t_packed &src,
                          SBE_SSZ_index_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(767, 760);
    dest.Header.MsgType = src.range(759, 752);
    dest.Header.MsgLen = reverse<16>(src.range(751, 736));
    dest.Header.SecurityID[0] = src.range(735, 728);
    dest.Header.SecurityID[1] = src.range(727, 720);
    dest.Header.SecurityID[2] = src.range(719, 712);
    dest.Header.SecurityID[3] = src.range(711, 704);
    dest.Header.SecurityID[4] = src.range(703, 696);
    dest.Header.SecurityID[5] = src.range(695, 688);
    dest.Header.SecurityID[6] = src.range(687, 680);
    dest.Header.SecurityID[7] = src.range(679, 672);
    dest.Header.SecurityID[8] = src.range(671, 664);
    dest.Header.ChannelNo = reverse<16>(src.range(663, 648));
    dest.Header.ApplSeqNum = reverse<64>(src.range(647, 584));
    dest.Header.TradingPhase.Code0 = src.range(583, 580);
    dest.Header.TradingPhase.Code1 = src.range(579, 576);
    dest.NumTrades = reverse<64>(src.range(575, 512));
    dest.TotalVolumeTrade = reverse<64>(src.range(511, 448));
    dest.TotalValueTrade = reverse<64>(src.range(447, 384));
    dest.PrevClosePx = reverse<64>(src.range(383, 320));
    dest.LastPx = reverse<64>(src.range(319, 256));
    dest.OpenPx = reverse<64>(src.range(255, 192));
    dest.HighPx = reverse<64>(src.range(191, 128));
    dest.LowPx = reverse<64>(src.range(127, 64));
    dest.TransactTime = reverse<64>(src.range(63, 0));
}
void sbe_intf::SBE_SSZ_index_snap_t_pack(SBE_SSZ_index_snap_t &src,
                          SBE_SSZ_index_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(767, 760) = src.Header.SecurityIDSource;
    dest.range(759, 752) = src.Header.MsgType;
    dest.range(751, 736) = reverse<16>(src.Header.MsgLen);
    dest.range(735, 728) = src.Header.SecurityID[0];
    dest.range(727, 720) = src.Header.SecurityID[1];
    dest.range(719, 712) = src.Header.SecurityID[2];
    dest.range(711, 704) = src.Header.SecurityID[3];
    dest.range(703, 696) = src.Header.SecurityID[4];
    dest.range(695, 688) = src.Header.SecurityID[5];
    dest.range(687, 680) = src.Header.SecurityID[6];
    dest.range(679, 672) = src.Header.SecurityID[7];
    dest.range(671, 664) = src.Header.SecurityID[8];
    dest.range(663, 648) = reverse<16>(src.Header.ChannelNo);
    dest.range(647, 584) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(583, 580) = src.Header.TradingPhase.Code0;
    dest.range(579, 576) = src.Header.TradingPhase.Code1;
    dest.range(575, 512) = reverse<64>(src.NumTrades);
    dest.range(511, 448) = reverse<64>(src.TotalVolumeTrade);
    dest.range(447, 384) = reverse<64>(src.TotalValueTrade);
    dest.range(383, 320) = reverse<64>(src.PrevClosePx);
    dest.range(319, 256) = reverse<64>(src.LastPx);
    dest.range(255, 192) = reverse<64>(src.OpenPx);
    dest.range(191, 128) = reverse<64>(src.HighPx);
    dest.range(127, 64) = reverse<64>(src.LowPx);
    dest.range(63, 0) = reverse<64>(src.TransactTime);
}
void sbe_intf::SBE_SSZ_ord_t_unpack(SBE_SSZ_ord_t_packed &src,
                          SBE_SSZ_ord_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(383, 376);
    dest.Header.MsgType = src.range(375, 368);
    dest.Header.MsgLen = reverse<16>(src.range(367, 352));
    dest.Header.SecurityID[0] = src.range(351, 344);
    dest.Header.SecurityID[1] = src.range(343, 336);
    dest.Header.SecurityID[2] = src.range(335, 328);
    dest.Header.SecurityID[3] = src.range(327, 320);
    dest.Header.SecurityID[4] = src.range(319, 312);
    dest.Header.SecurityID[5] = src.range(311, 304);
    dest.Header.SecurityID[6] = src.range(303, 296);
    dest.Header.SecurityID[7] = src.range(295, 288);
    dest.Header.SecurityID[8] = src.range(287, 280);
    dest.Header.ChannelNo = reverse<16>(src.range(279, 264));
    dest.Header.ApplSeqNum = reverse<64>(src.range(263, 200));
    dest.Header.TradingPhase.Code0 = src.range(199, 196);
    dest.Header.TradingPhase.Code1 = src.range(195, 192);
    dest.Price = reverse<32>(src.range(191, 160));
    dest.OrderQty = reverse<64>(src.range(159, 96));
    dest.Side = src.range(95, 88);
    dest.OrdType = src.range(87, 80);
    dest.TransactTime = reverse<64>(src.range(79, 16));
    dest.Resv[0] = src.range(15, 8);
    dest.Resv[1] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_ord_t_pack(SBE_SSZ_ord_t &src,
                          SBE_SSZ_ord_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(383, 376) = src.Header.SecurityIDSource;
    dest.range(375, 368) = src.Header.MsgType;
    dest.range(367, 352) = reverse<16>(src.Header.MsgLen);
    dest.range(351, 344) = src.Header.SecurityID[0];
    dest.range(343, 336) = src.Header.SecurityID[1];
    dest.range(335, 328) = src.Header.SecurityID[2];
    dest.range(327, 320) = src.Header.SecurityID[3];
    dest.range(319, 312) = src.Header.SecurityID[4];
    dest.range(311, 304) = src.Header.SecurityID[5];
    dest.range(303, 296) = src.Header.SecurityID[6];
    dest.range(295, 288) = src.Header.SecurityID[7];
    dest.range(287, 280) = src.Header.SecurityID[8];
    dest.range(279, 264) = reverse<16>(src.Header.ChannelNo);
    dest.range(263, 200) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(199, 196) = src.Header.TradingPhase.Code0;
    dest.range(195, 192) = src.Header.TradingPhase.Code1;
    dest.range(191, 160) = reverse<32>(src.Price);
    dest.range(159, 96) = reverse<64>(src.OrderQty);
    dest.range(95, 88) = src.Side;
    dest.range(87, 80) = src.OrdType;
    dest.range(79, 16) = reverse<64>(src.TransactTime);
    dest.range(15, 8) = src.Resv[0];
    dest.range(7, 0) = src.Resv[1];
}
void sbe_intf::SBE_SSZ_exe_t_unpack(SBE_SSZ_exe_t_packed &src,
                          SBE_SSZ_exe_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(511, 504);
    dest.Header.MsgType = src.range(503, 496);
    dest.Header.MsgLen = reverse<16>(src.range(495, 480));
    dest.Header.SecurityID[0] = src.range(479, 472);
    dest.Header.SecurityID[1] = src.range(471, 464);
    dest.Header.SecurityID[2] = src.range(463, 456);
    dest.Header.SecurityID[3] = src.range(455, 448);
    dest.Header.SecurityID[4] = src.range(447, 440);
    dest.Header.SecurityID[5] = src.range(439, 432);
    dest.Header.SecurityID[6] = src.range(431, 424);
    dest.Header.SecurityID[7] = src.range(423, 416);
    dest.Header.SecurityID[8] = src.range(415, 408);
    dest.Header.ChannelNo = reverse<16>(src.range(407, 392));
    dest.Header.ApplSeqNum = reverse<64>(src.range(391, 328));
    dest.Header.TradingPhase.Code0 = src.range(327, 324);
    dest.Header.TradingPhase.Code1 = src.range(323, 320);
    dest.BidApplSeqNum = reverse<64>(src.range(319, 256));
    dest.OfferApplSeqNum = reverse<64>(src.range(255, 192));
    dest.LastPx = reverse<32>(src.range(191, 160));
    dest.LastQty = reverse<64>(src.range(159, 96));
    dest.ExecType = src.range(95, 88);
    dest.TransactTime = reverse<64>(src.range(87, 24));
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
    dest.range(495, 480) = reverse<16>(src.Header.MsgLen);
    dest.range(479, 472) = src.Header.SecurityID[0];
    dest.range(471, 464) = src.Header.SecurityID[1];
    dest.range(463, 456) = src.Header.SecurityID[2];
    dest.range(455, 448) = src.Header.SecurityID[3];
    dest.range(447, 440) = src.Header.SecurityID[4];
    dest.range(439, 432) = src.Header.SecurityID[5];
    dest.range(431, 424) = src.Header.SecurityID[6];
    dest.range(423, 416) = src.Header.SecurityID[7];
    dest.range(415, 408) = src.Header.SecurityID[8];
    dest.range(407, 392) = reverse<16>(src.Header.ChannelNo);
    dest.range(391, 328) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(327, 324) = src.Header.TradingPhase.Code0;
    dest.range(323, 320) = src.Header.TradingPhase.Code1;
    dest.range(319, 256) = reverse<64>(src.BidApplSeqNum);
    dest.range(255, 192) = reverse<64>(src.OfferApplSeqNum);
    dest.range(191, 160) = reverse<32>(src.LastPx);
    dest.range(159, 96) = reverse<64>(src.LastQty);
    dest.range(95, 88) = src.ExecType;
    dest.range(87, 24) = reverse<64>(src.TransactTime);
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
    dest.Header.MsgLen = reverse<16>(src.range(2863, 2848));
    dest.Header.SecurityID[0] = src.range(2847, 2840);
    dest.Header.SecurityID[1] = src.range(2839, 2832);
    dest.Header.SecurityID[2] = src.range(2831, 2824);
    dest.Header.SecurityID[3] = src.range(2823, 2816);
    dest.Header.SecurityID[4] = src.range(2815, 2808);
    dest.Header.SecurityID[5] = src.range(2807, 2800);
    dest.Header.SecurityID[6] = src.range(2799, 2792);
    dest.Header.SecurityID[7] = src.range(2791, 2784);
    dest.Header.SecurityID[8] = src.range(2783, 2776);
    dest.Header.ChannelNo = reverse<16>(src.range(2775, 2760));
    dest.Header.ApplSeqNum = reverse<64>(src.range(2759, 2696));
    dest.Header.TradingPhase.Code0 = src.range(2695, 2692);
    dest.Header.TradingPhase.Code1 = src.range(2691, 2688);
    dest.NumTrades = reverse<64>(src.range(2687, 2624));
    dest.TotalVolumeTrade = reverse<64>(src.range(2623, 2560));
    dest.TotalValueTrade = reverse<64>(src.range(2559, 2496));
    dest.PrevClosePx = reverse<32>(src.range(2495, 2464));
    dest.LastPx = reverse<32>(src.range(2463, 2432));
    dest.OpenPx = reverse<32>(src.range(2431, 2400));
    dest.HighPx = reverse<32>(src.range(2399, 2368));
    dest.LowPx = reverse<32>(src.range(2367, 2336));
    dest.BidWeightPx = reverse<32>(src.range(2335, 2304));
    dest.BidWeightSize = reverse<64>(src.range(2303, 2240));
    dest.AskWeightPx = reverse<32>(src.range(2239, 2208));
    dest.AskWeightSize = reverse<64>(src.range(2207, 2144));
    dest.UpLimitPx = reverse<32>(src.range(2143, 2112));
    dest.DnLimitPx = reverse<32>(src.range(2111, 2080));
    dest.ContractPos = reverse<64>(src.range(2079, 2016));
    dest.RefPx = reverse<32>(src.range(2015, 1984));
    dest.BidLevel[0].Price = reverse<32>(src.range(1983, 1952));
    dest.BidLevel[0].Qty = reverse<64>(src.range(1951, 1888));
    dest.BidLevel[1].Price = reverse<32>(src.range(1887, 1856));
    dest.BidLevel[1].Qty = reverse<64>(src.range(1855, 1792));
    dest.BidLevel[2].Price = reverse<32>(src.range(1791, 1760));
    dest.BidLevel[2].Qty = reverse<64>(src.range(1759, 1696));
    dest.BidLevel[3].Price = reverse<32>(src.range(1695, 1664));
    dest.BidLevel[3].Qty = reverse<64>(src.range(1663, 1600));
    dest.BidLevel[4].Price = reverse<32>(src.range(1599, 1568));
    dest.BidLevel[4].Qty = reverse<64>(src.range(1567, 1504));
    dest.BidLevel[5].Price = reverse<32>(src.range(1503, 1472));
    dest.BidLevel[5].Qty = reverse<64>(src.range(1471, 1408));
    dest.BidLevel[6].Price = reverse<32>(src.range(1407, 1376));
    dest.BidLevel[6].Qty = reverse<64>(src.range(1375, 1312));
    dest.BidLevel[7].Price = reverse<32>(src.range(1311, 1280));
    dest.BidLevel[7].Qty = reverse<64>(src.range(1279, 1216));
    dest.BidLevel[8].Price = reverse<32>(src.range(1215, 1184));
    dest.BidLevel[8].Qty = reverse<64>(src.range(1183, 1120));
    dest.BidLevel[9].Price = reverse<32>(src.range(1119, 1088));
    dest.BidLevel[9].Qty = reverse<64>(src.range(1087, 1024));
    dest.AskLevel[0].Price = reverse<32>(src.range(1023, 992));
    dest.AskLevel[0].Qty = reverse<64>(src.range(991, 928));
    dest.AskLevel[1].Price = reverse<32>(src.range(927, 896));
    dest.AskLevel[1].Qty = reverse<64>(src.range(895, 832));
    dest.AskLevel[2].Price = reverse<32>(src.range(831, 800));
    dest.AskLevel[2].Qty = reverse<64>(src.range(799, 736));
    dest.AskLevel[3].Price = reverse<32>(src.range(735, 704));
    dest.AskLevel[3].Qty = reverse<64>(src.range(703, 640));
    dest.AskLevel[4].Price = reverse<32>(src.range(639, 608));
    dest.AskLevel[4].Qty = reverse<64>(src.range(607, 544));
    dest.AskLevel[5].Price = reverse<32>(src.range(543, 512));
    dest.AskLevel[5].Qty = reverse<64>(src.range(511, 448));
    dest.AskLevel[6].Price = reverse<32>(src.range(447, 416));
    dest.AskLevel[6].Qty = reverse<64>(src.range(415, 352));
    dest.AskLevel[7].Price = reverse<32>(src.range(351, 320));
    dest.AskLevel[7].Qty = reverse<64>(src.range(319, 256));
    dest.AskLevel[8].Price = reverse<32>(src.range(255, 224));
    dest.AskLevel[8].Qty = reverse<64>(src.range(223, 160));
    dest.AskLevel[9].Price = reverse<32>(src.range(159, 128));
    dest.AskLevel[9].Qty = reverse<64>(src.range(127, 64));
    dest.TransactTime = reverse<64>(src.range(63, 0));
}
void sbe_intf::SBE_SSZ_option_snap_t_pack(SBE_SSZ_option_snap_t &src,
                          SBE_SSZ_option_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(2879, 2872) = src.Header.SecurityIDSource;
    dest.range(2871, 2864) = src.Header.MsgType;
    dest.range(2863, 2848) = reverse<16>(src.Header.MsgLen);
    dest.range(2847, 2840) = src.Header.SecurityID[0];
    dest.range(2839, 2832) = src.Header.SecurityID[1];
    dest.range(2831, 2824) = src.Header.SecurityID[2];
    dest.range(2823, 2816) = src.Header.SecurityID[3];
    dest.range(2815, 2808) = src.Header.SecurityID[4];
    dest.range(2807, 2800) = src.Header.SecurityID[5];
    dest.range(2799, 2792) = src.Header.SecurityID[6];
    dest.range(2791, 2784) = src.Header.SecurityID[7];
    dest.range(2783, 2776) = src.Header.SecurityID[8];
    dest.range(2775, 2760) = reverse<16>(src.Header.ChannelNo);
    dest.range(2759, 2696) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(2695, 2692) = src.Header.TradingPhase.Code0;
    dest.range(2691, 2688) = src.Header.TradingPhase.Code1;
    dest.range(2687, 2624) = reverse<64>(src.NumTrades);
    dest.range(2623, 2560) = reverse<64>(src.TotalVolumeTrade);
    dest.range(2559, 2496) = reverse<64>(src.TotalValueTrade);
    dest.range(2495, 2464) = reverse<32>(src.PrevClosePx);
    dest.range(2463, 2432) = reverse<32>(src.LastPx);
    dest.range(2431, 2400) = reverse<32>(src.OpenPx);
    dest.range(2399, 2368) = reverse<32>(src.HighPx);
    dest.range(2367, 2336) = reverse<32>(src.LowPx);
    dest.range(2335, 2304) = reverse<32>(src.BidWeightPx);
    dest.range(2303, 2240) = reverse<64>(src.BidWeightSize);
    dest.range(2239, 2208) = reverse<32>(src.AskWeightPx);
    dest.range(2207, 2144) = reverse<64>(src.AskWeightSize);
    dest.range(2143, 2112) = reverse<32>(src.UpLimitPx);
    dest.range(2111, 2080) = reverse<32>(src.DnLimitPx);
    dest.range(2079, 2016) = reverse<64>(src.ContractPos);
    dest.range(2015, 1984) = reverse<32>(src.RefPx);
    dest.range(1983, 1952) = reverse<32>(src.BidLevel[0].Price);
    dest.range(1951, 1888) = reverse<64>(src.BidLevel[0].Qty);
    dest.range(1887, 1856) = reverse<32>(src.BidLevel[1].Price);
    dest.range(1855, 1792) = reverse<64>(src.BidLevel[1].Qty);
    dest.range(1791, 1760) = reverse<32>(src.BidLevel[2].Price);
    dest.range(1759, 1696) = reverse<64>(src.BidLevel[2].Qty);
    dest.range(1695, 1664) = reverse<32>(src.BidLevel[3].Price);
    dest.range(1663, 1600) = reverse<64>(src.BidLevel[3].Qty);
    dest.range(1599, 1568) = reverse<32>(src.BidLevel[4].Price);
    dest.range(1567, 1504) = reverse<64>(src.BidLevel[4].Qty);
    dest.range(1503, 1472) = reverse<32>(src.BidLevel[5].Price);
    dest.range(1471, 1408) = reverse<64>(src.BidLevel[5].Qty);
    dest.range(1407, 1376) = reverse<32>(src.BidLevel[6].Price);
    dest.range(1375, 1312) = reverse<64>(src.BidLevel[6].Qty);
    dest.range(1311, 1280) = reverse<32>(src.BidLevel[7].Price);
    dest.range(1279, 1216) = reverse<64>(src.BidLevel[7].Qty);
    dest.range(1215, 1184) = reverse<32>(src.BidLevel[8].Price);
    dest.range(1183, 1120) = reverse<64>(src.BidLevel[8].Qty);
    dest.range(1119, 1088) = reverse<32>(src.BidLevel[9].Price);
    dest.range(1087, 1024) = reverse<64>(src.BidLevel[9].Qty);
    dest.range(1023, 992) = reverse<32>(src.AskLevel[0].Price);
    dest.range(991, 928) = reverse<64>(src.AskLevel[0].Qty);
    dest.range(927, 896) = reverse<32>(src.AskLevel[1].Price);
    dest.range(895, 832) = reverse<64>(src.AskLevel[1].Qty);
    dest.range(831, 800) = reverse<32>(src.AskLevel[2].Price);
    dest.range(799, 736) = reverse<64>(src.AskLevel[2].Qty);
    dest.range(735, 704) = reverse<32>(src.AskLevel[3].Price);
    dest.range(703, 640) = reverse<64>(src.AskLevel[3].Qty);
    dest.range(639, 608) = reverse<32>(src.AskLevel[4].Price);
    dest.range(607, 544) = reverse<64>(src.AskLevel[4].Qty);
    dest.range(543, 512) = reverse<32>(src.AskLevel[5].Price);
    dest.range(511, 448) = reverse<64>(src.AskLevel[5].Qty);
    dest.range(447, 416) = reverse<32>(src.AskLevel[6].Price);
    dest.range(415, 352) = reverse<64>(src.AskLevel[6].Qty);
    dest.range(351, 320) = reverse<32>(src.AskLevel[7].Price);
    dest.range(319, 256) = reverse<64>(src.AskLevel[7].Qty);
    dest.range(255, 224) = reverse<32>(src.AskLevel[8].Price);
    dest.range(223, 160) = reverse<64>(src.AskLevel[8].Qty);
    dest.range(159, 128) = reverse<32>(src.AskLevel[9].Price);
    dest.range(127, 64) = reverse<64>(src.AskLevel[9].Qty);
    dest.range(63, 0) = reverse<64>(src.TransactTime);
}
void sbe_intf::SBE_SSZ_fund_snap_t_unpack(SBE_SSZ_fund_snap_t_packed &src,
                          SBE_SSZ_fund_snap_t &dest)
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
    dest.IOPV = reverse<32>(src.range(31, 0));
}
void sbe_intf::SBE_SSZ_fund_snap_t_pack(SBE_SSZ_fund_snap_t &src,
                          SBE_SSZ_fund_snap_t_packed &dest)
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
    dest.range(31, 0) = reverse<32>(src.IOPV);
}
void sbe_intf::SBE_SSZ_bond_snap_t_unpack(SBE_SSZ_bond_snap_t_packed &src,
                          SBE_SSZ_bond_snap_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(2943, 2936);
    dest.Header.MsgType = src.range(2935, 2928);
    dest.Header.MsgLen = reverse<16>(src.range(2927, 2912));
    dest.Header.SecurityID[0] = src.range(2911, 2904);
    dest.Header.SecurityID[1] = src.range(2903, 2896);
    dest.Header.SecurityID[2] = src.range(2895, 2888);
    dest.Header.SecurityID[3] = src.range(2887, 2880);
    dest.Header.SecurityID[4] = src.range(2879, 2872);
    dest.Header.SecurityID[5] = src.range(2871, 2864);
    dest.Header.SecurityID[6] = src.range(2863, 2856);
    dest.Header.SecurityID[7] = src.range(2855, 2848);
    dest.Header.SecurityID[8] = src.range(2847, 2840);
    dest.Header.ChannelNo = reverse<16>(src.range(2839, 2824));
    dest.Header.ApplSeqNum = reverse<64>(src.range(2823, 2760));
    dest.Header.TradingPhase.Code0 = src.range(2759, 2756);
    dest.Header.TradingPhase.Code1 = src.range(2755, 2752);
    dest.NumTrades = reverse<64>(src.range(2751, 2688));
    dest.TotalVolumeTrade = reverse<64>(src.range(2687, 2624));
    dest.TotalValueTrade = reverse<64>(src.range(2623, 2560));
    dest.PrevClosePx = reverse<32>(src.range(2559, 2528));
    dest.LastPx = reverse<32>(src.range(2527, 2496));
    dest.OpenPx = reverse<32>(src.range(2495, 2464));
    dest.HighPx = reverse<32>(src.range(2463, 2432));
    dest.LowPx = reverse<32>(src.range(2431, 2400));
    dest.BidWeightPx = reverse<32>(src.range(2399, 2368));
    dest.BidWeightSize = reverse<64>(src.range(2367, 2304));
    dest.AskWeightPx = reverse<32>(src.range(2303, 2272));
    dest.AskWeightSize = reverse<64>(src.range(2271, 2208));
    dest.LastPxTradeType = reverse<32>(src.range(2207, 2176));
    dest.MatchTradeLastPx = reverse<32>(src.range(2175, 2144));
    dest.AuctionVolumeTrade = reverse<64>(src.range(2143, 2080));
    dest.AuctionValueTrade = reverse<64>(src.range(2079, 2016));
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
void sbe_intf::SBE_SSZ_bond_snap_t_pack(SBE_SSZ_bond_snap_t &src,
                          SBE_SSZ_bond_snap_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(2943, 2936) = src.Header.SecurityIDSource;
    dest.range(2935, 2928) = src.Header.MsgType;
    dest.range(2927, 2912) = reverse<16>(src.Header.MsgLen);
    dest.range(2911, 2904) = src.Header.SecurityID[0];
    dest.range(2903, 2896) = src.Header.SecurityID[1];
    dest.range(2895, 2888) = src.Header.SecurityID[2];
    dest.range(2887, 2880) = src.Header.SecurityID[3];
    dest.range(2879, 2872) = src.Header.SecurityID[4];
    dest.range(2871, 2864) = src.Header.SecurityID[5];
    dest.range(2863, 2856) = src.Header.SecurityID[6];
    dest.range(2855, 2848) = src.Header.SecurityID[7];
    dest.range(2847, 2840) = src.Header.SecurityID[8];
    dest.range(2839, 2824) = reverse<16>(src.Header.ChannelNo);
    dest.range(2823, 2760) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(2759, 2756) = src.Header.TradingPhase.Code0;
    dest.range(2755, 2752) = src.Header.TradingPhase.Code1;
    dest.range(2751, 2688) = reverse<64>(src.NumTrades);
    dest.range(2687, 2624) = reverse<64>(src.TotalVolumeTrade);
    dest.range(2623, 2560) = reverse<64>(src.TotalValueTrade);
    dest.range(2559, 2528) = reverse<32>(src.PrevClosePx);
    dest.range(2527, 2496) = reverse<32>(src.LastPx);
    dest.range(2495, 2464) = reverse<32>(src.OpenPx);
    dest.range(2463, 2432) = reverse<32>(src.HighPx);
    dest.range(2431, 2400) = reverse<32>(src.LowPx);
    dest.range(2399, 2368) = reverse<32>(src.BidWeightPx);
    dest.range(2367, 2304) = reverse<64>(src.BidWeightSize);
    dest.range(2303, 2272) = reverse<32>(src.AskWeightPx);
    dest.range(2271, 2208) = reverse<64>(src.AskWeightSize);
    dest.range(2207, 2176) = reverse<32>(src.LastPxTradeType);
    dest.range(2175, 2144) = reverse<32>(src.MatchTradeLastPx);
    dest.range(2143, 2080) = reverse<64>(src.AuctionVolumeTrade);
    dest.range(2079, 2016) = reverse<64>(src.AuctionValueTrade);
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
void sbe_intf::SBE_SSZ_bond_ord_t_unpack(SBE_SSZ_bond_ord_t_packed &src,
                          SBE_SSZ_bond_ord_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(383, 376);
    dest.Header.MsgType = src.range(375, 368);
    dest.Header.MsgLen = reverse<16>(src.range(367, 352));
    dest.Header.SecurityID[0] = src.range(351, 344);
    dest.Header.SecurityID[1] = src.range(343, 336);
    dest.Header.SecurityID[2] = src.range(335, 328);
    dest.Header.SecurityID[3] = src.range(327, 320);
    dest.Header.SecurityID[4] = src.range(319, 312);
    dest.Header.SecurityID[5] = src.range(311, 304);
    dest.Header.SecurityID[6] = src.range(303, 296);
    dest.Header.SecurityID[7] = src.range(295, 288);
    dest.Header.SecurityID[8] = src.range(287, 280);
    dest.Header.ChannelNo = reverse<16>(src.range(279, 264));
    dest.Header.ApplSeqNum = reverse<64>(src.range(263, 200));
    dest.Header.TradingPhase.Code0 = src.range(199, 196);
    dest.Header.TradingPhase.Code1 = src.range(195, 192);
    dest.Price = reverse<32>(src.range(191, 160));
    dest.OrderQty = reverse<64>(src.range(159, 96));
    dest.Side = src.range(95, 88);
    dest.OrdType = src.range(87, 80);
    dest.TransactTime = reverse<64>(src.range(79, 16));
    dest.Resv[0] = src.range(15, 8);
    dest.Resv[1] = src.range(7, 0);
}
void sbe_intf::SBE_SSZ_bond_ord_t_pack(SBE_SSZ_bond_ord_t &src,
                          SBE_SSZ_bond_ord_t_packed &dest)
{
#pragma HLS INLINE

    dest.range(383, 376) = src.Header.SecurityIDSource;
    dest.range(375, 368) = src.Header.MsgType;
    dest.range(367, 352) = reverse<16>(src.Header.MsgLen);
    dest.range(351, 344) = src.Header.SecurityID[0];
    dest.range(343, 336) = src.Header.SecurityID[1];
    dest.range(335, 328) = src.Header.SecurityID[2];
    dest.range(327, 320) = src.Header.SecurityID[3];
    dest.range(319, 312) = src.Header.SecurityID[4];
    dest.range(311, 304) = src.Header.SecurityID[5];
    dest.range(303, 296) = src.Header.SecurityID[6];
    dest.range(295, 288) = src.Header.SecurityID[7];
    dest.range(287, 280) = src.Header.SecurityID[8];
    dest.range(279, 264) = reverse<16>(src.Header.ChannelNo);
    dest.range(263, 200) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(199, 196) = src.Header.TradingPhase.Code0;
    dest.range(195, 192) = src.Header.TradingPhase.Code1;
    dest.range(191, 160) = reverse<32>(src.Price);
    dest.range(159, 96) = reverse<64>(src.OrderQty);
    dest.range(95, 88) = src.Side;
    dest.range(87, 80) = src.OrdType;
    dest.range(79, 16) = reverse<64>(src.TransactTime);
    dest.range(15, 8) = src.Resv[0];
    dest.range(7, 0) = src.Resv[1];
}
void sbe_intf::SBE_SSZ_bond_exe_t_unpack(SBE_SSZ_bond_exe_t_packed &src,
                          SBE_SSZ_bond_exe_t &dest)
{
#pragma HLS INLINE

    dest.Header.SecurityIDSource = src.range(511, 504);
    dest.Header.MsgType = src.range(503, 496);
    dest.Header.MsgLen = reverse<16>(src.range(495, 480));
    dest.Header.SecurityID[0] = src.range(479, 472);
    dest.Header.SecurityID[1] = src.range(471, 464);
    dest.Header.SecurityID[2] = src.range(463, 456);
    dest.Header.SecurityID[3] = src.range(455, 448);
    dest.Header.SecurityID[4] = src.range(447, 440);
    dest.Header.SecurityID[5] = src.range(439, 432);
    dest.Header.SecurityID[6] = src.range(431, 424);
    dest.Header.SecurityID[7] = src.range(423, 416);
    dest.Header.SecurityID[8] = src.range(415, 408);
    dest.Header.ChannelNo = reverse<16>(src.range(407, 392));
    dest.Header.ApplSeqNum = reverse<64>(src.range(391, 328));
    dest.Header.TradingPhase.Code0 = src.range(327, 324);
    dest.Header.TradingPhase.Code1 = src.range(323, 320);
    dest.BidApplSeqNum = reverse<64>(src.range(319, 256));
    dest.OfferApplSeqNum = reverse<64>(src.range(255, 192));
    dest.LastPx = reverse<32>(src.range(191, 160));
    dest.LastQty = reverse<64>(src.range(159, 96));
    dest.ExecType = src.range(95, 88);
    dest.TransactTime = reverse<64>(src.range(87, 24));
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
    dest.range(495, 480) = reverse<16>(src.Header.MsgLen);
    dest.range(479, 472) = src.Header.SecurityID[0];
    dest.range(471, 464) = src.Header.SecurityID[1];
    dest.range(463, 456) = src.Header.SecurityID[2];
    dest.range(455, 448) = src.Header.SecurityID[3];
    dest.range(447, 440) = src.Header.SecurityID[4];
    dest.range(439, 432) = src.Header.SecurityID[5];
    dest.range(431, 424) = src.Header.SecurityID[6];
    dest.range(423, 416) = src.Header.SecurityID[7];
    dest.range(415, 408) = src.Header.SecurityID[8];
    dest.range(407, 392) = reverse<16>(src.Header.ChannelNo);
    dest.range(391, 328) = reverse<64>(src.Header.ApplSeqNum);
    dest.range(327, 324) = src.Header.TradingPhase.Code0;
    dest.range(323, 320) = src.Header.TradingPhase.Code1;
    dest.range(319, 256) = reverse<64>(src.BidApplSeqNum);
    dest.range(255, 192) = reverse<64>(src.OfferApplSeqNum);
    dest.range(191, 160) = reverse<32>(src.LastPx);
    dest.range(159, 96) = reverse<64>(src.LastQty);
    dest.range(95, 88) = src.ExecType;
    dest.range(87, 24) = reverse<64>(src.TransactTime);
    dest.range(23, 16) = src.Resv[0];
    dest.range(15, 8) = src.Resv[1];
    dest.range(7, 0) = src.Resv[2];
}