#ifndef __BINARYSEARCH_H__
#define __BINARYSEARCH_H__

#include "ap_axi_sdata.h"
#include "hls_stream.h"

#define DATA_TOTAL_SIZE 72
#define DATA_VALID_SIZE 48
#define RAM_DEPTH 2048
#define RAM_DEPTH_LOG 11  //2^11=2048

//ramSzie需等于2的n次方，同时logSize需等于n;
//ram数据中的前m比特用于匹配数据;
//当数据为全1时是表示无效数据;
//若成功找到，返回index=[0~ramSize-1]；否则返回-1.
template<unsigned int ramSize, unsigned int logSize, int dataTotalBitSize, int dataValidBitSize>
class binarySearchCore
{
public:
    void mainRun(
        unsigned int& access_nb,
        ap_uint<dataTotalBitSize>* ordered_data, 
        ap_uint<dataValidBitSize> d, 
        ap_int<logSize+1>& index
    )
    {
        ap_int<logSize+1> left = 0;
        ap_int<logSize+1> right = ramSize - 1;
        ap_int<logSize+1> location = -1;
        ap_int<logSize+1> middle;
        unsigned int j;

        for (j = 0; j < logSize + 1; j++)
        {
#pragma HLS UNROLL
            middle = (left + right) / 2;
            ap_uint<dataValidBitSize> m_d = ordered_data[middle].range(dataValidBitSize-1, 0);
            if (d < m_d || m_d==ap_uint<dataValidBitSize>(-1))
            {
                right = middle - 1;
            }
            else if (d > m_d)
            {
                left = middle + 1;
            }
            else
            {
                location = middle;
#ifndef __SYNTHESIS__
                printf("j=%d\n", j);
#endif
                break;
            }
            if (left > right)
                location = -1;
        }
        index = location;
        access_nb = j;
    }

};


typedef ap_uint<DATA_TOTAL_SIZE> ram_data_t;
typedef ap_uint<DATA_VALID_SIZE> ram_target_t;
typedef ap_int<RAM_DEPTH_LOG+1> ram_index_t; //0~2047 为有效值, -1为无效值

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
);


#endif
