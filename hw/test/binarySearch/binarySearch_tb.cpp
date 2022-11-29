#include "binarySearch_top.h"
#include <iostream>
#include <assert.h>


int main()
{
    unsigned int w_ram_en = 0;
    unsigned int w_ram_idx = 0;
    unsigned int w_ram_dataH = 0;
    unsigned int w_ram_dataM = 0;
    unsigned int w_ram_dataL = 0;
    unsigned int target_dataM = 0;
    unsigned int target_dataL = 0;
    unsigned int target_index = 0;

    //未写入数据前，测试应该都是-1
    std::cout << "Testing first searching..." << std::endl;
    w_ram_en = 0;
    for (int i=0; i<10; ++i){
        target_dataM = i*2;
        target_dataL = i;
        binarySearch_top(
            w_ram_en,
            w_ram_idx,
            w_ram_dataH,
            w_ram_dataM,
            w_ram_dataL,
            target_dataM,
            target_dataL,
            target_index
        );
        std::cout << i << " over. target_index=" << target_index << std::endl;
        assert(target_index==-1);
    }

    //初始化数据
    std::cout << "Writing data..." << std::endl;
    w_ram_en = 1;
    for (int i=0; i<2048/2; ++i){ //写必须从0开始，数据要从小到大
        w_ram_idx = i;
        w_ram_dataL = i*i+13;
        w_ram_dataM = i;
        w_ram_dataH = i-1;
        binarySearch_top(
            w_ram_en,
            w_ram_idx,
            w_ram_dataH,
            w_ram_dataM,
            w_ram_dataL,
            target_dataM,
            target_dataL,
            target_index
        );
    }

    //执行搜索
    std::cout << "Testing second searching..." << std::endl;
    w_ram_en = 0;
    for (int i=0; i<2048; i+=1){
        target_dataL = i*i+13;
        target_dataM = i;
        binarySearch_top(
            w_ram_en,
            w_ram_idx,
            w_ram_dataH,
            w_ram_dataM,
            w_ram_dataL,
            target_dataM,
            target_dataL,
            target_index
        );
        std::cout << i << " over. target_index=" << target_index << std::endl;
        if (i<1024){
            assert(target_index==i);
        }else{
            assert(target_index==-1);
        }
    }


    return 0;
}