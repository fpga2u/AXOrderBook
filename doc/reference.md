# 参考

## [How to Build a Fast Limit Order Book](/doc/ref_paper/howtohft_howtobuildafastlimitorderbook.pdf)

* 一个实现 [HFT-Orderbook](https://github.com/Crypto-toolbox/HFT-Orderbook)
* 主要讨论美股的限价订单簿(LOB)，A股的“市价单”和“对手最优单”可以在一定程度上转换成限价单插入到LOB中
* 定义了三种结构：
  * Order: 某个价位的委托链表，每个节点表示一个买入/卖出委托；每个委托有独立的订单号；新的委托总是加在链表的尾部，成交总是从头部开始。
  * Limit: 二叉树，每个节点表示一个价位，且包含此价位的委托链表指针。
  * Book: 包含买单树和卖单树，以及指向各自最优买/卖价格节点的指针。
* 同时采用```{订单号:*Order}```和```{价位:*Limit}```的两组```map```来快速查找
* 时间复杂度：
  * Add – O(log M) for the first order at a limit, O(1) for all others. #某个价格档首笔委托到达时需要在二叉树内插入一个节点，因此  间复杂度为O(log M) M为现有价格档数；后续委托通过其价格map到二叉树节点，因此为O(1)。
  * Cancel – O(1) # 通过订单号map到链表。
  * Execute – O(1)    # 通过订单号map到链表。
  * GetVolumeAtLimit – O(1)   #通过Book中最优价格指针直接获取，在Add/Cancel/Execute时需要维护最优价格指针。
  * GetBestBid/Offer – O(1)
* 空间复杂度：
  * ```{订单号:*Order}```和```{价位:*Limit}```的两组```map```如果时间复杂度为O(1)，则空间复杂度为O(n)。

