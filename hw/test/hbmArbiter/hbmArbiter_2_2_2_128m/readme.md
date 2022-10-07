# HBM仲裁器 每MU(2读 2写) * 2MU (每MU 128M空间)

TODO: MU测位宽应为32，写首拍为地址。

## 子目录

* arbiter: 仲裁器本体
* latency: 读响应计时器
* dmy_mu: 伪宏单元，用于测试仲裁器
* combine: 仲裁器本体 + 伪宏单元 联合测试，csim only，不可综合，因为arbiter接口是AXI4-Stream(仅可用于外部接口)
* vitis: 基于vites体系实机测试

## 仿真

## 实机

### vitis 测试

#### 环境与版本

* CentOS7(3.10.0-1160.49.1.el7.x86_64)
* Vitis 2022.1与之前的xilinx_u50_gen3x16_xdma_201920_3不兼容，需升级XRT和DEVICE([Xilix 下载页](https://www.xilinx.com/products/boards-and-kits/alveo/u50.html#gettingStarted))，当前文件：
  * Xilinx runtime (XRT) : xrt_202210.2.13.466_7.8.2003-x86_64-xrt.rpm
  * U50 Device: xilinx-u50-gen3x16-xdma_2022.1_2022_0415_2123-noarch.rpm.tar.gz
  * U50 Device 开发:xilinx-u50-gen3x16-xdma-5-202210-1-dev-1-3499627.noarch.rpm

### 导出rtl ip
