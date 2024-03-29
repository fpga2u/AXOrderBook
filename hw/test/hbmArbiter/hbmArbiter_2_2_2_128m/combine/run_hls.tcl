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

if { [catch { set uname_r [exec uname] } conn_handle] } {
    puts $conn_handle
    set isLinux 0
} else {
    if {[string equal ${uname_r} "Linux"]} {
        set isLinux 1
    } else {
        set isLinux 0
    }
}
puts "isLinux=${isLinux}"

if { [catch { [ string length $::env(EXPORT_XO_ONLY) ] } conn_handle] } {
    # Using setting.tcl
    puts $conn_handle
    source settings.tcl
    puts "Using XPART=setting(${XPART})"
    puts "Using CLKP=setting(${CLKP})"
    puts "Using EXPORT_XO_ONLY=setting(${EXPORT_XO_ONLY})"
} else {
    # Using environment variable
    set XPART $::env(XPART)
    puts "Using XPART=Env(${XPART})"

    set CLKP $::env(CLKP)
    puts "Using CLKP=Env(${CLKP})"

    set EXPORT_XO_ONLY $::env(EXPORT_XO_ONLY)
    puts "Using EXPORT_XO_ONLY=Env(${EXPORT_XO_ONLY})"
}

set TOP_NAME "comb_2_2_2_128m_top"
set PROJ "prj_${TOP_NAME}"
set SOLN "sol"
set CASE_ROOT [pwd]
set KERNEL_ROOT "${CASE_ROOT}"
set ARBITER_ROOT "${CASE_ROOT}/../arbiter"
set MU_ROOT "${CASE_ROOT}/../dmy_mu"
set LM_ROOT "${CASE_ROOT}/../latency"

if {$EXPORT_XO_ONLY == 0} {
    set DEF_C_TEST "-D_C_TEST_"
} else {
    set DEF_C_TEST ""
}

if {$EXPORT_XO_ONLY == 1} {
    set PROJ "xo_prj"
}

open_project -reset $PROJ

add_files "${KERNEL_ROOT}/comb_2_2_2_128m_top.cpp" -cflags "-I${KERNEL_ROOT} -I${ARBITER_ROOT} -I${MU_ROOT} -I${LM_ROOT} ${DEF_C_TEST}"
add_files "${ARBITER_ROOT}/hbmArbiter_2_2_2_128m_top.cpp" -cflags "-I${ARBITER_ROOT} -I${ARBITER_ROOT} ${DEF_C_TEST}"

if {$EXPORT_XO_ONLY == 0} {
    add_files -tb "comb_2_2_2_128m_tb.cpp" -cflags "-I${KERNEL_ROOT} -I${ARBITER_ROOT} -I${MU_ROOT} -I${LM_ROOT} -D_C_TEST_"
}

set_top ${TOP_NAME}

if {$EXPORT_XO_ONLY == 0} {
    set FLOW_TARGET "vivado"
} else {
    set FLOW_TARGET "vitis"
}
open_solution -reset $SOLN -flow_target ${FLOW_TARGET}

set_part $XPART
create_clock -period $CLKP -name default

if {$EXPORT_XO_ONLY == 1} {
    # config_sdx -target xocc
    csynth_design
    export_design -rtl verilog -format xo -output ${KERNEL_ROOT}/${TOP_NAME}.xo
    exit
}

if {$isLinux == 0} {
    set LDFLAGS "{-Wl,--stack,10737418240}"
} else {
    set LDFLAGS "{-z stack-size=10737418240}"
}
if {$CSIM == 1} {
    csim_design -ldflags ${LDFLAGS}
}

if {$CSYNTH == 1} {
  csynth_design
}

if {$COSIM == 1} {
    if {$WAVE_DEBUG == 1} {
        if {$TRACE_LEVEL_ALL == 1} {
            set TRACE_LEVEL "all"
        } else {
            set TRACE_LEVEL "port_hier"
        }
        cosim_design -ldflags ${LDFLAGS} -wave_debug -trace_level ${TRACE_LEVEL} 
    } else {
        cosim_design -ldflags ${LDFLAGS}
    }
}

if {$VIVADO_SYN == 1} {
  export_design -flow syn -rtl verilog
}

if {$VIVADO_IMPL == 1} {
  export_design -flow impl -rtl verilog
}

if {$QOR_CHECK == 1} {
  puts "QoR check not implemented yet"
}

exit
