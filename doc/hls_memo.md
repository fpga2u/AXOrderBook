# HLS 记录

**不一定对，随时会改。**

* 函数
  * 函数即模块
  * 当有static变量时，多次调用函数时csim就可能出问题，因为static是共享的，即相当于强制inline了
  * 需要用模板来防止static共享
  * 通用结构：
    * xxx为功能名
    * xxx_top()为模块仿真、cosim测试、vitis xo导出、IP导出时的顶层
      * 用extern "C"修饰
      * 一般为dataflow
      * 用pragma申明接口
      * 调用xxx()
      * 不申明其它变量，不调用其它函数，只将接口信号传递给xxx()
    * xxx()为真正功能实现
      * 为模板类的静态函数，或类的静态模板
        * 当需要多次例化时，应为模板
        * 当只需一次例化时，可无需做模板
      * 建议自身为dataflow
      * 尽量只做子函数调用，不写逻辑
    * 因此至少有3个逻辑代码文件:xxx.h、xxx_top.h、xxx_top.cpp 
    * 至少有1个tb文件:xxx_tb.cpp
    * 某些用于测试的特殊模块，如多IP联合测试用的top
      * 在测试中只有一个实例时，直接调用xxx()，不调用xxx_top()
      * 只需要include xxx.h
    * TODO: 用脚本生成文件结构和接口
* dataflow
  * 可嵌套
* 寄存器
  * 目前前后guard是为了在vitis中读寄存器时可以确定地址范围
* pragma
* hls::stream
  * ```hls::stream<ap_axis/axiu<?,?,?,?>>``` 用于模块接口，而非子模块间
  * ```hls::stream<ap_uint<n>>``` 用于模块内部，FIFO或PIPO
* ap_ctrl_none
  * freerun模式
  * 对外接口或子模块间通信必须使用FIFO (hls::stream, streamed arrays, AXIS)，不能用memory
  * 从最底层到top模块都必须是dataﬂow(但不能是"dataﬂow-in-loop")，且定义为ap_ctrl_none
  * 因此不能用 sequental or pipelined FSM，或"dataﬂow-in-loop"
    * 除非在ap_ctrl_chain中使用的ap_ctrl_none
  * **谨慎使用Non-blocking式的读，其容易导致csim和实机不一致，因为无法在c中模拟正确的执行次数**

## 命名规则

### 模块顶层接口命名

* 大写
* ```<功能描述>_<I/O>```
  * I/O均针对本模块
