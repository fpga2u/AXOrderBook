#!/bin/bash

if [ -z "${XILINX_XRT}" ]; then
    if [ ! -d /opt/xilinx/xrt/setup.sh ];then
        echo "XILINX XRT not found!"
        return 1
    fi
    source /opt/xilinx/xrt/setup.sh
fi

export PLATFORM_REPO_PATHS='/opt/xilinx/platforms'
export XILINX_PLATFORM='xilinx_u50_gen3x16_xdma_5_202210_1'
export DEVICE=${PLATFORM_REPO_PATHS}/${XILINX_PLATFORM}/${XILINX_PLATFORM}.xpfm
export XPART='xcu50-fsvh2104-2L-e'
export CLKP='330MHz'

echo "PLATFORM_REPO_PATHS : $PLATFORM_REPO_PATHS"
echo "XILINX_PLATFORM     : $XILINX_PLATFORM"
echo "DEVICE              : $DEVICE"
echo "XPART               : $XPART"
echo "CLKP                : $CLKP"

if [ ! -e $DEVICE ];then
   echo "===== ERROR ====="
   echo "$DEVICE not exists"
   return 1
fi
