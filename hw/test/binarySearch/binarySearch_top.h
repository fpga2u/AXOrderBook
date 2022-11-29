#ifndef __BINARYSEARCH_TOP_H__
#define __BINARYSEARCH_TOP_H__

extern "C"
void binarySearch_top(
    /* register-to-host */
    unsigned int& w_ram_en,
    unsigned int& w_ram_idx,
    unsigned int& w_ram_dataH,  //[71:64]
    unsigned int& w_ram_dataM,  //[63:32]
    unsigned int& w_ram_dataL,  //[31:0]
    unsigned int& target_dataM,  //[47:32]
    unsigned int& target_dataL,  //[31:0]
    unsigned int& target_index
);

#endif
