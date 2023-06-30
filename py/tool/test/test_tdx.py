from tool.tdx.reader import *

def test_TdxDailyBarReader(tdx_vipdoc):
    tdx_reader = TdxDailyBarReader(tdx_vipdoc)
    try:
        #for row in tdx_reader.parse_data_by_file('/Volumes/more/data/vipdoc/sh/lday/sh600000.day'):
        #    print(row)
        # for row in tdx_reader.get_kline_by_code('110068', 'sh'):
        #     print(row)
        
        '''发现本地的TDX数据中可转债价格精度在20221219以后发生跳变，从*1000变成*10000。'''
        print(tdx_reader.get_df('110068', 'sh'))
        print(tdx_reader.get_preClosePx('110068', 'sh', 20230207))

    except TdxFileNotFoundException as e:
        pass

