# -*- coding: utf-8 -*-

import logging
import datetime
from time import localtime
import os
import behave.test.test_axob as behave

if __name__== '__main__':
    myname = os.path.split(__file__)[1][:-3]
    mytime = str(datetime.datetime(*localtime()[:6])).replace(':',"").replace('-',"").replace(" ","_")

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    # fh = logging.FileHandler(f'log/{myname}_{mytime}.log')
    fh = logging.FileHandler(f'log/{myname}.log', mode='w')
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)

    formatter_ts = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter_nts = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter_nts)
    sh.setFormatter(formatter_ts)

    logger.addHandler(fh)
    logger.addHandler(sh)
    logPack = logger.debug, logger.info, logger.warn, logger.error
    
    # 上交所：股票（暂时不研究，等逐笔合并流出来再说）
    # logger.info('starting sse 600519')
    # behave.TEST_axob(20230207, 600519, instrument_type=behave.INSTRUMENT_TYPE.STOCK, SecurityIDSource=behave.SecurityIDSource_SSE)

    # 上交所：债券
    logger.info('starting sse 110068')
    behave.TEST_axob(20230207, 110068, instrument_type=behave.INSTRUMENT_TYPE.BOND, SecurityIDSource=behave.SecurityIDSource_SSE)

    ### 20220617测试错误
    # logger.info('starting TEST_axob_bat')
    # data_source = "data/20220617/bat_test2.log"
    # ptn=[301129]
    # behave.TEST_axob_bat(data_source, ptn, n_max=0, openCall_only=False, logPack=logPack) #

    
    # ### 20220608测试错误
    # logger.info('starting TEST_axob_bat')
    # fh.setLevel(logging.WARN)
    # sh.setLevel(logging.ERROR)
    # data_source = "data/20220608/bat_test1.log"
    # ptn=[300833, 301023, 300971, 300862, 300993, 300800, 300727, 300935, 300880, 300167, 300520, 300513, 300722, 300429, 301087, 300295, 301207, 300420, 301151, 300326, 300485, 300358, 300232, 300359, 300304, 300390, 2932]
    # # ptn=[2932]  # 不同channel的逐笔间存在时差，一个channel进入盘后竞价了，导致另一个channel的TPM切换但还没有收到自己的最后一个连续竞价逐笔消息。
    # behave.TEST_axob_bat(data_source, ptn, n_max=0, openCall_only=False)
    # # behave.TEST_mu_rolling(data_source, ptn, n_max=0, rolling_gap=1, begin_section='mu_1_145602870')

    # ### 20220608测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220608, 200613) #TODO: 退市B股，进入退市整理期首日，多次临停但快照TPM无变化
                                         #http://www.szse.cn/disclosure/notice/temp/t20220608_593688.html
    #临停规则
    #http://www.szse.cn/www/lawrules/index/rule/P020210105571755659081.pdf
    #http://investor.szse.cn/application/search/index.html?keyword=%E7%9B%98%E4%B8%AD%E4%B8%B4%E6%97%B6&r=1670290891297
    #http://investor.szse.cn/knowledge/stock/deal/t20210203_584642.html
    #http://investor.szse.cn/knowledge/stock/deal/t20210203_584643.html
    #http://investor.szse.cn/knowledge/bond/other/t20220622_594109.html
    #http://investor.szse.cn/knowledge/bond/other/t20220810_595304.html
    #http://investor.szse.cn/knowledge/bond/other/t20220810_595306.html
    
    # ### 20220609测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220609, 301160) #收盘集合竞价时无价格档在笼子外
    
    # ### 20220609测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220609, 2801) # 市价单后紧跟本方最优，导致本方最优取的价格不对
    
    # ### 20220610测试错误
    # logger.info('starting TEST_axob_bat')
    # data_source = "data/20220610/bat_test1.log"
    # ptn=[1, 300089]
    # behave.TEST_axob_bat(data_source, ptn, n_max=0, openCall_only=False) #000001闭市后，300089来了两个快照导致误设了ClosePx

    # ### 20220620测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220620, 301286)

    # ### 20220620测试错误
    # logger.info('starting TEST_axob_bat')
    # fh.setLevel(logging.WARN)
    # sh.setLevel(logging.ERROR)
    # behave.TEST_axob(20220620, 301238) #创业板新股次日，无涨跌停时，买单价格超过昨收28倍，需要被丢弃
    
    # ### 20220622测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220622, 300103)

    # ### 20220623测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220623, 300928) #买方价格笼子外订单连续进入撮合直到涨停，导致买方本方最优价过期却被用作买方参考价。

    # ## 20220701测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220701, 1309)    #TODO: 新股上市首日，涨停价44%，但集合竞价进行申报的价格有效区间是[80%, 120%]，连续竞价时才是[64%, 144%]
                                          #http://www.szse.cn/disclosure/notice/temp/t20220701_594505.html
    
    # ### 20220804测试错误
    # logger.info('starting TEST_axob_bat')
    # fh.setLevel(logging.WARN)
    # sh.setLevel(logging.ERROR)
    # behave.TEST_axob(20220804, 301278) #创业板新股首日，波动性中断期间撤单导致价格笼子变化
    #                                    #http://www.szse.cn/disclosure/notice/temp/t20220804_595243.html
    #                                    #http://www.szse.cn/disclosure/notice/temp/t20220804_595244.html
    # # data_source = "data/20220804/AX_sbe_szse_301278.log"
    # # behave.TEST_mu_rolling(data_source, [301278], n_max=0, rolling_gap=30, begin_section='mu_1_111033000')

    # ## 20220805测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220805, 1236)      #TODO: 新股上市首日，涨停价44%，但集合竞价进行申报的价格有效区间是[80%, 120%]，连续竞价时才是[64%, 144%]
                                            #http://www.szse.cn/disclosure/notice/temp/t20220805_595261.html

    # ## 20220808测试错误
    # logger.info('starting TEST_axob_bat')
    # behave.TEST_axob(20220808, 1229)    #TODO: 新股上市首日，涨停价44%，但集合竞价进行申报的价格有效区间是[80%, 120%]，连续竞价时才是[64%, 144%]
                                          #http://www.szse.cn/disclosure/notice/temp/t20220808_595282.html

    # ### 20220812测试
    # logger.info('starting TEST_axob_bat')
    # fh.setLevel(logging.WARN)
    # sh.setLevel(logging.ERROR)
    # behave.TEST_axob(20220812, 301336, logPack=logPack) #创业板新股首日，波动性中断测试
    #                                                     #http://www.szse.cn/disclosure/notice/temp/t20220812_595343.html
    #                                                     #http://www.szse.cn/disclosure/notice/temp/t20220812_595344.html
    
    # ### 20220812测试
    # logger.info('starting TEST_axob_bat')
    # fh.setLevel(logging.WARN)
    # sh.setLevel(logging.ERROR)
    # behave.TEST_axob(20220812, 301192) #价格溢出

    # ### 20221010测试错误
    # logger.info('starting TEST_axob_bat')
    # fh.setLevel(logging.WARN)
    # sh.setLevel(logging.ERROR)
    # behave.TEST_axob(20221010, 301313) #创业板新股次日

    #########
    # logger.info('starting TEST_axob_SL')
    # behave.TEST_axob_SL(20220422, 1)
    
    # logger.info('starting TEST_mu_SL')
    # data_source = "data/20221010/sbe_20221010_all.log"
    # # min_inc=[200054, 200512, 200030, 200045, 200553, 200011, 200020, 200530, 200025, 300996, 200028, 200152, 301059, 200706, 200550, 200037, 200521, 200505, 200056, 300354, 300930, 301066, 300980, 200029, 200055, 300508, 200019, 200026, 300668, 2569, 200992, 200017, 200761, 300870, 2485, 2870, 200570, 301072, 200581, 200413, 300733, 300069, 300654, 201872, 300916, 200771, 2857, 972, 200541, 200058, 2972, 301099, 300530, 301004, 504, 300757, 2735, 300645, 2692, 300948, 200016, 2200, 300885, 2058, 200468, 300833, 300622, 301239, 200726, 300876, 301106, 2975, 200429, 301057, 300550, 300897, 300791, 300521, 2779, 300892, 300964, 301097, 300489, 300984, 300523, 300971, 300426, 300779, 300515, 301020, 301049, 300816, 300958, 300982, 300715, 300986, 2724, 301012, 301182, 300417]
    # min_inc=[300668, 300996, 301059, 1]
    # behave.TEST_mu_SL(data_source, min_inc) #
