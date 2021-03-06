# 订单簿重建算法 python模型

使用python实现两种订单簿重建算法

## 主动式：模拟撮合 ([active model](active))

在收到逐笔委托后，就模拟交易所撮合机制进行成交判断并修改价格档位和订单队列，即刻生成新的订单簿。

优势：更新订单簿的速度快；在集合竞价阶段也可以发布订单簿；可以发布价格档位的订单队列。

劣势：为进行模拟撮合，必须按照价格和序列号（时间）两个维度来管理订单，数据结构复杂。

## 被动式：等待成交 ([passive model](passive))

由于交易所的成交消息是紧跟在委托之后的，所以可在收到委托后先缓存，待收齐对应的成交消息后，根据成交内容修改价格档位和订单队列，从而生成新的订单簿。

优势：不需要管理订单队列，数据结构简单。

劣势：更新订单簿的速度有延时；集合竞价阶段不能重建订单簿；只能发布价格档、没有对应的订单队列。

## 公共工具 ([tool](tool))

* msg_util: 行情数据类，可读取本项目使用的L2历史文件

* log_util: 日志工具

## 执行

python部分不是一个库，因此没有提供安装。

可执行脚本都在```AXOrderBook/py```目录中，都需在```AXOrderBook```目录下运行，如:

```s
cd AXOrderBook
python py/run_test.py
```

或使用vscode：

```t
先使用vscode打开整个AXOrderBook目录，再通过选择菜单"Run"->"Run Without Debugging"进行。
```

执行生成的log文件都在```AXOrderBook/log```中。
