# Copyright 2020 Xilinx Inc.
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

project(hbmArbiter_2_2_2_128m)
cmake_minimum_required(VERSION 3.0)

set(CMAKE_CXX_STANDARD 17)
set(XRT_INCLUDE_DIRS $ENV{XILINX_XRT}/include)
set(XRT_LIBS xrt_coreutil)

include_directories(
${XRT_INCLUDE_DIRS}
)

link_directories(
$ENV{XILINX_XRT}/lib
)

add_executable(hbmArbiter_2_2_2_128m_test 
src/hbmArbiter_2_2_2_128m_test.cpp
)

target_link_libraries(hbmArbiter_2_2_2_128m_test
${XRT_LIBS}
)

EXEC_PROGRAM(rm ARGS "-rf ./hbmArbiter_2_2_2_128m_test_emu.xclbin")

EXEC_PROGRAM(ln ARGS "-s ../../vitis/hbmArbiter_2_2_2_128m_test_emu.xclbin")
