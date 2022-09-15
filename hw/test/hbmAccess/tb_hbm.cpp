#include "kernel.h"
#include <iostream>

extern "C"
void vadd(
        const ap_uint<512> in1[HBM_ENTRIES], // Read-Only Vector 1
        const ap_uint<512> in2[HBM_ENTRIES], // Read-Only Vector 2
        ap_uint<512> out[HBM_ENTRIES],      // Output Result for ADD
        const unsigned int dsize,        // Size in integer
        const unsigned int kernel_loop,  // Running the same kernel operations kernel_loop times
        bool addRandom                   // Address Pattern is random
        );
        
int main()
{
    long unsigned int total_access_bytes = 64 * 16; //总共访问byte数，一个地址是512b即64Byte，这个值太大将导致cosim耗时太久
    long unsigned int total_int_size = total_access_bytes/sizeof(int) ; // Convert to number of integer words
    unsigned int kernel_loop = 1;

    bool addRandom = false;

    const unsigned int vsize = total_int_size / VDATA_SIZE;


    ap_uint<512> buffer_in1[HBM_ENTRIES];
    ap_uint<512> buffer_in2[HBM_ENTRIES];
    ap_uint<512> buffer_output[HBM_ENTRIES];

    for (int i=0; i<vsize; ++i){
        for (int j=0; j<VDATA_SIZE; ++j){
            buffer_in1[i].range(j*32+31, j*32) = i;
            buffer_in2[i].range(j*32+31, j*32) = j;
        }
    }

    vadd(
        buffer_in1,               // Read-Only Vector 1
        buffer_in2,               // Read-Only Vector 2
        buffer_output,                     // Output Result for ADD
        total_int_size,       // Size in integer
        kernel_loop,  // Running the same kernel operations kernel_loop times
        addRandom                 // Address Pattern is random
        );

    for (int i=0; i<vsize; ++i){
        for (int j=0; j<VDATA_SIZE; ++j){
            if (buffer_output[i].range(j*32+31, j*32) != (i + j)){
                std::cout << "i=" << i << " j=" << j << " error=" << buffer_output[i].range(j*32+31, j*32) << std::endl;
                return -1;
            }
        }
    }


    std::cout << "TEST OK!" << std::endl;

    return 0;
}
