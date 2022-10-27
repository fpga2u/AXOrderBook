# -*- coding: utf-8 -*-


# import setuptools

import pynq
from pynq import Device

import numpy as np
np.set_printoptions(formatter={'int': hex}, threshold=1000)


bin_file = 'hbmArbiter_2_2_2_128m_test_emu.xclbin'

####### 通用信息
# shell应为 xilinx_u50_gen3x16_xdma_base_5
devices = Device.devices
for i in range(len(devices)):
    print("{}) {}".format(i, devices[i].name))

# 装载xclbin
ol = pynq.Overlay(bin_file)

# 时钟信息
print(ol.clock_dict)

# CU列表
print(ol.ip_dict.keys())

# CU寄存器值
for k in ol.ip_dict:
    print("{}.{}".format(k, ol.__getattr__(k).register_map))

# CU调用接口信息
for k in ol.ip_dict:
    print("{}{}".format(k, ol.__getattr__(k).signature))

#######
hbmArbiter = ol.hbmArbiter_2_2_2_128m_top_1
mu0 = ol.mu0
mu1 = ol.mu1

lm_mu0_rd0 = ol.lm_mu0_rd0
lm_mu0_rd1 = ol.lm_mu0_rd1

lm_mu1_rd0 = ol.lm_mu1_rd0
lm_mu1_rd1 = ol.lm_mu1_rd1

#TODO: 可以读出值吗？不行的话只需要一个DMY
mu0_reg_guard_bgn = pynq.allocate((1, 1), dtype='u4')
mu0_wr0_wk_nb = pynq.allocate((1, 1), dtype='u4')
mu0_wr1_wk_nb = pynq.allocate((1, 1), dtype='u4')
mu0_rd0_wk_nb = pynq.allocate((1, 1), dtype='u4')
mu0_rd1_wk_nb = pynq.allocate((1, 1), dtype='u4')
mu0_rdo0_rx_nb = pynq.allocate((1, 1), dtype='u4')
mu0_rdo1_rx_nb = pynq.allocate((1, 1), dtype='u4')
mu0_rd0err_nb = pynq.allocate((1, 1), dtype='u4')
mu0_rd1err_nb = pynq.allocate((1, 1), dtype='u4')
mu0_gap_wk_nb = pynq.allocate((1, 1), dtype='u4')
mu0_reg_guard_end = pynq.allocate((1, 1), dtype='u4')

mu0s = mu0.start(
    reg_guard_bgn = mu0_reg_guard_bgn, 
    wk_nb = 16, 
    min_addr = 0,
    max_addr = 16, 
    min_data = 0,
    gap_nb = 4, 
    wr0_wk_nb = mu0_wr0_wk_nb,
    wr1_wk_nb = mu0_wr1_wk_nb,
    rd0_wk_nb = mu0_rd0_wk_nb,
    rd1_wk_nb = mu0_rd1_wk_nb,
    rdo0_rx_nb = mu0_rdo0_rx_nb,
    rdo1_rx_nb = mu0_rdo1_rx_nb,
    rd0err_nb = mu0_rd0err_nb,
    rd1err_nb = mu0_rd1err_nb,
    gap_wk_nb = mu0_gap_wk_nb,
    reg_guard_end = mu0_reg_guard_end
)



# mu0_start.waite() #TODO: 当前会卡住


# CU寄存器值
for k in ol.ip_dict:
    print("{}.{}".format(k, ol.__getattr__(k).register_map))


###### clean up
del mu0_reg_guard_bgn
del mu0_wr0_wk_nb
del mu0_wr1_wk_nb
del mu0_rd0_wk_nb
del mu0_rd1_wk_nb
del mu0_rdo0_rx_nb
del mu0_rdo1_rx_nb
del mu0_rd0err_nb
del mu0_rd1err_nb
del mu0_gap_wk_nb
del mu0_reg_guard_end
