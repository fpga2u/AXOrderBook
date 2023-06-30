from tool.tdx.reader import *

def test_TdxDailyBarReader(tdx_vipdoc):
    tdx_reader = TdxDailyBarReader(tdx_vipdoc)
    try:
        #for row in tdx_reader.parse_data_by_file('/Volumes/more/data/vipdoc/sh/lday/sh600000.day'):
        #    print(row)
        for row in tdx_reader.get_kline_by_code('000001', 'sz'):
            print(row)
        print(tdx_reader.get_df('000001', 'sz'))
    except TdxFileNotFoundException as e:
        pass

