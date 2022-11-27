# -*- coding: utf-8 -*-

import traceback
import logging
import datetime
from time import localtime
import os
import behave.test.test_axob as behave
from tool.axsbe_base import INSTRUMENT_TYPE, SecurityIDSource_SZSE

if __name__== '__main__':
    myname = os.path.split(__file__)[1][:-3]
    mytime = str(datetime.datetime(*localtime()[:6])).replace(':',"").replace('-',"").replace(" ","_")

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(f'log/{myname}_{mytime}.log')
    # fh = logging.FileHandler(f'log/{myname}.log', mode='w')
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

    ###测试20220617所有有委托的只股票，全天
    fh.setLevel(logging.WARN)
    sh.setLevel(logging.ERROR)
    logger.info('starting TEST_axob_bat')
    data_source = "H:/AXOB_data_newP/20220623/sbe_20220623_all.log"
    all_inc=[200706, 200613, 200512, 200030, 200553, 200025, 2200, 200530, 200056, 301068, 200550, 300886, 300795, 200570, 200011, 200037, 200541, 200581, 200055, 200029, 2289, 300553, 300837, 200429, 504, 2760, 200505, 300986, 300960, 200771, 300930, 752, 301080, 200413, 2857, 300622, 2319, 300539, 2356, 300103, 300906, 301075, 300557, 2259, 7, 300257, 2890, 300525, 200017, 300371, 300858, 2779, 300417, 301062, 300920, 301042, 300806, 300635, 410, 2575, 300947, 613, 301029, 2656, 300790, 300321, 300824, 2930, 2953, 300069, 300955, 300936, 300489, 2552, 2935, 301049, 2729, 509, 2819, 300203, 2991, 301045, 300758, 2781, 611, 300508, 2872, 300865, 2668, 300596, 2778, 300501, 300549, 300515, 301052, 2199, 300875, 300650, 300564, 2203, 2740, 300971, 2295, 2880, 300953, 301026, 688, 2980, 692, 300805, 301081, 300788, 300416, 301031, 300720, 301053, 300779, 300982, 301182, 301235, 200539, 300345, 2730, 2835, 300753, 300965, 300667, 300864, 300430, 300959, 200761, 300689, 300935, 2653, 300983, 300392, 301128, 2150, 300901, 300948, 2748, 300682, 300632, 2981, 300419, 606, 300902, 300594, 3018, 3027, 301178, 590, 300669, 300915, 2453, 2862, 300174, 2899, 300829, 301076, 1217, 300330, 2577, 2911, 2856, 2976, 2826, 2842, 301106, 2921, 300150, 1209, 300812, 2853, 300566, 300995, 2861, 300856, 300808, 301028, 301032, 2881, 2198, 300469, 300155, 300577, 200869, 300414, 300550, 2940, 45, 300950, 300641, 300286, 2504, 200012, 301097, 502, 2213, 300399, 2501, 2871, 301043, 300703, 2420, 782, 300030, 300861, 200488, 300176, 300851, 1215, 300868, 300480, 3013, 300593, 300575, 409, 2494, 300275, 300826, 2827, 1288, 2231, 301086, 301012, 2970, 2847, 2831, 806, 301162, 300813, 300378, 300854, 300269, 553, 2998, 2014, 2973, 2250, 300290, 300844, 2947, 300963, 300265, 2977, 301185, 300709, 300718, 2360, 300853, 669, 300654, 759, 300713, 2891, 300873, 300729, 48, 300715, 2901, 3003, 2321, 300768, 2795, 1218, 301099, 300797, 300949, 301279, 300268, 755, 2641, 301180, 2338, 300629, 2381, 300919, 300230, 300092, 2318, 2875, 300882, 300815, 2763, 300922, 2959, 301004, 300394, 2825, 300023, 2787, 2801, 300614, 2715, 300778, 300711, 300562, 531, 2535, 2698, 2771, 300900, 2193, 2521, 2768, 2937, 300258, 2264, 300659, 301001, 300291, 2769, 300627, 300106, 2898, 300440, 300696, 300226, 2993, 300455, 300719, 300830, 301117, 300977, 300138, 952, 300270, 2800, 301000, 691, 301024, 300631, 2732, 300407, 300956, 626, 301061, 300461, 3029, 2377, 301213, 301009, 300462, 301023, 2096, 2322, 300221, 2616, 300032, 2820, 301079, 300722, 2777, 300537, 300548, 300487, 561, 2084, 300680, 300349, 2229, 300542, 3019, 2671, 301228, 2811, 300530, 659, 300235, 673, 2790, 300843, 300630, 300765, 2746, 300857, 38, 300975, 300573, 2933, 300605, 300942, 159, 2040, 300640, 300424, 300004, 698, 300587, 300214, 300835, 300951, 2393, 301138, 3001, 300685, 300859, 300425, 300880, 2095, 301102, 2345, 300526, 2430, 301110, 2735, 955, 2398, 2696, 300395, 301070, 695, 2566, 2967, 300567, 300344, 2836, 300289, 2622, 301148, 2688, 300638, 720, 300520, 2815, 300518, 300996, 300533, 300892, 2962, 300388, 300143, 300055, 300828, 300647, 2391, 2114, 300785, 300384, 2484, 2438, 300252, 2741, 2046, 300599, 300684, 300201, 300406, 300903, 881, 301150, 2369, 301131, 300888, 2107, 1205, 3021, 301206, 2695, 2643, 300195, 856, 301071, 3012, 300190, 419, 2679, 2375, 2172, 300506, 300992, 300491, 300755, 911, 2543, 300322, 301050, 869, 2637, 300285, 300962, 2254, 300358, 300342, 300016, 2394, 931, 2416, 2054, 300733, 300743, 300651, 300495, 300018, 300563, 2627, 300802, 300767, 300547, 300866, 301248, 300163, 2571, 2676, 597, 2173, 300242, 300422, 300586, 301201, 300730, 301047, 2404, 300890, 300301, 2290, 2362, 541, 300762, 2743, 300368, 300712, 2358, 300473, 300302, 301072, 300050, 300135, 301137, 300644, 300074, 300429, 300084, 300387, 300127, 2452, 616, 300107, 818, 300555, 2012, 915, 300780, 300273, 2828, 2757, 2287, 2605, 2928, 567, 819, 300998, 301189, 544, 2583, 300005, 429, 300503, 2301, 300054, 2337, 300137, 300231, 2329, 2189, 300493, 300452, 300246, 1289, 2897, 300559, 300167, 2161, 2449, 573, 2077, 2196, 300460, 2378, 300513, 2780, 300323, 2351, 300883, 300220, 850, 300551, 2123, 2401, 300620, 300057, 300973, 2593, 2324, 300066, 300745, 2006, 603, 300494, 300558, 995, 300628, 2303, 2175, 605, 2549, 2878, 300423, 300454, 2149, 1308, 2887, 300288, 300348, 300747, 300022, 300397, 300739, 301229, 300436, 300234, 300097, 2726, 2556, 785, 301092, 300279, 301018, 300427, 300099, 300519, 300375, 5, 301130, 2808, 300626, 2546, 300262, 2022, 300580, 300925, 2705, 301181, 300878, 411, 2547, 2111, 62, 2308, 2462, 300571, 300272, 300666, 300140, 2109, 300707, 2706, 301100, 153, 2440, 2043, 708, 2115, 2905, 2523, 301177, 300894, 300776, 2019, 300439, 526, 2990, 300444, 3011, 2900, 301107, 300636, 300128, 300678, 1267, 300799, 596, 300151, 2296, 300067, 2097, 300360, 300213, 300386, 2017, 2879, 2212, 2190, 2112, 430, 301090, 300927, 2003, 26, 2772, 300161, 300173, 2652, 300657, 300692, 2299, 2089, 2907, 2650, 300598, 2557, 1216, 300466, 300807, 3026, 300006, 301163, 301078, 300615, 2644, 300742, 2957, 300295, 2248, 813, 2723, 300180, 2677, 2987, 2187, 600, 2028, 2464, 301015, 301153, 2773, 523, 2119, 2106, 428, 555, 300945, 301256, 2206, 300209, 300825, 300674, 2701, 300318, 610, 2262, 2496, 300961, 4, 300080, 88, 301088, 415, 2383, 300467, 666, 301060, 2629, 2063, 2140, 501, 2009, 300867, 300012, 2458, 300153, 301190, 2472, 2344, 2689, 2495, 2803, 2520, 2158, 301216, 2488, 300063, 2728, 2461, 823, 2221, 766, 2522, 2171, 2873, 2985, 300053, 2579, 2004, 300165, 2893, 300038, 2563, 609, 2300, 2341, 300991, 2281, 426, 2702, 300091, 301010, 798, 2551, 958, 2020, 2113, 917, 3037, 301183, 838, 2999, 2545, 301211, 300309, 300294, 300576, 300367, 2667, 2609, 2918, 2373, 902, 300541, 2476, 2517, 300928, 11, 300751, 300465, 657, 2005, 2920, 2533, 2859, 300317, 2130, 2085, 300648, 300496, 2035, 300239, 300168, 2640, 300228, 300145, 532, 300177, 300188, 300306, 2298, 2468, 712, 300793, 2177, 301126, 1203, 2446, 2066, 923, 300198, 701, 2408, 300607, 2216, 560, 99, 300085, 300472, 300036, 300415, 655, 300474, 404, 905, 300171, 2558, 2530, 300244, 2274, 300197, 2242, 300552, 2294, 791, 2996, 300047, 300412, 300111, 2707, 300881, 2534, 301222, 300133, 978, 2272, 2353, 2628, 2169, 300379, 300831, 2554, 2244, 639, 300613, 301217, 61, 2258, 300132, 628, 2011, 300148, 2310, 300363, 528, 2448, 301089, 997, 949, 300319, 2122, 300308, 2876, 637, 890, 2201, 548, 300499, 21, 503, 2693, 2498, 975, 733, 2302, 2786, 837, 300471, 300020, 2766, 19, 2542, 300476, 2417, 301236, 2682, 2064, 300676, 996, 615, 2902, 2048, 300253, 848, 2058, 2971, 2343, 990, 301109, 2413, 301020, 2406, 3039, 2568, 300146, 554, 2685, 300748, 2059, 903, 886, 672, 3035, 2223, 423, 2839, 300693, 301083, 581, 2584, 300027, 300428, 300250, 300463, 2396, 918, 300181, 301160, 2038, 2194, 2083, 822, 2075, 950, 2664, 761, 10, 2493, 2051, 2518, 301120, 2068, 300584, 300304, 70, 620, 300895, 676, 2580, 686, 2243, 897, 2646, 301166, 300267, 550, 301187, 300035, 2325, 729, 300568, 2246, 948, 2435, 2081, 2266, 301017, 2076, 2389, 300083, 300316, 836, 300510, 300208, 2100, 728, 570, 2182, 2565, 622, 402, 300087, 592, 2208, 521, 300534, 2108, 826, 2073, 717, 507, 2725, 2824, 300002, 300303, 488, 2205, 300311, 963, 2045, 2945, 690, 2500, 300070, 2263, 300468, 2625, 505, 300061, 2207, 3040, 300401, 727, 300009, 300199, 2443, 300007, 2309, 2463, 2717, 301286, 2181, 300033, 2750, 2139, 300359, 2626, 731, 970, 300284, 2414, 29, 758, 300276, 300073, 2382, 2041, 797, 300737, 301169, 301298, 2532, 300077, 8, 2402, 2436, 300482, 2156, 2457, 2434, 300438, 2439, 2621, 300081, 882, 516, 680, 2759, 2292, 601, 300039, 2456, 2489, 300065, 2539, 2437, 2191, 2674, 959, 300585, 716, 951, 300497, 546, 300037, 795, 300315, 300477, 833, 2601, 2044, 812, 300264, 2727, 2598, 27, 2110, 300158, 3022, 301263, 300131, 300821, 300346, 887, 2821, 750, 300702, 300147, 413, 2152, 300772, 582, 300223, 300008, 2733, 552, 300184, 300456, 540, 2024, 300249, 300136, 2284, 2444, 2126, 2074, 2146, 403, 2478, 968, 300237, 2651, 2197, 2277, 961, 300660, 2355, 629, 300185, 2334, 667, 2600, 300383, 2128, 300122, 300144, 2480, 2386, 2049, 2125, 2936, 300507, 661, 2350, 300458, 2371, 2665, 300393, 825, 2251, 46, 568, 966, 2245, 860, 778, 300999, 300337, 300724, 2421, 300263, 998, 300364, 300102, 2400, 767, 300639, 300182, 633, 2273, 722, 960, 300142, 830, 2613, 2352, 2738, 2256, 2305, 300115, 965, 2155, 2142, 300118, 400, 300088, 2797, 2846, 2531, 300058, 2459, 652, 2227, 2007, 2514, 300433, 893, 2080, 2050, 300459, 815, 831, 909, 2013, 2639, 300343, 2230, 709, 736, 2218, 2047, 937, 2607, 2131, 63, 807, 166, 2202, 2519, 301039, 300479, 2460, 776, 977, 591, 2497, 2129, 671, 2056, 2657, 1319, 300750, 630, 2176, 2340, 2487, 792, 2317, 678, 300274, 723, 627, 2466, 2559, 2235, 2060, 100, 2, 700, 25, 2603, 651, 2527, 17, 1270, 868, 2662, 2380, 2178, 821, 300059, 2703, 2454, 2432, 2241]

    try:
        behave.TEST_mu_bat(data_source, all_inc, batch_nb=16, bgn_batch=0, SecurityIDSource=SecurityIDSource_SZSE, instrument_type=INSTRUMENT_TYPE.STOCK, logPack=logPack) #
    except Exception as e:
        logger.error(f'{traceback.format_exc()}')