#ifndef __SBE_INTF_HPP__
#define __SBE_INTF_HPP__

#include "sbe_ssz_origin.hpp"
typedef ap_uint<96> price_level_t_packed;
typedef ap_uint<808> QtyQueue_level_t_packed;
typedef ap_uint<8> SSZ_TradingPhaseCodePack_t_packed;
typedef ap_uint<192> SBE_SSZ_header_t_packed;
typedef ap_uint<2816> SBE_SSZ_instrument_snap_t_packed;
typedef ap_uint<768> SBE_SSZ_index_snap_t_packed;
typedef ap_uint<384> SBE_SSZ_ord_t_packed;
typedef ap_uint<512> SBE_SSZ_exe_t_packed;
typedef ap_uint<2880> SBE_SSZ_option_snap_t_packed;
typedef ap_uint<2816> SBE_SSZ_fund_snap_t_packed;
typedef ap_uint<2944> SBE_SSZ_bond_snap_t_packed;
typedef ap_uint<384> SBE_SSZ_bond_ord_t_packed;
typedef ap_uint<512> SBE_SSZ_bond_exe_t_packed;

class sbe_intf
{
public:

    static void price_level_t_unpack(price_level_t_packed &src,
                          price_level_t &dest);

    static void price_level_t_pack(price_level_t &src,
                          price_level_t_packed &dest);

    static void QtyQueue_level_t_unpack(QtyQueue_level_t_packed &src,
                          QtyQueue_level_t &dest);

    static void QtyQueue_level_t_pack(QtyQueue_level_t &src,
                          QtyQueue_level_t_packed &dest);

    static void SSZ_TradingPhaseCodePack_t_unpack(SSZ_TradingPhaseCodePack_t_packed &src,
                          SSZ_TradingPhaseCodePack_t &dest);

    static void SSZ_TradingPhaseCodePack_t_pack(SSZ_TradingPhaseCodePack_t &src,
                          SSZ_TradingPhaseCodePack_t_packed &dest);

    static void SBE_SSZ_header_t_unpack(SBE_SSZ_header_t_packed &src,
                          SBE_SSZ_header_t &dest);

    static void SBE_SSZ_header_t_pack(SBE_SSZ_header_t &src,
                          SBE_SSZ_header_t_packed &dest);

    static void SBE_SSZ_instrument_snap_t_unpack(SBE_SSZ_instrument_snap_t_packed &src,
                          SBE_SSZ_instrument_snap_t &dest);

    static void SBE_SSZ_instrument_snap_t_pack(SBE_SSZ_instrument_snap_t &src,
                          SBE_SSZ_instrument_snap_t_packed &dest);

    static void SBE_SSZ_index_snap_t_unpack(SBE_SSZ_index_snap_t_packed &src,
                          SBE_SSZ_index_snap_t &dest);

    static void SBE_SSZ_index_snap_t_pack(SBE_SSZ_index_snap_t &src,
                          SBE_SSZ_index_snap_t_packed &dest);

    static void SBE_SSZ_ord_t_unpack(SBE_SSZ_ord_t_packed &src,
                          SBE_SSZ_ord_t &dest);

    static void SBE_SSZ_ord_t_pack(SBE_SSZ_ord_t &src,
                          SBE_SSZ_ord_t_packed &dest);

    static void SBE_SSZ_exe_t_unpack(SBE_SSZ_exe_t_packed &src,
                          SBE_SSZ_exe_t &dest);

    static void SBE_SSZ_exe_t_pack(SBE_SSZ_exe_t &src,
                          SBE_SSZ_exe_t_packed &dest);

    static void SBE_SSZ_option_snap_t_unpack(SBE_SSZ_option_snap_t_packed &src,
                          SBE_SSZ_option_snap_t &dest);

    static void SBE_SSZ_option_snap_t_pack(SBE_SSZ_option_snap_t &src,
                          SBE_SSZ_option_snap_t_packed &dest);

    static void SBE_SSZ_fund_snap_t_unpack(SBE_SSZ_fund_snap_t_packed &src,
                          SBE_SSZ_fund_snap_t &dest);

    static void SBE_SSZ_fund_snap_t_pack(SBE_SSZ_fund_snap_t &src,
                          SBE_SSZ_fund_snap_t_packed &dest);

    static void SBE_SSZ_bond_snap_t_unpack(SBE_SSZ_bond_snap_t_packed &src,
                          SBE_SSZ_bond_snap_t &dest);

    static void SBE_SSZ_bond_snap_t_pack(SBE_SSZ_bond_snap_t &src,
                          SBE_SSZ_bond_snap_t_packed &dest);

    static void SBE_SSZ_bond_ord_t_unpack(SBE_SSZ_bond_ord_t_packed &src,
                          SBE_SSZ_bond_ord_t &dest);

    static void SBE_SSZ_bond_ord_t_pack(SBE_SSZ_bond_ord_t &src,
                          SBE_SSZ_bond_ord_t_packed &dest);

    static void SBE_SSZ_bond_exe_t_unpack(SBE_SSZ_bond_exe_t_packed &src,
                          SBE_SSZ_bond_exe_t &dest);

    static void SBE_SSZ_bond_exe_t_pack(SBE_SSZ_bond_exe_t &src,
                          SBE_SSZ_bond_exe_t_packed &dest);
}; // class sbe_intf

#endif // __SBE_INTF_HPP__"