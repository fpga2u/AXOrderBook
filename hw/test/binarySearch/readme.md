# HLS 二进制查找RAM内容

默认RAM为72bx2048，每个地址前48b为搜索key，后24位为数据。

## 仿真
1. 打开 ```Vitis HLS 2022.1 Command Prompt```
2. cd进入本目录
3. 根据需要修改 setting.tcl 文件，以便执行 CSIM / CSYNTH / COSIM 等过程，以及设定是 COSIM 是否需要波形等
4. 执行:

   ```sh
   vitis_hls run_hls.tcl
   ```

5. 查看vitis.log和波形

## BRAM使用情况说明

1. 由于 72b 中目前只有 48b 被使用，所以vitis综合成了 48bx2048 的ram。
2. 48bx2048 可以由 36bx1024 *2 + 18bx2048 *1组成，即3个36Kb BRAM。
3. vitis.log中的BRAM单位是18Kb BRAM，所以报告中BRAM使用量为6。
