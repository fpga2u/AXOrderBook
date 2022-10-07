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

# Makefile for xclbin creation
#

#+-------------------------------------------------------------------------------
# The following parameters are assigned with default values. These parameters can
# be overridden through the make command line
#+-------------------------------------------------------------------------------

REPORT := no
PROFILE := no
DEBUG := no
TARGET := hw

#'estimate' for estimate report generation
#'system' for system report generation
ifneq ($(REPORT), no)
CLFLAGS += --report estimate
LDCLFLAGS += --report system
endif

# generates profile summary report
ifeq ($(PROFILE), yes)
LDCLFLAGS += --profile_kernel data:all:all:all
endif

# generates debug summary report
ifeq ($(DEBUG), yes)
CLFLAGS += --dk protocol:all:all:all
endif

# hw emu: trace
ifeq ($(TARGET), hw_emu)
CLFLAGS += -g
endif

# configuration settings
VPP := $(XILINX_VITIS)/bin/v++

# extract platform name only from full path to xpfm
XILINX_PLATFORM=$(basename $(notdir $(DEVICE)))


ifeq ($(TARGET), hw_emu)
PROJECT = hbmArbiter_2_2_2_128m_test_emu
else
PROJECT = hbmArbiter_2_2_2_128m_test
endif


ARBITER_XO := hbmArbiter_2_2_2_128m_top.xo
DMY_MU_XO := dmy_mu_2_2_2_128m_top.xo
LATENCY_XO := lm_2_2_2_128m_top.xo


ARBITER_XO_FULLPATH=../arbiter/$(ARBITER_XO)
DMY_MU_XO_FULLPATH=../dmy_mu/$(DMY_MU_XO)
LATENCY_XO_FULLPATH=../latency/$(LATENCY_XO)

# shell specific connectivity
ifneq (,$(shell echo $(XILINX_PLATFORM) | awk '/_u50_gen.*_xdma_/'))
VPPLINKFLAGS := --config hbmArbiter_2_2_2_128m_test.cfg
# else ifneq (,$(shell echo $(XILINX_PLATFORM) | awk '/_u250_gen.*_xdma_/'))
# VPPLINKFLAGS := --config atrd.u250.ini
else
$(error Unsupported XILINX_PLATFORM=$(XILINX_PLATFORM))
endif

XODIR = xo
XOS = $(ARBITER_XO)\
      $(DMY_MU_XO)\
	  $(LATENCY_XO)

CLFLAGS += -t $(TARGET) --platform $(DEVICE) --save-temps

$(XODIR):
	mkdir $@

# gather up external kernels
xo/$(ARBITER_XO): $(ARBITER_XO_FULLPATH) | $(XODIR)
	cp $< $@
xo/$(DMY_MU_XO): $(DMY_MU_XO_FULLPATH) | $(XODIR)
	cp $< $@
xo/$(LATENCY_XO): $(LATENCY_XO_FULLPATH) | $(XODIR)
	cp $< $@

BINARY_CONTAINER = $(PROJECT).xclbin
BINARY_CONTAINER_XOS = $(addprefix $(XODIR)/,$(XOS))

.PHONY: gather-xos
gather-xos: $(BINARY_CONTAINER_XOS)

.PHONY: binary-container
binary-container: $(BINARY_CONTAINER)

$(BINARY_CONTAINER): $(BINARY_CONTAINER_XOS)
	$(VPP) $(CLFLAGS) $(LDCLFLAGS) -l -o $@ $^ $(VPPLINKFLAGS)

.PHONY: clean
clean:
	-rm -f $(PROJECT).xclbin* $(PROJECT).ltx
	-rm -rf _x .Xil
	-rm -f *.log

realclean: clean
	-rm -rf xo/

.PHONY: help
help:
	@echo "Makefile usage:"
	@echo "  make binary-container TARGET=<hw/hw_emu> Generate hardware build (xclbin)"
	@echo "  make clean             Clean intermediate build folders"
	@echo "  make realclean         Clean + remove imported kernel objects (xo)"
