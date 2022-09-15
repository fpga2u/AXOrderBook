# U50 HBM HLS 性能测试

## 来源

* kernel：

    [Xilinx教程](https://github.com/Xilinx/Vitis-Tutorials)

    /Hardware_Acceleration/Feature_Tutorials/07-using-hbm/reference_files

## 修改说明

* vitis流程改为vivado流程
* 接口从 unsigned int data[16] 改为 ap_uint<512>
  
## 运行

1. 打开 ```Vitis HLS 2022.1 Command Prompt```
2. cd进入本目录
3. 执行:

   ```sh
   vitis_hls run_hls.tcl
   ```

4. 日志在```vitis_hls.log```，可与标准日志```vitis_hls_64x16.log```比较

## 配置文件说明

* settings.tcl
  * U50/U280有HBM，U200/U250都是DDR。
  * vitis 运行阶段控制文件，默认运行 ```CSIM -> CSYNTH -> COSIM``` 3个阶段，可手动修改增加或减少阶段，但尽量不要跳过中间阶段直接执行后面的阶段。
