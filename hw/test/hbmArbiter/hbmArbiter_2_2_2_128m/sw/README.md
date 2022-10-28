# C版 host程序

由于vitis自带的cmake版本较低，建议用两个shell终端分别有不同的环境变量，一个用于编译，一个用于测试。

## 编译

```shell
##在第一个shell中
cd ./sw/build
export XILINX_XRT=/data/opt/xilinx/xrt
cmake ..
make
```

## hw_emu 仿真

```shell
##在第二个shell中
cd ./sw/build
export XILINX_XRT=/data/opt/xilinx/xrt
source /data/Xilinx/Vivado/2022.1/settings64.sh
source setup_emu.sh -s on -p xilinx_u50_gen3x16_xdma_5_202210_1
./hbmArbiter_2_2_2_128m_test

vitis_analyzer xrt.run_summary
```

## 实机测试

```shell
##在第二个shell中
cd ./sw/build
export XILINX_XRT=/data/opt/xilinx/xrt
source /data/Xilinx/Vivado/2022.1/settings64.sh
source setup_emu.sh -s off -p xilinx_u50_gen3x16_xdma_5_202210_1
./hbmArbiter_2_2_2_128m_test
```
