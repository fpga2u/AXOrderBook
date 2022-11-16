# -*- coding: utf-8 -*-

from tool.axsbe_base import INSTRUMENT_TYPE
import tool.test.test_msg as msg
import tool.test.test_pipeline as pp
import tool.msg_util as msg_util

if __name__== '__main__':
    # msg.TEST_msg_byte_stream()
    # msg.TEST_msg_SL()

    # #
    # msg.TEST_msg_ms(35000)

    # #
    # msg.TEST_serial(10000)

    # # active_OB.TEST_OB()

    # ## 185s
    # msg.TEST_msg_ms_filt("data/20220817/sbe_0817a.txt", "000001", 0, 35000)

    # ##
    # msg.TEST_msg_text("data/20220818/lv1szdump20220818.cap.ITsbe.txt", "000997", 0, 35000)

    ####
    # pp.test_pipeline_I1E1()

    # pp.test_pipeline_id()

    # # 198.0328 sec
    # msg.TEST_print_securityID("data/20220812/sbe_20220812_all.log", read_nb=0, instrument_type=INSTRUMENT_TYPE.STOCK)

    # msg.TEST_ApplSeqNum("data/20220812/sbe_20220812_all.log", 0)
    msg_util.extract_security("data/20220812/sbe_20220812_all.log", "data/20220812/AX_sbe_szse_301336.log", [301336])

