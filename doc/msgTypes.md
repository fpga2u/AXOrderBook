# L2行情消息细节

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
