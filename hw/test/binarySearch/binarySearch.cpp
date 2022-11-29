#include "binarySearch.h"

//在72bit x 2048数据中查找；每地址的前48bit为目标值；在w_ram_en为1期间写ram数据、为0期间搜索ram。
void binarySearchApp(
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

    static bool init = false;
    static ram_data_t ram[RAM_DEPTH];
    if (!init){
        for (int i=0; i<RAM_DEPTH; ++i){
            ram[i] = ram_data_t(-1);
        }
        init = true;
    }
    
    binarySearchCore<RAM_DEPTH, RAM_DEPTH_LOG, DATA_TOTAL_SIZE, DATA_VALID_SIZE> bsc;

    if (w_ram_en){
        ram_data_t wdat;
#if DATA_TOTAL_SIZE<=32
        wdat.range(DATA_TOTAL_SIZE-1, 0) = w_ram_dataL;
#else
        wdat.range(31, 0) = w_ram_dataL;
#if DATA_TOTAL_SIZE<=64
        wdat.range(DATA_TOTAL_SIZE-1, 32) = w_ram_dataM;
#else
        wdat.range(63, 32) = w_ram_dataM;
        wdat.range(DATA_TOTAL_SIZE-1, 64) = w_ram_dataH;
#endif
#endif
        ram[w_ram_idx] = wdat;
        access_nb = 0;
        target_index = -1;  //如果没有这句，cosim会锁死
    } else {
        ram_target_t tgt;
#if DATA_VALID_SIZE<=32
        tgt.range(DATA_VALID_SIZE-1, 0) = target_dataL;
#else
        tgt.range(31, 0) = target_dataL;
#if DATA_VALID_SIZE<=64
        tgt.range(DATA_VALID_SIZE-1, 32) = target_dataM;
#else
        tgt.range(63, 32) = target_dataM;
        // tgt.range(DATA_VALID_SIZE, 64) = w_ram_dataH;
#endif
#endif

        ram_index_t index;
        bsc.mainRun(access_nb, ram, tgt, index);
        target_index = index;
    }
}
