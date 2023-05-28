
#ifndef __SBE_SSZ_ORIGIN_H__
#define __SBE_SSZ_ORIGIN_H__
/*
#ifdef __cplusplus
extern "C"
{
#endif
*/

#include "ap_axi_sdata.h"
#include "sbe_stock_origin.hpp"

/*
#ifdef WIN32
#define PACKED
#pragma pack(push,1)
#else
#define PACKED __attribute__ ((__packed__))
#endif
*/

#define __SecurityIDSource_SSZ_                 (102)   //深交所

#ifndef __MsgType_HEARTBEAT__
#define __MsgType_HEARTBEAT__                   (1)     //心跳消息
#endif

#define __MsgType_SSZ_INSTRUMENT_SNAP__         (111)   //个股快照、可转债快照
#define __MsgType_SSZ_INDEX_SNAP__              (11)    //指数快照
#define __MsgType_SSZ_ORDER__                   (192)   //个股逐笔委托、可转债逐笔委托
#define __MsgType_SSZ_EXECUTION__               (191)   //个股逐笔成交、可转债逐笔成交
#define __MsgType_SSZ_OPTION_SNAP__             (13)    //期权快照
#define __MsgType_SSZ_FUND_SNAP__               (12)    //基金快照

#define __MsgType_SSZ_BOND_SNAP__               (211)   //债券现券快照、逆回购快照
#define __MsgType_SSZ_BOND_ORDER__              (92)    //债券现券逐笔委托、逆回购逐笔委托
#define __MsgType_SSZ_BOND_EXECUTION__          (91)    //债券现券逐笔成交、逆回购逐笔成交


typedef struct SSZ_TradingPhaseCodePack_t 
{
    // ap_uint<8>             Value;
    // struct unpack{
        ap_uint<4>         Code0;// : 4;  //映射自交易阶段代码第0位
        ap_uint<4>         Code1;// : 4;  //映射自交易阶段代码第1位
    // } unpack;
}SSZ_TradingPhaseCodePack_t;

//Stock ShenZhen Unified header
typedef
struct SBE_SSZ_header_t
{
    ap_uint<8>     SecurityIDSource;                      //交易所代码:102=深交所;101=上交所.
    ap_uint<8>     MsgType;                               //消息类型:111=快照行情;191=逐笔成交;192=逐笔委托.
    ap_uint<16>    MsgLen;                                //消息总字节数，含消息头.
    ap_int<8>        SecurityID[9];                         //证券代码，6或8字符后加'\0'
    ap_uint<16>    ChannelNo;                             //通道号
    ap_uint<64>    ApplSeqNum;                            //消息序列号，仅对逐笔成交和逐笔委托有效; 快照数据中bit[63]='1'表示L1(仅5档有效)
    struct SSZ_TradingPhaseCodePack_t     TradingPhase;       //交易阶段代码映射，仅对行情快照有效（深交所和上交所具体映射方式不同）.
}SBE_SSZ_header_t;


//map from MsgType=300111
typedef
struct SBE_SSZ_instrument_snap_t
{
    struct SBE_SSZ_header_t  Header;    //msgType=111

    ap_int<64>         NumTrades;          //成交笔数
    ap_int<64>         TotalVolumeTrade;   //成交总量, Qty,N15(2)
    ap_int<64>         TotalValueTrade;    //成交总金额, Amt,N18(4)
    ap_int<32>         PrevClosePx;        //昨收价, Price,N13(4)

    ap_int<32>         LastPx;             //最近价, MDEntryPx,N18(6)
    ap_int<32>         OpenPx;             //开盘价, MDEntryPx,N18(6)
    ap_int<32>         HighPx;             //最高价, MDEntryPx,N18(6)
    ap_int<32>         LowPx;              //最低价, MDEntryPx,N18(6)

    ap_int<32>         BidWeightPx;        //买方委托数量加权平均价, MDEntryPx,N18(6)
    ap_int<64>         BidWeightSize;      //买方委托总数量, Qty,N15(2)
    ap_int<32>         AskWeightPx;        //卖方委托数量加权平均价, MDEntryPx,N18(6)，超出32位可表示精度时=0x7fffffff
    ap_int<64>         AskWeightSize;      //卖方委托总数量, Qty,N15(2)
    ap_int<32>         UpLimitPx;          //涨停价, MDEntryPx,N18(6) 无涨停价格限制 = 0x7fffffff (转自999999999.999900)
    ap_int<32>         DnLimitPx;          //跌停价, MDEntryPx,N18(6) 无跌停价格限制 = 0x2710 (转自0.010000) 或 0x80000000 (转自-999999999.999900)
    struct price_level_t   BidLevel[10];//十档买盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    struct price_level_t   AskLevel[10];//十档卖盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    ap_uint<64>         TransactTime;      //YYYYMMDDHHMMSSsss(毫秒)
    ap_uint<8>          Resv[4];
}SBE_SSZ_instrument_snap_t;

//map from MsgType=309011
typedef
struct SBE_SSZ_index_snap_t
{
    struct SBE_SSZ_header_t  Header;    //msgType=11

    ap_int<64>         NumTrades;
    ap_int<64>         TotalVolumeTrade;   //成交总量, Qty,N15(2)
    ap_int<64>         TotalValueTrade;    //成交总金额, Amt,N18(4)
    ap_int<64>         PrevClosePx;        //昨收价, Price,N13(4)
    ap_int<64>         LastPx;             //最近价, MDEntryPx,N18(6)
    ap_int<64>         OpenPx;             //开盘价, MDEntryPx,N18(6)
    ap_int<64>         HighPx;             //最高价, MDEntryPx,N18(6)
    ap_int<64>         LowPx;              //最低价, MDEntryPx,N18(6)
    ap_uint<64>        TransactTime;
}SBE_SSZ_index_snap_t;

//map from MsgType=300192
typedef
struct SBE_SSZ_ord_t
{
    struct SBE_SSZ_header_t  Header;    //msgType=192

    ap_int<32>         Price;          //委托价格, Price,N13(4)
    ap_int<64>         OrderQty;       //委托数量, Qty,N15(2)
    ap_int<8>          Side;           //买卖方向: '1'=买, '2'=卖, 'G'=借入, 'F'=出借
    ap_int<8>          OrdType;        //订单类别: '1'=市价, '2'=限价, 'U'=本方最优
    ap_uint<64>        TransactTime;   //YYYYMMDDHHMMSSsss(毫秒)
    ap_uint<8>         Resv[2];
}SBE_SSZ_ord_t;

//map from MsgType=300191
typedef
struct SBE_SSZ_exe_t
{
    struct SBE_SSZ_header_t  Header;    //msgType=191

    ap_int<64>         BidApplSeqNum;  //买方委托索引 *
    ap_int<64>         OfferApplSeqNum;//卖方委托索引 *
    ap_int<32>         LastPx;         //成交价格, Price,N13(4)
    ap_int<64>         LastQty;        //成交数量, Qty,N15(2)
    ap_int<8>          ExecType;       //成交类别: '4'=撤销, 'F'=成交
    ap_uint<64>        TransactTime;   //YYYYMMDDHHMMSSsss(毫秒)
    ap_uint<8>         Resv[3];
}SBE_SSZ_exe_t;


//map from MsgType=300111, channel in [1050, 1059]
typedef
struct SBE_SSZ_option_snap_t
{
    struct SBE_SSZ_header_t  Header;    //msgType=13

    ap_int<64>         NumTrades;          //成交笔数
    ap_int<64>         TotalVolumeTrade;   //成交总量, Qty,N15(2)
    ap_int<64>         TotalValueTrade;    //成交总金额, Amt,N18(4)
    ap_int<32>         PrevClosePx;        //昨收价, Price,N13(4)

    ap_int<32>         LastPx;             //最近价, MDEntryPx,N18(6)
    ap_int<32>         OpenPx;             //开盘价, MDEntryPx,N18(6)
    ap_int<32>         HighPx;             //最高价, MDEntryPx,N18(6)
    ap_int<32>         LowPx;              //最低价, MDEntryPx,N18(6)

    ap_int<32>         BidWeightPx;        //买方委托数量加权平均价, MDEntryPx,N18(6)
    ap_int<64>         BidWeightSize;      //买方委托总数量, Qty,N15(2)
    ap_int<32>         AskWeightPx;        //卖方委托数量加权平均价, MDEntryPx,N18(6)，超出32位可表示精度时=0x7fffffff
    ap_int<64>         AskWeightSize;      //卖方委托总数量, Qty,N15(2)
    ap_int<32>         UpLimitPx;          //涨停价, MDEntryPx,N18(6) 无涨停价格限制 = 0x7fffffff (转自999999999.999900)
    ap_int<32>         DnLimitPx;          //跌停价, MDEntryPx,N18(6) 无跌停价格限制 = 0x2710 (转自0.010000) 或 0x80000000 (转自-999999999.999900)
    ap_int<64>         ContractPos;        //合约持仓量, Qty,N15(2)
    ap_int<32>         RefPx;              //参考价, MDEntryPx,N18(6)
    struct price_level_t   BidLevel[10];//十档买盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    struct price_level_t   AskLevel[10];//十档卖盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    ap_uint<64>         TransactTime;      //YYYYMMDDHHMMSSsss(毫秒)
}SBE_SSZ_option_snap_t;

//map from MsgType=300111, channel in [1020, 1029]
typedef
struct SBE_SSZ_fund_snap_t
{
    struct SBE_SSZ_header_t  Header;    //msgType=12

    ap_int<64>         NumTrades;          //成交笔数
    ap_int<64>         TotalVolumeTrade;   //成交总量, Qty,N15(2)
    ap_int<64>         TotalValueTrade;    //成交总金额, Amt,N18(4)
    ap_int<32>         PrevClosePx;        //昨收价, Price,N13(4)

    ap_int<32>         LastPx;             //最近价, MDEntryPx,N18(6)
    ap_int<32>         OpenPx;             //开盘价, MDEntryPx,N18(6)
    ap_int<32>         HighPx;             //最高价, MDEntryPx,N18(6)
    ap_int<32>         LowPx;              //最低价, MDEntryPx,N18(6)

    ap_int<32>         BidWeightPx;        //买方委托数量加权平均价, MDEntryPx,N18(6)
    ap_int<64>         BidWeightSize;      //买方委托总数量, Qty,N15(2)
    ap_int<32>         AskWeightPx;        //卖方委托数量加权平均价, MDEntryPx,N18(6)，超出32位可表示精度时=0x7fffffff
    ap_int<64>         AskWeightSize;      //卖方委托总数量, Qty,N15(2)
    ap_int<32>         UpLimitPx;          //涨停价, MDEntryPx,N18(6) 无涨停价格限制 = 0x7fffffff (转自999999999.999900)
    ap_int<32>         DnLimitPx;          //跌停价, MDEntryPx,N18(6) 无跌停价格限制 = 0x2710 (转自0.010000) 或 0x80000000 (转自-999999999.999900)
    struct price_level_t   BidLevel[10];//十档买盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    struct price_level_t   AskLevel[10];//十档卖盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    ap_uint<64>        TransactTime;       //YYYYMMDDHHMMSSsss(毫秒)
    ap_int<32>         IOPV;               //基金实时参考净值, MDEntryPx,N18(6)
}SBE_SSZ_fund_snap_t;


//map from MsgType=300211
typedef
struct SBE_SSZ_bond_snap_t
{
    struct SBE_SSZ_header_t  Header;        //msgType=211

    ap_int<64>         NumTrades;              //成交笔数
    ap_int<64>         TotalVolumeTrade;       //成交总量, Qty,N15(2)
    ap_int<64>         TotalValueTrade;        //成交总金额, Amt,N18(4)
    ap_int<32>         PrevClosePx;            //昨收价, Price,N13(4)

    ap_int<32>         LastPx;                 //最近价, MDEntryPx,N18(6)
    ap_int<32>         OpenPx;                 //开盘价, MDEntryPx,N18(6)
    ap_int<32>         HighPx;                 //最高价, MDEntryPx,N18(6)
    ap_int<32>         LowPx;                  //最低价, MDEntryPx,N18(6)

    ap_int<32>         BidWeightPx;            //买方委托数量加权平均价, MDEntryPx,N18(6)
    ap_int<64>         BidWeightSize;          //买方委托总数量, Qty,N15(2)
    ap_int<32>         AskWeightPx;            //卖方委托数量加权平均价, MDEntryPx,N18(6)，超出32位可表示精度时=0x7fffffff
    ap_int<64>         AskWeightSize;          //卖方委托总数量, Qty,N15(2)
    ap_int<32>         LastPxTradeType;        //产生该最近价的成交方式, Qty,N15(2)，[0.01=匹配成交;0.02=协商成交;0.03=点击成交;0.04=询价成交;0.05=竞买成交]
    ap_int<32>         MatchTradeLastPx;       //匹配成交最近价, MDEntryPx,N18(6)
    ap_int<64>         AuctionVolumeTrade;     //匹配成交成交量, Qty,N15(2)
    ap_int<64>         AuctionValueTrade;      //匹配成交成交金额, Amt,N18(4)
    struct price_level_t   BidLevel[10];    //十档买盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    struct price_level_t   AskLevel[10];    //十档卖盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    ap_uint<64>        TransactTime;           //YYYYMMDDHHMMSSsss(毫秒)
    ap_uint<8>         Resv[4];
}SBE_SSZ_bond_snap_t;

//map from MsgType=300292
typedef
struct SBE_SSZ_bond_ord_t
{
    struct SBE_SSZ_header_t  Header;        //msgType=92

    ap_int<32>         Price;          //委托价格, Price,N13(4)
    ap_int<64>         OrderQty;       //委托数量, Qty,N15(2)
    ap_int<8>          Side;           //买卖方向: '1'=买, '2'=卖, 'G'=借入, 'F'=出借
    ap_int<8>          OrdType;        //订单类别: '1'=市价, '2'=限价, 'U'=本方最优
    ap_uint<64>        TransactTime;   //YYYYMMDDHHMMSSsss(毫秒)
    ap_uint<8>         Resv[2];
}SBE_SSZ_bond_ord_t;

//map from MsgType=300291
typedef
struct SBE_SSZ_bond_exe_t
{
    struct SBE_SSZ_header_t  Header;        //msgType=91

    ap_int<64>         BidApplSeqNum;      //买方委托索引 *
    ap_int<64>         OfferApplSeqNum;    //卖方委托索引 *
    ap_int<32>         LastPx;             //成交价格, Price,N13(4)
    ap_int<64>         LastQty;            //成交数量, Qty,N15(2)
    ap_int<8>          ExecType;           //成交类别: '4'=撤销, 'F'=成交
    ap_uint<64>        TransactTime;       //YYYYMMDDHHMMSSsss(毫秒)
    ap_uint<8>         Resv[3];
}SBE_SSZ_bond_exe_t;













/*
#ifdef WIN32
#pragma pack(pop)
#undef PACKED
#else
#undef PACKED
#endif
*/


/*
#ifdef __cplusplus
}
#endif
*/
#endif /*__SBE_SSZ_ORIGIN_H__*/
