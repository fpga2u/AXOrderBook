# Using xilinx_u50_gen3x16_xdma_5_202210_1

当前的XRT命令手册：

[xbmgmt](https://xilinx.github.io/XRT/master/html/xbmgmt.html)

* 常用命令
  
```shell
#环境变量
source /opt/xilinx/xrt/setup.sh

#重烧成golden(需冷启动)，如果已经烧了 U50_revert_to_golden.mcs 应该可以不用执行
/opt/xilinx/xrt/bin/xbmgmt program  --device 01:00.0 --revert-to-golden

#显示当前U50信息
/opt/xilinx/xrt/bin/xbmgmt examine --device 01:00.0  --report all

#烧成最新的shell(需冷启动)
/opt/xilinx/xrt/bin/xbmgmt program --device 01:00.0 --base --image xilinx_u50_gen3x16_xdma_base_5

#加载我们的计算模块
/opt/xilinx/xrt/bin/xbmgmt program --device 01:00.0 --user hbmArbiter_2_2_2_128m_test.xclbin

#强制复位，应用层将与shell断开，所有应用必须重启
/opt/xilinx/xrt/bin/xbmgmt reset --device 01:00.0
```
