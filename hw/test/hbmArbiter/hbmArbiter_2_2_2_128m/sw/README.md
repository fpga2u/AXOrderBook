# C版 host程序

## hw_emu

由于vitis自带的cmake版本较低，建议用两个shell终端进行测试，各用不同的环境变量。

```shell
##在第一个shell中 build sw
cd ./sw/build
export XILINX_XRT=/data/opt/xilinx/xrt
cmake ..
make

##在第二个shell中 run
cd ./sw/build
export XILINX_XRT=/data/opt/xilinx/xrt
source /data/Xilinx/Vivado/2022.1/settings64.sh
source setup_emu.sh -s on -p xilinx_u50_gen3x16_xdma_5_202210_1
./hbmArbiter_2_2_2_128m_test
```
