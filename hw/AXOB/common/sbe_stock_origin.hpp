#ifndef __SBE_STOCK_ORIGIN_H__
#define __SBE_STOCK_ORIGIN_H__

/*
#ifdef __cplusplus
extern "C"
{
#endif
*/

#include "ap_axi_sdata.h"

/*
#ifdef WIN32
#define PACKED
#pragma pack(push,1)
#else
#define PACKED __attribute__ ((__packed__))
#endif
*/


typedef
struct price_level_t
{
    ap_int<32>    Price;  //price
    ap_int<64>    Qty;    //qty
}price_level_t;

typedef
struct QtyQueue_level_t   //not imple for now
{
    ap_uint<8>  NoOrders;  //nb of QtyQueue
    ap_uint<16> QtyQueue[50];
}QtyQueue_level_t;




/*
#ifdef WIN32
#pragma pack(pop)
#undef PACKED
#else
#undef PACKED
#endif
*/


/*
#ifdef __cplusplus
}
#endif
*/
#endif /*__SBE_STOCK_ORIGIN_H__*/
