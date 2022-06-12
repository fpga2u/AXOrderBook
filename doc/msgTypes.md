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
ChannelNo|通道号
ApplSeqNum|委托序列号，同一通道内的序号按顺序递增
Price|委托价格（非限价委托时无意义）
OrderQty|委托数量
Side|委托方向（卖/卖/借入/借出）
OrdType|委托类型（市价/限价/本方最优）
TransactTime|生成时间

---

## L2逐笔成交（execution）

交易所在撮合两笔订单成交后，就会发出一条逐笔成交消息；交易所在收到客户的撤单请求并撤单成功后，也会发出一条逐笔成交消息。

逐笔成交的常用字段包括：
字段|说明
--|--
SecurityID|证券代码
ChannelNo|通道号
ApplSeqNum|成交序列号，同一通道内的序号按顺序递增
BidApplSeqNum|买方序列号，与逐笔委托的序列号相同
OfferApplSeqNum|卖方序列号，与逐笔委托的序列号相同
LastPx|成交价格（撤单时无意义）
LastQty|成交数量
ExecType|执行类型（已成交/已撤销）

---

## 简单二进制编码（AX-SBE）

L2行情数据量很大，而且我们在python和FPGA HLS中都需要读入数据，为便于开发，我们将所需的三种消息重新进行编码：将消息映射成C语言结构体，并按x86小端模式存储字段值。这种编码模式我们称为简单二进制编码（AX-simple-binary-encoding）。

> sbe-header

所有sbe消息都按消息头+消息体的格式定义，其中消息头是统一的结构体：

```c
struct SBE_header_t
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
struct price_level_t
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

> 深交所消息头

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

> 深交所快照行情

对每个价格档位，仅保留其价格和成交量，未保留其50笔排队订单，这样减小数据量并且不影响我们用来校验重建的订单簿。

```c
struct SBE_SSZ_instrument_snap_t
{
    struct SBE_SSZ_header_t  Header;

    int64_t         NumTrades;
    int64_t         TotalVolumeTrade;
    int64_t         TotalValueTrade;
    int32_t         PrevClosePx;

    int32_t         LastPx;
    int32_t         OpenPx;
    int32_t         HighPx;
    int32_t         LowPx;

    int32_t         BidWeightPx;
    int64_t         BidWeightSize;
    int32_t         AskWeightPx;
    int64_t         AskWeightSize;
    int32_t         UpLimitPx;
    int32_t         DnLimitPx;
    struct price_level_t   BidLevel[10];
    struct price_level_t   AskLevel[10];
    uint64_t         TransactTime;
    uint8_t          Resv[4];
};
```

> 深交所逐笔委托

```c
struct SBE_SSZ_ord_t
{
    struct SBE_SSZ_header_t  Header;

    int32_t         Price;
    int64_t         OrderQty;
    int8_t          Side;
    int8_t          OrdType;
    uint64_t        TransactTime;
    uint8_t         Resv[2];
};
```

> 深交所逐笔成交

```c
struct SBE_SSZ_exe_t
{
    struct SBE_SSZ_header_t  Header;

    int64_t         BidApplSeqNum;
    int64_t         OfferApplSeqNum;
    int32_t         LastPx;
    int64_t         LastQty;
    int8_t          ExecType;
    uint64_t        TransactTime;
    uint8_t         Resv[3];
};
```

---

### 上交所sbe消息格式

> 上交所快照行情

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

struct SBE_SSH_instrument_snap_t
{
    struct SBE_SSH_header_t  Header;    //msgType=111

    int32_t         NumTrades;
    int64_t         TotalVolumeTrade;
    int64_t         TotalValueTrade;
    int32_t         PrevClosePx;
    int32_t         LastPx;
    int32_t         OpenPx;
    int32_t         HighPx;
    int32_t         LowPx;
    int32_t         BidWeightPx;
    int64_t         BidWeightSize;
    int32_t         AskWeightPx;
    int64_t         AskWeightSize;
    uint32_t        DataTimeStamp;
    struct price_level_t   BidLevel[10];
    struct price_level_t   AskLevel[10];
    TradingPhaseCodePack_t TradingPhaseCodePack;
    uint8_t          Resv[3];
};
```

> 上交所逐笔委托

```c
struct SBE_SSH_ord_t
{
    struct SBE_SSH_header_t  Header;    //msgType=192

    int64_t         OrderNo;
    int32_t         Price;
    int64_t         OrderQty;
    int8_t          OrdType;
    int8_t          Side;
    uint32_t        OrderTime;
    uint8_t         Resv[6];
};
```

> 上交所逐笔成交

```c
struct SBE_SSH_exe_t
{
    struct SBE_SSH_header_t  Header;    //msgType=191

    int64_t         TradeBuyNo;
    int64_t         TradeSellNo;
    int32_t         LastPx;
    int64_t         LastQty;
    int8_t          TradeBSFlag;
    uint32_t        TradeTime;
    uint8_t         Resv[7];
};
```

## 上交所、深交所主要差异

* 价格精度

* 数量精度

* 时间戳精度

* 交易阶段代码

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
