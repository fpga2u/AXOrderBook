#include "binarySearch_top.h"
#include "binarySearch.h"


void binarySearch_top(
    /* register-to-host */
    unsigned int& w_ram_en,
    unsigned int& w_ram_idx,
    unsigned int& w_ram_dataH,  //[71:64]
    unsigned int& w_ram_dataM,  //[63:32]
    unsigned int& w_ram_dataL,  //[31:0]
    unsigned int& target_dataM,  //[47:32]
    unsigned int& target_dataL,  //[31:0]
    unsigned int& target_index,
    unsigned int& access_nb
)
{
/* register-to-host */
#pragma HLS INTERFACE s_axilite bundle=control port=w_ram_en
#pragma HLS INTERFACE s_axilite bundle=control port=w_ram_idx
#pragma HLS INTERFACE s_axilite bundle=control port=w_ram_dataH
#pragma HLS INTERFACE s_axilite bundle=control port=w_ram_dataM
#pragma HLS INTERFACE s_axilite bundle=control port=w_ram_dataL
#pragma HLS INTERFACE s_axilite bundle=control port=target_dataM
#pragma HLS INTERFACE s_axilite bundle=control port=target_dataL
#pragma HLS INTERFACE s_axilite bundle=control port=target_index

/* proto */
#pragma HLS INTERFACE ap_ctrl_chain port=return
#pragma HLS INTERFACE s_axilite port=return bundle=control


#pragma HLS dataflow

    binarySearchApp(
        w_ram_en,
        w_ram_idx,
        w_ram_dataH,
        w_ram_dataM,
        w_ram_dataL,
        target_dataM,
        target_dataL,
        target_index,
        access_nb
    );


}

