# HBM仲裁器 每MU(2读 2写) * 2MU (每MU 128M空间)

TODO: MU测位宽应为32，写首拍为地址。

## 子目录

* arbiter: 仲裁器本体
* latency: 读响应计时器
* dmy_mu: 伪宏单元，用于测试仲裁器
* combine: 仲裁器本体 + 伪宏单元 联合测试，csim only，不可综合，因为arbiter接口是AXI4-Stream(仅可用于外部接口)
* vitis: 基于vites体系实机测试

## 仿真
1. 打开 ```Vitis HLS 2022.1 Command Prompt```
2. cd进入本目录下的 arbiter 或 combine 或 dmy_mu 或 lantency 目录
3. 根据需要修改 setting.tcl 文件，以便执行 CSIM / CSYNTH / COSIM 等过程，以及设定是 COSIM 是否需要波形等
4. 执行:

   ```sh
   vitis_hls run_hls.tcl
   ```
5. 查看vitis.log和波形

## 实机

**需要Linux。**

### 编译FPGA下载文件
1. 进入本目录下的 vitis 目录
2. 根据需要修改 setting.sh 文件，其中 TARGET 为 hw 时编译实机运行文件，为 hw_emu 时编译硬件模拟文件
3. 执行:

    ```sh
    source setting.sh
    source buildall.sh
    ```

### 运行测试

注意:如果是 hw_emu 则在C++或py进程退出时需要等待很久（半小时以上），不要用Ctrl-C打断，否则波形文件内容全是x。

#### C++
[说明](sw/README.md)

#### pynq
依赖 python 3.8+ / pynq 3.0.0

当前使用: Anaconda3-2021.04

1. 进入本目录下的 vitis 目录
2. 执行（其中xilinx、anaconda3路径根据实际情况修改）:
   
   ```sh
   export XILINX_XRT=/data/opt/xilinx/xrt
   source /data/Xilinx/Vivado/2022.1/settings64.sh
   source ../sw/build/setup_emu.sh -s on -p xilinx_u50_gen3x16_xdma_5_202210_1
   eval "$(/data/anaconda3/bin/conda shell.bash hook)"
   export EMCONFIG_PATH=$(pwd)
   python test_pynq.py
   ```


### vitis 测试

[XRT](/doc/XRT.md)

### 导出rtl ip
