# HBM 多路访问仲裁器测试

## 目的

* 目前设计的思路是以```宏单元```作为设计单位，对HBM的访问也是按此组织。
* 从功能角度```宏单元```应屏蔽 HBM伪通道概念，对存储器的访问按功能分区。
* 单个```宏单元```需要访问的存储器功能区有：
  * ```宏单元```所有个股的委托数组，每个地址一条委托，单个```宏单元```需64MB或128MB空间
  * ```宏单元```每个价格档对应的委托链表，每个地址2个节点，单个```宏单元```需32MB空间
* 单个```宏单元```对功能区的访问有可能有多个模块进行，预计串行。
* 多个```宏单元```间对HBM的访问应该是并行的。
* 由于单个```宏单元```的功能区用不满一个bank，且多个```宏单元```共享bank会更灵活，因此按照功能区分配bank，即每个bank用于存储若干个```宏单元```的委托数组或档位链表中的一种。
* 故每个bank独立有一个```仲裁器```，用于处理多个```宏单元```的访问。

## 仲裁器与HBM关系

![Arbiter](/doc/pic/hbmArbiter_arbiter_hbm.png)

## 仲裁器与宏单元(MU)关系

![Arbiter](/doc/pic/hbmArbiter_arbiter_mu.png)

## HLS 设计

这个模块将是一个独立的顶层，即可以作为vitis中的.xo，也可以导出RTL IP使用。

由于MU侧的数量和接口不确定，先测试一种基本类型：每MU(2读2写) * 2MU，后续再采用宏编程方式生成需要的类型。

采用freerun模式，不需要握手。

后续在开发MU时，仲裁器作为tb的一部分使用。

### 接口

* 参数
  * 无
* MU侧
  * 每个MU
    * hls::stream<{addr:}>& rdi : 输入，读请求，addr位宽取决于功能区深度，32MB=19, 64MB=20, 128MB=21
    * hls::stream<{data:256b}>& rdo : 输出，读响应
    * hls::stream<{addr:,data:256b}>& wri : 输入，写请求，addr位宽与读请求相同
  * 读请求与读响应成对
  * 读写不必成对，可以有多组读，或多组写
  * 写优先
* HBM侧
  * ap_uint<512> hbmData[HBM_ENTRIES] : 读写hbm
* 寄存器
  * 每个MU
    * read i count, read ack count
    * write i count
    * max addr
  * HBM
    * read count, write count
* 协议
  * ap_ctrl_none : free run

### 子模块

![submodules](/doc/pic/hbmArbiter_sub.png)

* 每个MU对应一个MUM：
  * 读取MU的多路命令，写优先于读，写0优先于写1
  * 读写映射成内部统一的命令，输出
  * 读取后级反馈，主要是读数据输出回对应的读口
  * 一个MU内部认为命令是串行的，因此不会冲突
* 所有MUM由rr轮询访问HBM

## 实机测试

* 虚拟MU，由CPU指定写数据，写间隔，自读检查，循环次数；统计效率。
* 32个仲裁器
* CPU检查hbm数据
