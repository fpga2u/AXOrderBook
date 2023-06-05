# L2行情消息细节

A股的L2实时行情消息在订单簿重建时所用到的有三种：行情快照、逐笔委托、逐笔成交。虽然上交所和深交所的L2行情接口协议不同，但主要字段基本一致。

为便于开发，我们将交易所原始行情数据进行了压缩转换，使易于在python或FPGA HLS内使用。

测试历史数据用txt格式保存，便于阅读。

---

## L2快照（snap）

L2快照消息包含了当前订单簿的最优10档价格，因此通常被称为10档行情。交易所发布的快照消息通常为3秒一次。

快照的常用字段包括：

字段|说明
--|--
SecurityID|证券代码
NumTrades|成交笔数
TotalVolumeTrade|成交总量
TotalValueTrade|成交总金额
LastPx|最近价
OpenPx|开盘价
HighPx|最高价
LowPx|最低价
BidWeightPx|买方加权平均价
BidWeightSize|买方订单总量
AskWeightPx|卖方加权平均价
AskWeightSize|卖方订单总量
bid[10]|买方10档（包括各档价格和总量，及前50笔排队订单）
ask[10]|卖方10档（包括各档价格和总量，及前50笔排队订单）
TradingPhaseCode|交易阶段代码
TransactTime|生成时间

---

## L2逐笔委托（order）

交易所在收到客户下的合法交易订单后，就会发出一条逐笔委托消息。

逐笔委托的常用字段包括：

字段|说明
--|--
SecurityID|证券代码
ChannelNo|通道号，一个通道内有数千个股，某日某只个股始的通道号是固定的，不同日是不固定的
ApplSeqNum|委托序列号，同一通道内的序号```从1开始```按顺序递增，同一个通道的逐笔成交和逐笔委托的序号是连着的
Price|委托价格（非限价委托时无意义，可能为0、n个9或负数）
OrderQty|委托数量
Side|委托方向（卖/卖/借入/借出）
OrdType|委托类型（深圳：市价/限价/本方最优；上海：新增/删除）
TransactTime|生成时间

---

## L2逐笔成交（execution）

交易所在撮合两笔订单成交后，就会发出一条逐笔成交消息；交易所在收到客户的撤单请求并撤单成功后，也会发出一条逐笔成交消息。

逐笔成交的常用字段包括：
字段|说明
--|--
SecurityID|证券代码
ChannelNo|通道号，一个通道内有数千个股，某日某只个股始的通道号是固定的，不同日是不固定的
ApplSeqNum|成交序列号，同一通道内的序号```从1开始```按顺序递增，同一个通道的逐笔成交和逐笔委托的序号是连着的
BidApplSeqNum|买方序列号，与逐笔委托的序列号相同（撤单时只有买方或卖方有意义，另一方为0表示不存在）
OfferApplSeqNum|卖方序列号，与逐笔委托的序列号相同
LastPx|成交价格（深圳：撤单时无意义）
LastQty|成交数量
ExecType|执行类型（深圳：已成交/已撤销；上海：主买/主卖）

---

## 消息统计

我们统计了2022年某几天的A股L2消息数量。

> ### 深交所

统计了2290只个股，在个股层面做若干日平均。

消息类型|总数
--|--
逐笔委托|6.6千万条
逐笔成交(已成交)|4.3千万条
逐笔成交(已撤销)|1.7千万条

22-10-28 深圳个股+基金+可转债 逐笔委托+成交 一共1.8亿余条。

> 分布

个股|均值|最小值|25%|50%|75%|最大值
--|--|--|--|--|--|--
价格|17.88|0.69|5.56|10.18|20.26|503.00|
个股委托(限价)|28,888|320|11,994|21,058|36,864|366,621|
个股委托(市价)|91|0|7|19|62|2,773|
个股委托(本方最优)|1|0|0|0|1|66|
逐笔成交(已成交)|19,012|32|7,008|13,336|24,782|206,632|
逐笔成交(已撤销)|7,560|62|3,641|5,779|9,325|127,259|

* 委托呈头部集中状态，2290只个股中：
  * 前500只个股的委托数占到了市场总委托数的50%
  * 前60只个股的委托数占到了总委托数的12%。
* 深交所委托单最多的个股是九安医疗36.8万笔
* 深交所宁德时代的委托单是19.1万笔

---

## 简单二进制编码（AX-SBE）

L2行情数据量很大，而且我们在python和FPGA HLS中都需要读入数据，为便于开发，我们将所需的三种消息重新进行编码：将消息映射成C语言结构体，并按x86小端模式存储字段值。这种编码模式我们称为简单二进制编码（AX-simple-binary-encoding）。

以下以C代码说明AX-SBE的结构和字段意义。

注释中的Nx(y)表示相应的类型实际为浮点数类型，其中 x 表示整数与小数总计位数，不包括小数点， y 表示小数位数，比如对于 Price,N13(4) 类型， Int64 值 186400 表示的价格为 18.6400。

> sbe-header

所有sbe消息都按消息头+消息体的格式定义，其中消息头是统一的结构体：

```c
struct SBE_header_t //24B
{
    uint8_t     SecurityIDSource;   //交易所代码:102=深交所;101=上交所.
    uint8_t     MsgType;            //消息类型:111=快照行情;191=逐笔成交;192=逐笔委托.
    uint16_t    MsgLen;             //消息总字节数，含消息头.
    char        SecurityID[9];      //证券代码，6或8字符后加'\0'
    uint16_t    ChannelNo;          //通道号
    uint64_t    ApplSeqNum;         //消息序列号，仅对逐笔成交和逐笔委托有效.
    uint8_t     TradingPhase;       //交易阶段代码映射，仅对行情快照有效（深交所和上交所具体映射方式不同）.
};
```

> sbe-price-level

用于表示价格档位

```c
struct price_level_t //12B
{
    int32_t    Price;  //价格（深交所和上交所精度不同，股票和债券精度也不同）
    int64_t    Qty;    //数量（深交所和上交所精度不同，股票和债券精度也不同）
};
```

> sbe-level-orders

用于表示各档的订单队列

```c
struct QtyQueue_level_t
{
    uint8_t  NoOrders;      //有效订单数目
    uint16_t QtyQueue[50];  //前50笔排队订单的各自数量，按顺序，[0]为首笔
};
```

---

### 深交所sbe消息格式

> #### 深交所消息头

为便于解析深交所的交易阶段代码，单独定义一个深交所消息头，其只是将公共消息头的```TradingPhase```重新组织：

```c
typedef union SSZ_TradingPhaseCodePack_t 
{
    uint8_t             Value;
    struct unpack{
        uint8_t         Code0 : 4;  //映射自交易阶段代码第0位
        uint8_t         Code1 : 4;  //映射自交易阶段代码第1位
    } unpack;
}SSZ_TradingPhaseCodePack_t;

struct SBE_SSZ_header_t
{
    uint8_t     SecurityIDSource;
    uint8_t     MsgType;
    uint16_t    MsgLen;
    char        SecurityID[9];
    uint16_t    ChannelNo;
    uint64_t    ApplSeqNum;
    SSZ_TradingPhaseCodePack_t     TradingPhase;
};
```

> #### 深交所快照行情

对每个价格档位，仅保留其价格和成交量，未保留其50笔排队订单，这样减小数据量并且不影响我们用来校验重建的订单簿。

```c
//对应深交所协议频道代码为股票的消息类型300111
struct SBE_SSZ_instrument_snap_t //352B
{
    struct SBE_SSZ_header_t  Header;    //msgType=111

    int64_t         NumTrades;          //成交笔数
    int64_t         TotalVolumeTrade;   //成交总量, Qty,N15(2)
    int64_t         TotalValueTrade;    //成交总金额, Amt,N18(4)
    int32_t         PrevClosePx;        //昨收价, Price,N13(4)

    int32_t         LastPx;             //最近价, MDEntryPx,N18(6)
    int32_t         OpenPx;             //开盘价, MDEntryPx,N18(6)
    int32_t         HighPx;             //最高价, MDEntryPx,N18(6)
    int32_t         LowPx;              //最低价, MDEntryPx,N18(6)

    int32_t         BidWeightPx;        //买方委托数量加权平均价, MDEntryPx,N18(6)
    int64_t         BidWeightSize;      //买方委托总数量, Qty,N15(2)
    int32_t         AskWeightPx;        //卖方委托数量加权平均价, MDEntryPx,N18(6)
    int64_t         AskWeightSize;      //卖方委托总数量, Qty,N15(2)
    int32_t         UpLimitPx;          //涨停价, MDEntryPx,N18(6) *
    int32_t         DnLimitPx;          //跌停价, MDEntryPx,N18(6) **
    struct price_level_t   BidLevel[10];//十档买盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    struct price_level_t   AskLevel[10];//十档卖盘，价格 MDEntryPx,N18(6)，数量 Qty,N15(2)
    uint64_t         TransactTime;      //YYYYMMDDHHMMSSsss(毫秒) 实际以3秒为变化单位
    uint8_t          Resv[4];
};
// *  涨停价取值为 999999999.9999 表示无涨停价格限制。
// ** 跌停价对于价格可以为负数的证券，取值为-999999999.9999 表示无跌停价格限制；对于价格不可以为负数的证券，值为证券的价格档位表示无跌停价格限制，比如对于股票填写 0.01。
```

> #### 深交所逐笔委托

```c
//对应深交所协议消息类型300192
struct SBE_SSZ_ord_t //48B
{
    struct SBE_SSZ_header_t  Header;    //msgType=192

    int32_t         Price;          //委托价格, Price,N13(4)
    int64_t         OrderQty;       //委托数量, Qty,N15(2)
    int8_t          Side;           //买卖方向: '1'=买, '2'=卖, 'G'=借入, 'F'=出借
    int8_t          OrdType;        //订单类别: '1'=市价, '2'=限价, 'U'=本方最优
    uint64_t        TransactTime;   //YYYYMMDDHHMMSSsss(毫秒) 实际以10ms为变化单位
    uint8_t         Resv[2];
};
```

> #### 深交所逐笔成交

```c
//对应深交所协议消息类型300191
struct SBE_SSZ_exe_t //64B
{
    struct SBE_SSZ_header_t  Header;    //msgType=191

    int64_t         BidApplSeqNum;  //买方委托索引 *
    int64_t         OfferApplSeqNum;//卖方委托索引 *
    int32_t         LastPx;         //成交价格, Price,N13(4)
    int64_t         LastQty;        //成交数量, Qty,N15(2)
    int8_t          ExecType;       //成交类别: '4'=撤销, 'F'=成交
    uint64_t        TransactTime;   //YYYYMMDDHHMMSSsss(毫秒) 实际以10ms为变化单位
    uint8_t         Resv[3];
};
// * 委托索引从 1 开始计数， 0 表示无对应委托
```

---

### 上交所sbe消息格式

> #### 上交所快照行情

SBE_SSH_header_t 与 SBE_header_t完全一致。
由于上交所交易阶段代码原始数据较大，消息头内只映射了第0Byte，其余额外定义一个字段放在消息体内：

对每个价格档位，仅保留其价格和成交量，未保留其50笔排队订单，这样减小数据量并且不影响我们用来校验重建的订单簿。

```c
typedef union TradingPhaseCodePack_t 
{
    uint8_t             Value;
    struct unpack{
        uint8_t         B1 : 2; //映射自交易阶段代码第1Byte
        uint8_t         B2 : 4; //映射自交易阶段代码第2Byte
        uint8_t         B3 : 2; //映射自交易阶段代码第3Byte
    } unpack;
}TradingPhaseCodePack_t;

//对应上交所消息类型UA3202 (股票、基金)
struct SBE_SSH_instrument_snap_t  // 336B
{
    struct SBE_SSH_header_t  Header;    //msgType=111

    int32_t         NumTrades;          //成交笔数
    int64_t         TotalVolumeTrade;   //成交总量, 3位小数
    int64_t         TotalValueTrade;    //成交总金额, 5位小数
    int32_t         PrevClosePx;        //昨收盘价格, 3位小数
    int32_t         LastPx;             //成交价格, 3位小数
    int32_t         OpenPx;             //开盘价格, 3位小数
    int32_t         HighPx;             //最高价格, 3位小数
    int32_t         LowPx;              //最低价格, 3位小数
    int32_t         BidWeightPx;        //加权平均委买价格, 3位小数
    int64_t         BidWeightSize;      //委托买入总量, 3位小数
    int32_t         AskWeightPx;        //加权平均委卖价格, 3位小数
    int64_t         AskWeightSize;      //委托卖出总量, 3位小数
    uint32_t        DataTimeStamp;      //最新订单时间(秒), 143025表示14:30:25
    struct price_level_t   BidLevel[10];//价格3位小数; 申买量3位小数
    struct price_level_t   AskLevel[10];//价格3位小数; 申卖量3位小数
    TradingPhaseCodePack_t TradingPhaseCodePack;
    uint8_t          Resv[3];
};

//对应上交所消息类型UA3802 （债券）
struct SBE_SSH_bond_snap_t
{
    struct SBE_SSH_header_t  Header;        //MsgType=38

    int32_t         NumTrades;              //成交笔数
    int64_t         TotalVolumeTrade;       //成交总量, 3位小数
    int64_t         TotalValueTrade;        //成交总金额, 5位小数
    int32_t         LastPx;                 //成交价格, 3位小数
    int32_t         OpenPx;                 //开盘价格, 3位小数
    int32_t         HighPx;                 //最高价格, 3位小数
    int32_t         LowPx;                  //最低价格, 3位小数
    int32_t         AltWeightedAvgBidPx;    //加权平均委买价格, 3位小数
    int64_t         TotalBidQty;            //委托买入总量, 3位小数
    int32_t         AltWeightedAvgOfferPx;  //加权平均委卖价格, 3位小数
    int64_t         TotalOfferQty;          //委托卖出总量, 3位小数
    uint32_t        DataTimeStamp;          //最新订单时间(毫秒), 143025002表示14:30:25.002
    struct price_level_t   BidLevel[10];    //价格3位小数; 申买量3位小数
    struct price_level_t   AskLevel[10];    //价格3位小数; 申卖量3位小数
};
```

> #### 上交所逐笔委托 （股票、基金）

```c
//对应上交所消息类型UA5801
struct SBE_SSH_ord_t  //56B
{
    struct SBE_SSH_header_t  Header;    //msgType=192

    int64_t         OrderNo;            //原始订单号 *
    int32_t         Price;              //委托价格（元）, 3位小数
    int64_t         OrderQty;           //委托数量, 3位小数
    int8_t          OrdType;            //订单类型: 'A'=新增委托订单, 'D'=删除委托订单
    int8_t          Side;               //买卖单标志: 'B'=买单, 'S'=卖单
    uint32_t        OrderTime;          //委托时间(百分之一秒), 14302506表示14:30:25.06
    uint8_t         Resv[6];
    uint64_t        BizIndex;           //业务序号
};
// * 竞价逐笔委托消息中的原始订单号(OrderNo)与竞价逐笔成交消息中买方订单号(TradeBuyNo)或卖方订单号(TradeSellNo)相对应。
```

> #### 上交所逐笔成交 （股票、基金）

```c
//对应上交所消息类型UA3201
struct SBE_SSH_exe_t  //64B
{
    struct SBE_SSH_header_t  Header;    //msgType=191

    int64_t         TradeBuyNo;         //买方订单号
    int64_t         TradeSellNo;        //卖方订单号
    int32_t         LastPx;             //成交价格（元）, 3位小数
    int64_t         LastQty;            //成交数量, 3位小数 *
    int8_t          TradeBSFlag;        //内外盘标志: 'B'=外盘，主动买; 'S'=内盘，主动卖; 'N'=未知 **
    uint32_t        TradeTime;          //委托时间(百分之一秒), 14302506表示14:30:25.06
    uint8_t         Resv[7];
    uint64_t        BizIndex;           //业务序号
};
// *  股票单位：股; 债券分销单位：千元面额; 基金单位：份
// ** 目前看集合竞价结束时的成交标志为'N'
```

> #### 上交所债券逐笔消息

```c
//用于映射上交所消息类型UA3901
struct SBE_SSH_ms_header_t            //逐笔合并流头部【重定义最后1byte】
{
    uint8_t     SecurityIDSource;   //=101
    uint8_t     MsgType;            //65/68/84/83
    uint16_t    MsgLen;             //include this header, until ending byte of SBE message
    char        SecurityID[9];      // c8 + '\0'
    uint16_t    ChannelNo;          //
    uint64_t    ApplSeqNum;         //TickIndex
    uint8_t     TickBSFlag;         //
}PACKED;


//对应上交所消息类型UA3901 && Type='A'
struct SBE_SSH_bond_order_add_t
{
    struct SBE_SSH_ms_header_t  Header;    //MsgType=65, TickBSFlag: 'B'=买单; 'S'=卖单

    int64_t         OrderNo;            //订单号
    int32_t         Price;              //价格（元）, 3位小数
    int64_t         Qty;                //数量（千元面额）, 3位小数
    uint32_t        TickTime;           //订单时间(毫秒), 143025006表示14:30:25.006
};


//对应上交所消息类型UA3901 && Type='D'
struct SBE_SSH_bond_order_del_t
{
    struct SBE_SSH_ms_header_t  Header;    //MsgType=68, TickBSFlag: 'B'=买单; 'S'=卖单

    int64_t         OrderNo;            //订单号
    int32_t         Resv;               //
    int64_t         Qty;                //数量（千元面额）, 3位小数
    uint32_t        TickTime;           //订单时间(毫秒), 143025006表示14:30:25.006
};


//对应上交所消息类型UA3901 && Type='T'
struct SBE_SSH_bond_trade_t
{
    struct SBE_SSH_ms_header_t  Header;    //MsgType=84, TickBSFlag: 'B'=外盘，主动买; 'S'=内盘，主动卖; 'N'=未知

    int64_t         BuyOrderNo;         //买方订单号
    int64_t         SellOrderNo;        //卖方订单号
    int32_t         Price;              //价格（元）, 3位小数
    int64_t         Qty;                //数量（千元面额）, 3位小数
    int64_t         TradeMoney;         //成交金额, 5位小数
    uint32_t        TickTime;           //成交时间(毫秒), 143025006表示14:30:25.006
};


//对应上交所消息类型UA3901 && Type='S'
struct SBE_SSH_bond_status_t            //债券逐笔合并流市场状态
{
    struct SBE_SSH_ms_header_t  Header;    //MsgType=83, TickBSFlag: 11=产品未上市; 0=启动; 1=开市集合竞价; 2=连续自动撮合; 6=停牌; 5=闭市; 12=交易结束;
};
```


## 上交所、深交所主要差异

* 精度
  * 价格小数位数：深交所快照除昨收外6位、快照昨收和逐笔均4位；上交所均为3位。
  * 数量小数位数：深交所2位；上交所3位。
  * 金额小数位数：深交所4位；上交所5位。
  * 时间戳精度：深交所号称都是1毫秒，实际快照字段精度为秒，逐笔字段精度为1毫秒；上海快照精度为秒，逐笔精度为10毫秒。
* 交易阶段代码
  * 深交所，消息头中TradingPhase的子字段
    * TradingPhase.unpack.Code0
      AX-SBE值|交易所值|说明
      --|--|--
      0|'S'|表示启动（开市前）
      1|'O'|表示开盘集合竞价
      2|'T'|表示连续交易
      3|'B'|表示休市
      4|'C'|表示收盘集合竞价
      5|'E'|表示已闭市
      6|'H'|表示临时停牌
      7|'A'|表示盘后交易
      8|'V'|表示波动性中断
      other|other|表示无意义

    * TradingPhase.unpack.Code1
      AX-SBE值|交易所值|说明
      --|--|--
      0|'0' |表示此产品正常状态
      1|'1' |表示此产品全天停牌
      other|' '(空格)|无意义，当成此产品可正常交易处理

  * 上交所，消息头中TradingPhase，映射自的TradingPhaseCode字段的第1位(char[0])
    AX-SBE值|交易所值|说明
    --|--|--
    0|'S'|表示启动（开市前）时段，对应债券快照 'START'
    1|'C'|表示开盘集合竞价时段，对应债券快照 'OCALL'
    2|'T'|表示连续交易时段，对应债券快照 'TRADE'
    5|'E'|表示闭市时段，对应债券快照 'CLOSE'
    6|'P'|表示产品停牌，对应债券快照 'SUSP'
    9|'M'|表示可恢复交易的熔断时段（盘中集合竞价）
    10|'N'|表示不可恢复交易的熔断时段（暂停交易至闭市）
    4|'U'|表示收盘集合竞价时段
    3|'B'|表示休市时段
    8|'V'|表示波动性中断
    11|'ADD'|表示产品未上市，仅债券快照存在
    12|'ENDTR'|表示交易结束，仅债券快照存在

  * 上交所，消息体中TradingPhaseCodePack的子字段
    * TradingPhaseCodePack.unpack.B1，映射自TradingPhaseCode字段的第2位(char[1])
      AX-SBE值|交易所值|说明
      --|--|--
      0|'0'|表示此产品不可正常交易
      1|'1'|表示此产品可正常交易
      other|' '(空格)|无意义，当成此产品可正常交易处理

    * TradingPhaseCodePack.unpack.B2
      * 当为股票时，映射自 MDStreamID= MD002/MD003/MD004的TradingPhaseCode字段的第3位(char[2])
        AX-SBE值|交易所值|说明
        --|--|--
        0|'0'|表示未上市
        1|'1'|表示已上市
        other|' '(空格)|无意义

      * 当为期权时，映射自 MDStreamID= MD301的TradingPhaseCode字段的第3位(char[2])
        AX-SBE值|交易所值|说明
        --|--|--
        0|'0'|表示不限制开仓
        1|'1'|表示限制备兑开仓
        2|'2'|表示限制卖出开仓
        3|'3'|表示限制卖出开仓、备兑开仓
        4|'4'|表示限制买入开仓
        5|'5'|表示限制买入开仓、备兑开仓
        6|'6'|表示限制买入开仓、卖出开仓
        7|'7'|表示限制买入开仓、卖出开仓、备兑开仓
        other|未定义|无意义

    * TradingPhaseCodePack.unpack.B3，映射自TradingPhaseCode字段的第4位(char[3])
      AX-SBE值|交易所值|说明
      --|--|--
      0|'0'|表示此产品在当前时段不接受订单申报
      1|'1'|表示此产品在当前时段可接受订单申报
      other|' '(空格)|无意义

---

## 历史数据格式

AX-sbe格式是对交易所数据的压缩，并便于CPU程序读取和使用，但不利于开发人员阅读。为进一步利于调试，我们将转换后的SBE数据保存成可阅读的文本文件，并规定了内容格式。

每条历史行情数据在文本文件中存成两行，按顺序为注释行和字符行：

* 注释行
    以```//```开头，以```字段名=字段值```显示，字段间用空格分开

    如：

    ```log
    //SecurityIDSource=102 MsgType=111 MsgLen=352 SecurityID=000001 ...
    ```

* 字符行

    以十六进制显示每个字段值，```SecurityIDSource=102```即对应```0x66```，一个行情消息结构体的所有字节值按顺序串成一行，每个字段以x86小端组织。

字符行与注释行的每个字段列对齐。注释行+字符行示例如下:

```log
//SecurityIDSource=102 MsgType=111 MsgLen=352 SecurityID=000001           ...
  66                   6F          60 01      30 30 30 30 30 31 20 20 00  ...
```
