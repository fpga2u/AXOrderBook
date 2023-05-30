/**
 * c-sim 调试工具
 */

#ifndef __SBE_DBG_UTIL_HPP__
#define __SBE_DBG_UTIL_HPP__

#include "ap_axi_sdata.h"

inline
void setSecurityID(ap_int<8> SecurityID[9], const char * code)
{
    assert(strlen(code)<=8);

    int i=0;
    for (;i<strlen(code); ++i){
        SecurityID[i] = code[i];
    }
    for (;i<9;++i){
        SecurityID[i] = '\0';
    }
}


#endif // __SBE_DBG_UTIL_HPP__
