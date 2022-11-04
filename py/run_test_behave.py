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

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    formatter_ts = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter_nts = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter_nts)
    ch.setFormatter(formatter_ts)

    logger.addHandler(fh)
    logger.addHandler(ch)

    # logger.info('starting TEST_axob_openCall')
    # behave.TEST_axob_openCall(20220422, 1, 13500)

    # logger.info('starting TEST_axob_openCall')
    # behave.TEST_axob_openCall(20220425, 2594, 13621)

    # logger.info('starting TEST_axob_openCall')
    # behave.TEST_axob_openCall(20220426, 300750, 13621)

    # logger.info('starting TEST_axob_openCall_bat')
    # behave.TEST_axob_openCall_bat("data/20220817/sbe_2022_11_04__11_58_45.txt", [300635], 0)
    
    logger.info('starting TEST_axob_openCall_bat')
    min_inc=[200054, 200045, 200468, 200020, 200706, 200028, 200025, 200152, 200512, 200413, 200553, 200019, 200521, 200581, 200429, 300930, 2930, 200026, 200011, 200029, 200550, 200030, 300492, 200505, 300622, 200992, 2586, 201872, 200037, 200570, 2200, 200530, 200771, 2569, 301035, 200017, 300635, 200596, 301097, 3004, 300426, 300536, 300955, 752, 300442, 2779, 2700, 200726, 2052, 200056, 200058, 2692, 300906, 2836, 300518, 300286, 300645, 300795, 200761, 200055, 2919, 2880, 300374, 300391, 300592, 2819, 301006, 23, 504, 2122, 2319, 695, 300354, 2072, 2499, 2778, 301129, 300911, 300756, 200016, 2787, 301122, 2159, 200541, 200869, 301080, 2735, 301101, 301051, 300656, 300475, 301066, 300938, 300615, 2972, 300953, 300798, 2336, 301235, 300478]
    behave.TEST_axob_openCall_bat("data/20220817/sbe_2022_11_04__11_58_45.txt", min_inc, 0)
    
    # logger.info('starting TEST_axob_openCall_bat')
    # max_inc=[2231, 2709, 2351, 300024, 333, 619, 2600, 2119, 300274, 591, 2506, 2621, 2199, 630, 301269, 899, 2202, 656, 2047, 2514, 709, 3012, 2451, 2369, 2480, 3816, 2337, 728, 2162, 2113, 2460, 2185, 2547, 58, 2405, 2161, 2204, 858, 2346, 2347, 2610, 2129, 2426, 792, 9, 425, 100, 2, 821, 2045, 2475, 2340, 651, 530, 2594, 564, 536, 2685, 868, 2079, 2537, 2241, 2842, 2334, 2329, 2536, 2411, 2308, 2825, 957, 1, 2350, 2375, 2415, 55, 2466, 2689, 2654, 1339, 2553, 2156, 2903, 300059, 2665, 301330, 671, 3035, 2471, 725, 2031, 40, 2077, 625, 2579, 1236, 595, 1258, 629, 2272, 2630]
    # behave.TEST_axob_openCall_bat("data/20220817/sbe_2022_11_04__11_58_45.txt", max_inc, 0)

