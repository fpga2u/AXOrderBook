/*
* Copyright 2021 Xilinx, Inc.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
#include <ap_int.h>

#ifndef HBM_ENTRIES
#define HBM_ENTRIES (((256*8/512/2) << 20))   //单地址512b，单bank 256MB容量=256*8*2^20bit，即4M个地址
#endif

#ifndef BLENGTH
#define BLENGTH 1 //burst 长度，即连续进行多少次访问(每次512b)
#endif

#ifndef DATA_ELEMENTS
#define DATA_ELEMENTS 16//一次访问512bit / int为32bit = 16
#endif
const unsigned int VDATA_SIZE = DATA_ELEMENTS;

typedef struct v_datatype { unsigned int data[VDATA_SIZE]; } v_dt;
