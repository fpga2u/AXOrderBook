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

MK_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CUR_DIR=$(patsubst %/,%,$(dir $(MK_PATH)))

KERNEL_DIR=$(CUR_DIR)

KERNEL=lm_2_2_2_128m_top

SRCS=$(KERNEL_DIR)/lm_2_2_2_128m_top.cpp \
     $(KERNEL_DIR)/lm_2_2_2_128m_top.h \
     $(KERNEL_DIR)/latencyMoniter.h

# default build parameters
XPART?=xcu50-fsvh2104-2L-e
CLKP?=330MHz
TARGET?=hw

.PHONY: all
all: $(KERNEL)

$(KERNEL): $(SRCS)
	-rm -rf xo_prj
	XPART=$(XPART) CLKP=$(CLKP) TARGET=$(TARGET) EXPORT_XO_ONLY=1 vitis_hls -f run_hls.tcl

.PHONY: clean
clean:
	-rm -rf xo_prj
	-rm -f *.xo
	-rm -f *.log
