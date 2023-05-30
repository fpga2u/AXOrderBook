/*
 * SBE 消息格式字段解析工具
 * xxx_packed 类型为 xxx结构体完全展开后的辅助类型，便于在AXI_STREAM中发送。
 * xxx_pack()和xxx_unpack()用于在展开类型和原始类型中切换， TODO:理论上应该没有FF。
 */

#ifndef __SBE_INTF_HPP__
#define __SBE_INTF_HPP__

#include "xv_define.h"
#include "sbe_ssz_origin.hpp"


#define BITSIZE_price_level_t_packed 96
typedef ap_uint<BITSIZE_price_level_t_packed> price_level_t_packed;

#define BITSIZE_QtyQueue_level_t_packed 808
typedef ap_uint<BITSIZE_QtyQueue_level_t_packed> QtyQueue_level_t_packed;

#define BITSIZE_SSZ_TradingPhaseCodePack_t_packed 8
typedef ap_uint<BITSIZE_SSZ_TradingPhaseCodePack_t_packed> SSZ_TradingPhaseCodePack_t_packed;

#define BITSIZE_SBE_SSZ_header_t_packed 192
typedef ap_uint<BITSIZE_SBE_SSZ_header_t_packed> SBE_SSZ_header_t_packed;

#define BITSIZE_SBE_SSZ_instrument_snap_t_packed 2816
typedef ap_uint<BITSIZE_SBE_SSZ_instrument_snap_t_packed> SBE_SSZ_instrument_snap_t_packed;

#define BITSIZE_SBE_SSZ_index_snap_t_packed 768
typedef ap_uint<BITSIZE_SBE_SSZ_index_snap_t_packed> SBE_SSZ_index_snap_t_packed;

#define BITSIZE_SBE_SSZ_ord_t_packed 384
typedef ap_uint<BITSIZE_SBE_SSZ_ord_t_packed> SBE_SSZ_ord_t_packed;

#define BITSIZE_SBE_SSZ_exe_t_packed 512
typedef ap_uint<BITSIZE_SBE_SSZ_exe_t_packed> SBE_SSZ_exe_t_packed;

#define BITSIZE_SBE_SSZ_option_snap_t_packed 2880
typedef ap_uint<BITSIZE_SBE_SSZ_option_snap_t_packed> SBE_SSZ_option_snap_t_packed;

#define BITSIZE_SBE_SSZ_fund_snap_t_packed 2816
typedef ap_uint<BITSIZE_SBE_SSZ_fund_snap_t_packed> SBE_SSZ_fund_snap_t_packed;

#define BITSIZE_SBE_SSZ_bond_snap_t_packed 2944
typedef ap_uint<BITSIZE_SBE_SSZ_bond_snap_t_packed> SBE_SSZ_bond_snap_t_packed;

#define BITSIZE_SBE_SSZ_bond_ord_t_packed 384
typedef ap_uint<BITSIZE_SBE_SSZ_bond_ord_t_packed> SBE_SSZ_bond_ord_t_packed;

#define BITSIZE_SBE_SSZ_bond_exe_t_packed 512
typedef ap_uint<BITSIZE_SBE_SSZ_bond_exe_t_packed> SBE_SSZ_bond_exe_t_packed;


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

bool operator==(const price_level_t& A, const price_level_t& B);
bool operator==(const QtyQueue_level_t& A, const QtyQueue_level_t& B);
bool operator==(const SSZ_TradingPhaseCodePack_t& A, const SSZ_TradingPhaseCodePack_t& B);
bool operator==(const SBE_SSZ_header_t& A, const SBE_SSZ_header_t& B);
bool operator==(const SBE_SSZ_instrument_snap_t& A, const SBE_SSZ_instrument_snap_t& B);
bool operator==(const SBE_SSZ_index_snap_t& A, const SBE_SSZ_index_snap_t& B);
bool operator==(const SBE_SSZ_ord_t& A, const SBE_SSZ_ord_t& B);
bool operator==(const SBE_SSZ_exe_t& A, const SBE_SSZ_exe_t& B);
bool operator==(const SBE_SSZ_option_snap_t& A, const SBE_SSZ_option_snap_t& B);
bool operator==(const SBE_SSZ_fund_snap_t& A, const SBE_SSZ_fund_snap_t& B);
bool operator==(const SBE_SSZ_bond_snap_t& A, const SBE_SSZ_bond_snap_t& B);
bool operator==(const SBE_SSZ_bond_ord_t& A, const SBE_SSZ_bond_ord_t& B);
bool operator==(const SBE_SSZ_bond_exe_t& A, const SBE_SSZ_bond_exe_t& B);


#endif // __SBE_INTF_HPP__

