# SBE 加载模块，用于在 XILINX VITIS 结构中将SBE消息从HBM/DDR中读取出来，传送给MU/AXOB kernel。

## 仿真和综合
1. 打开 ```Vitis HLS 2022.1 Command Prompt```
2. cd进入本目录
3. 根据需要修改 setting.tcl 文件，以便执行 CSIM / CSYNTH / COSIM 等过程，以及设定是 COSIM 是否需要波形等
4. 执行:

   ```sh
   vitis_hls run_hls.tcl
   ```

   日志示例: vitis_hls-example.log

5. 查看vitis.log和波形

## 实机

TODO:

## 注意点

* host_frame_i指定[64]是为了防止co-sim失败。
* register全部用值+接口分离模式，防止在co-sim中死锁。
