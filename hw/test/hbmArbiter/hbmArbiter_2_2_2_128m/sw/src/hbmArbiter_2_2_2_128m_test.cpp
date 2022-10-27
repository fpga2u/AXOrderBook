/*
 * Copyright 2022 Xilinx, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <chrono>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sys/mman.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#include "experimental/xrt_kernel.h"


// Please use 'xbutil examine' command to get the device id of the target alveo card if multiple
//   cards are installed in the system.
#define DEVICE_ID   0


struct kernel_reg_t{
    std::string name;
    int id;
    uint32_t offset;

    kernel_reg_t(const std::string& name_, int id_, uint32_t offset_):
        name(name_), id(id_), offset(offset_)
    {}
};

int main(int argc, char *argv[])
{

    int file_size;   // font file size in bytes
    int i;

    // Judge emulation mode accoring to env variable
    std::string xclbin_file;
    char *env_emu;
    if (env_emu = getenv("XCL_EMULATION_MODE"))
    {
        std::string mode(env_emu);
        if (mode == "hw_emu")
        {
            std::cout << "[MESSAGE] Program running in hardware emulation mode" << std::endl;
            xclbin_file = "hbmArbiter_2_2_2_128m_test_emu.xclbin";
        }
        else
        {
            std::cout << "[ERROR] Unsupported Emulation Mode: " << mode << std::endl;
            return EXIT_FAILURE;
        }
    }
    else
    {
        std::cout << "[MESSAGE] Program running in hardware mode" << std::endl;
        xclbin_file = "hbmArbiter_2_2_2_128m_test.xclbin";
    }

    // Load xclbin
    std::cout << "Load " << xclbin_file << std::endl;
    xrt::device device = xrt::device(DEVICE_ID);
    xrt::uuid xclbin_uuid = device.load_xclbin(xclbin_file);

   // create kernel objects
    std::cout << "Create kernels" << std::endl;
    xrt::kernel hbmArbiter = xrt::kernel(device, xclbin_uuid, "hbmArbiter_2_2_2_128m_top_1", xrt::kernel::cu_access_mode::exclusive);
    xrt::kernel mu0 = xrt::kernel(device, xclbin_uuid, "mu0", xrt::kernel::cu_access_mode::exclusive);
    xrt::kernel mu1 = xrt::kernel(device, xclbin_uuid, "mu1", xrt::kernel::cu_access_mode::exclusive);
    xrt::kernel lm_mu0_rd0 = xrt::kernel(device, xclbin_uuid, "lm_mu0_rd0", xrt::kernel::cu_access_mode::exclusive);
    xrt::kernel lm_mu0_rd1 = xrt::kernel(device, xclbin_uuid, "lm_mu0_rd1", xrt::kernel::cu_access_mode::exclusive);
    xrt::kernel lm_mu1_rd0 = xrt::kernel(device, xclbin_uuid, "lm_mu1_rd0", xrt::kernel::cu_access_mode::exclusive);
    xrt::kernel lm_mu1_rd1 = xrt::kernel(device, xclbin_uuid, "lm_mu1_rd1", xrt::kernel::cu_access_mode::exclusive);

    // define kernel address, TODO: from kernl.xml
    //id | name | offset 
    const std::vector<kernel_reg_t> hbmArbiter_regs = {
        { 'reg_guard_bgn', 0, 0x10 },
        { 'mu0_rdi0_nb', 1, 0x20 },
        { 'mu0_rdi1_nb', 2, 0x30 },
        { 'mu0_wri0_nb', 3, 0x40 },
        { 'mu0_wri1_nb', 4, 0x50 },
        { 'mu0_rdo0_nb', 5, 0x60 },
        { 'mu0_rdo1_nb', 6, 0x70 },
        { 'mu0_max_addr', 7, 0x80 },
        { 'mu1_rdi0_nb', 8, 0x90 },
        { 'mu1_rdi1_nb', 9, 0xA0 },
        { 'mu1_wri0_nb', 10, 0xB0 },
        { 'mu1_wri1_nb', 11, 0xC0 },
        { 'mu1_rdo0_nb', 12, 0xD0 },
        { 'mu1_rdo1_nb', 13, 0xE0 },
        { 'mu1_max_addr', 14, 0xF0 },
        { 'hbm_rd_nb', 15, 0x100 },
        { 'hbm_wr_nb', 16, 0x110 },
        { 'reg_guard_end', 17, 0x120 },
    };
    const std::vector<kernel_reg_t> mu_regs = {
        { "reg_guard_bgn", 0, 0x10  },
        { "wk_nb", 1, 0x20  },
        { "min_addr", 2, 0x28  },
        { "max_addr", 3, 0x30  },
        { "min_data", 4, 0x38  },
        { "gap_nb", 5, 0x40  },
        { "wr0_wk_nb", 6, 0x48  },
        { "wr1_wk_nb", 7, 0x58  },
        { "rd0_wk_nb", 8, 0x68  },
        { "rd1_wk_nb", 9, 0x78  },
        { "rdo0_rx_nb", 10, 0x88  },
        { "rdo1_rx_nb", 11, 0x98  },
        { "rd0err_nb", 12, 0xA8  },
        { "rd1err_nb", 13, 0xB8  },
        { "gap_wk_nb", 14, 0xC8  },
        { "reg_guard_end", 15, 0xD8  },
    };
    const std::vector<kernel_reg_t> lm_regs = {
        { "reg_guard_bgn", 0, 0x10 },
        { "free_cnt", 1, 0x20 },
        { "up_nb", 2, 0x30 },
        { "dn_nb", 3, 0x40 },
        { "up_last_tick", 4, 0x50 },
        { "dn_last_tick", 5, 0x60 },
        { "history_id", 6, 0x70 },
        { "up_history_tick", 7, 0x78 },
        { "dn_history_tick", 8, 0x88 },
        { "reset_reg", 9, 0x98 },
        { "reg_guard_end", 10, 0xA0 },
    };

    std::cout << "hbmArbiter_regs:" << std::endl;
    for (auto& r : hbmArbiter_regs){
        uint32_t reg_v = hbmArbiter.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }

    std::cout << "mu0_regs:" << std::endl;
    for (auto& r : mu_regs){
        uint32_t reg_v = mu0.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "mu1_regs:" << std::endl;
    for (auto& r : mu_regs){
        uint32_t reg_v = mu1.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }

    std::cout << "lm_mu0_rd0:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu0_rd0.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "lm_mu0_rd1:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu0_rd1.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "lm_mu1_rd0:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu1_rd0.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "lm_mu1_rd1:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu1_rd1.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }

    // get memory bank groups
    xrtMemoryGroup bank_grp_hbm = hbmArbiter.group_id(30); //kernel.xml: hbm.id=30

    // create kernel runner instance
    xrt::run run_mu0 = xrt::run(mu0);
    std::cout << "[MESSAGE] FPGA initialization finished" << std::endl;


    // set kernel arguments for font load mode and clock initialization                         
    run_mu0.set_arg(0, 16);     // wk_nb
    run_mu0.set_arg(1, 0);      // min_addr
    run_mu0.set_arg(2, 16);     // max_addr
    run_mu0.set_arg(3, 0);      // min_data
    run_mu0.set_arg(4, 4);      // gap_nb

    run_mu0.start();
    // run_mu0.wait();
    std::cout << "[MESSAGE] run_mu0.started" << std::endl;      

    sleep(3);

    std::cout << "hbmArbiter_regs:" << std::endl;
    for (auto& r : hbmArbiter_regs){
        uint32_t reg_v = hbmArbiter.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }

    std::cout << "mu0_regs:" << std::endl;
    for (auto& r : mu_regs){
        uint32_t reg_v = mu0.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "mu1_regs:" << std::endl;
    for (auto& r : mu_regs){
        uint32_t reg_v = mu1.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }

    std::cout << "lm_mu0_rd0:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu0_rd0.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "lm_mu0_rd1:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu0_rd1.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "lm_mu1_rd0:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu1_rd0.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
    std::cout << "lm_mu1_rd1:" << std::endl;
    for (auto& r : lm_regs){
        uint32_t reg_v = lm_mu1_rd1.read_register(r.offset);
        std::cout << "  " << r.name << "=0x" << std::hex << reg_v << std::endl;
    }
   std::cout << "[MESSAGE] Program exit normally." << std::endl;
   return EXIT_SUCCESS;
}

