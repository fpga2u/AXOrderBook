/**
 * c-sim 消息打印
 */

#ifndef __SBE_DBG_INFO_HPP__
#define __SBE_DBG_INFO_HPP__


#ifndef __SYNTHESIS__
#  include <stdio.h>
#  include <iostream>

#  define OUTPUT_PORT stdout
#  define DEBUG_OUTPUT fprintf
/**printf like debug log**/
#  define slog(...)                                 \
	do                                              \
	{                                               \
        DEBUG_OUTPUT(OUTPUT_PORT, __VA_ARGS__);     \
	} while (0)

/**std::cout like INFO log**/
#  define INFO(str)                                 \
    do                                              \
    {                                               \
        std::cout << "INFO - " << str << std::endl; \
    } while( false )

/**std::cout like WARNING log**/
#  define WARN(str)                                     \
    do                                                  \
    {                                                   \
        std::cout << "WARNING - " << str << std::endl;  \
    } while( false )

/**std::cout like ERROR log**/
#  define ERR(str)                                      \
    do                                                  \
    {                                                   \
        std::cerr << "ERROR - " << str << std::endl;    \
    } while( false )

#else   //__SYNTHESIS__

#  define DONOTHING() /* Just do nothing */
#  define slog(...) DONOTHING() //do nothing
#  define INFO(str) DONOTHING() //do nothing
#  define WARN(str) DONOTHING() //do nothing
#  define ERR(str)  DONOTHING() //do nothing

#endif


#endif //__SBE_DBG_INFO_HPP__

