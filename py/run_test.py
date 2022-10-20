# -*- coding: utf-8 -*-

import tool.test.test_msg as msg
import tool.test.test_pipeline as pp
# import active.test.test_OB as active_OB

if __name__== '__main__':
    # msg.TEST_msg_byte_stream()
    # msg.TEST_msg_SL()

    ##
    # msg.TEST_msg_ms(35000)

    ##
    # msg.TEST_serial(10000)

    # active_OB.TEST_OB()

    # ## 185s
    # msg.TEST_msg_ms_filt("data/sbe_0817a.txt", "000001", 0, 35000)

    # ##
    # msg.TEST_msg_text("data/lv1szdump20220818.cap.ITsbe.txt", "000997", 0, 35000)

    pp.test_pipeline_I1E1()
