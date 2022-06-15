
import tool.test.test_msg as msg
# import active.test.test_OB as active_OB

if __name__== '__main__':
    msg.TEST_msg_byte_stream()
    msg.TEST_msg_SL()

    # ##    
    msg.TEST_msg_ms()

    # ##
    msg.TEST_serial(10000)

    # active_OB.TEST_OB()