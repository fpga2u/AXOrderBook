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

[XRT](/doc/XRT.md)

### 导出rtl ip
