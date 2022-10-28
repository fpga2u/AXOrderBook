# XRT

XRT是在Alveo加速卡上采用Vitis流程进行FPGA开发和部署时的软硬件中间层。

目前用到XRT提供的功能包括：

* 管理加速卡的静态区域和传感器等外围硬件，用xbmgmt工具。
* host程序的API
* 硬件仿真(hardware emulation)，XRT底层用XSIM跑仿真，可以和host的cpp或py程序交换，可以查看波形和模块调度情况。
* 实机测试

## 环境与版本

* CentOS7(3.10.0-1160.49.1.el7.x86_64)
  * Vitis 2022.1与之前的xilinx_u50_gen3x16_xdma_201920_3不兼容，需升级XRT和DEVICE([Xilix 下载页](https://www.xilinx.com/products/boards-and-kits/alveo/u50.html#gettingStarted))，当前文件：
    * Xilinx runtime (XRT) : xrt_202210.2.13.466_7.8.2003-x86_64-xrt.rpm
    * U50 Device:            xilinx-u50-gen3x16-xdma_2022.1_2022_0415_2123-noarch.rpm.tar.gz
    * U50 Device 开发:        xilinx-u50-gen3x16-xdma-5-202210-1-dev-1-3499627.noarch.rpm

  * CentOS8Stream(4.18.0-348.7.1.el8_5.x86_64)
    * Xilinx runtime (XRT) : xrt_202210.2.13.466_8.1.1911-x86_64-xrt.rpm
    * U50 Device     (同CentOS7): xilinx-u50-gen3x16-xdma_2022.1_2022_0415_2123-noarch.rpm.tar.gz
    * U50 Device 开发 (同CentOS7): xilinx-u50-gen3x16-xdma-5-202210-1-dev-1-3499627.noarch.rpm

## 当前的XRT命令手册

[xbmgmt](https://xilinx.github.io/XRT/master/html/xbmgmt.html)

* 常用命令
  
```shell
#Root privileges are required
sudo su

#环境变量
source /opt/xilinx/xrt/setup.sh

#重烧成golden(需冷启动)，如果已经烧了 U50_revert_to_golden.mcs 可以不用执行
/opt/xilinx/xrt/bin/xbmgmt program --device 01:00.0 --revert-to-golden

#显示当前U50信息
/opt/xilinx/xrt/bin/xbmgmt examine --device 01:00.0  --report all

#烧成最新的shell(需冷启动)
/opt/xilinx/xrt/bin/xbmgmt program --device 01:00.0 --base --image xilinx_u50_gen3x16_xdma_base_5

#加载我们的计算模块
/opt/xilinx/xrt/bin/xbmgmt program --device 01:00.0 --user hbmArbiter_2_2_2_128m_test.xclbin

#强制复位，应用层将与shell断开，所有应用必须重启
/opt/xilinx/xrt/bin/xbmgmt reset --device 01:00.0
```

## build XRT from source

```shell
git clone https://github.com/Xilinx/XRT.git
cd XRT
git submodule update --init

#假设Vitis安装在/data/Xilinx/Vitis/2022.1 :
export XILINX_VITIS=/data/Xilinx/Vitis/2022.1
sudo ./src/runtime_src/tools/scripts/xrtdeps.sh
# 如果 pybind11 安装失败，修改 xrtdeps.sh 中 "pip3 install -U pybind11" 为 "pip3 install -U pybind11 -i https://pypi.tuna.tsinghua.edu.cn/simple"

# 自行下载boost解压，假设解压到/data/cnmdp/boost_1_75_0（即b2可执行文件直接在boost_1_75_0中）
./src/runtime_src/tools/scripts/boost.sh -srcdir /data/cnmdp/boost_1_75_0 -noclone
# 或者之前已经安装到/usr/local，尝试按XRT需要重新安装
# sudo ./src/runtime_src/tools/scripts/boost.sh -srcdir /data/cnmdp/boost_1_75_0 -noclone -install /usr/local

cd build
./build.sh -with-static-boost $(pwd)/../boost/xrt

cd Release
make package

sudo yum install xrt_202310.2.15.0_8.5.2111-x86_64-xrt.rpm
```

## hw_emu

TODO:放vitis阐述

sudo su
source /opt/xilinx/xrt/setup.sh
export XCL_EMULATION_MODE=hw_emu
export EMCONFIG_PATH=$(pwd)
echo $EMCONFIG_PATH
source /data/Xilinx/Vitis_HLS/2022.1/settings64.sh
emconfigutil --platform xilinx_u50_gen3x16_xdma_5_202210_1

hw_emu 退出时要等很久（半小时?），波形要等完全退出才会在当前目录下看到，在.run目录里的波形都是X。
hw_emu 期间可以用debug_mode=gui开波形窗口，期间点击窗口上的暂停键可以暂停并加信号，如果kernel卡住，这是目前唯一看波形的方法。
hw_emu 期间在程序所在的.run目录下会生成临时文件，需要手动删除。
hw_emu 期间卡住目前只能杀进程。

## 编译加速卡动态区域

TODO:放vitis阐述

1. 从源代码到rtl，以kernel为单位，输出格式为xo，是接口说明和代码的封装
.cpp -> vitis_hls 或 v++ -> .xo
.v -> vivado -> .xo

2. link多kernel成动态区域下载文件或hw_emu仿真文件
.xo, .cfg -> v++ -> .xclbin
