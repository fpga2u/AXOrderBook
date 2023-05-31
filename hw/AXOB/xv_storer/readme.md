# SBE 保存模块，用于在 XILINX VITIS 结构中接收MU/AXOB kernel发送的SBE消息，并保存到HBM/DDR中。

## 仿真和综合
1. 打开 ```Vitis HLS 2022.1 Command Prompt```
2. cd进入本目录
3. 根据需要修改 setting.tcl 文件，以便执行 CSIM / CSYNTH / COSIM 等过程，以及设定是 COSIM 是否需要波形等
4. 执行:

   ```sh
   vitis_hls run_hls.tcl
   ```

   日志示例: vitis_hls-gmem0-w1r1.log

5. 查看vitis.log和波形

## 实机

TODO:
