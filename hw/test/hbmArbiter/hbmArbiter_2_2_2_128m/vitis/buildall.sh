#!/usr/bin/env bash

#
# Copyright 2020 Xilinx, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# set pipefail to catch and exit on any errors
set -Eeuo pipefail

BASE_DIR=$(dirname $(readlink -f $0))

# check platform target, avoid delayed build failure at xclbin generation stage
if [ -z "${XILINX_PLATFORM}" ]; then
    source setting.sh
    if [ $? -ne 0 ]; then
        echo "ERROR: Environment variable XILINX_PLATFORM is required"
        exit 1
    fi
fi

# xilinx kernel objects (xo's)
pushd ${BASE_DIR}/../arbiter
make DEVICE=${DEVICE} XPART=${XPART} CLKP=${CLKP} all
popd

pushd ${BASE_DIR}/../dmy_mu
make DEVICE=${DEVICE} XPART=${XPART} CLKP=${CLKP} all
popd

pushd ${BASE_DIR}/../latency
make DEVICE=${DEVICE} XPART=${XPART} CLKP=${CLKP} all
popd

# xilinx binary container (xclbin)
pushd ${BASE_DIR}
make binary-container
popd

