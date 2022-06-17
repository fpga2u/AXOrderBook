import pandas as pd

#backup oly

ls = [# not public
    "./data/pegga_day0_p0.pcapng.stats.log", 
    "./data/pegga_day1_p0.pcapng.stats.log",
    "./data/pegga_day2_p0.pcapng.stats.log",
]

ds = [pd.read_csv(x, sep=";", dtype={'securityID':str}) for x in ls]
ds = [x[((x.securityID<"004000")|((x.securityID>="300000")&(x.securityID<"399000"))) & (x.orderLmt!=0) & (x.high!=0) & (x.exec!=0)] for x in ds]
ds = pd.concat(ds)
ds['orderSum']=ds.orderLmt + ds.orderMkt + ds.orderSd
#ds['orderR'] = ds.orderSum - ds.exec - ds.cancel
ds.high = ds.high // 10000
ds = ds.groupby('securityID').mean()

print(ds.shape)
print(ds.describe())
print(ds.orderSum.sum(), ds.exec.sum(), ds.cancel.sum())
print(ds[ds.orderSum>40000].shape, ds[ds.orderSum>40000].orderSum.sum())
print(ds[ds.orderSum>100000].shape, ds[ds.orderSum>100000].orderSum.sum())
print(ds[ds.orderSum==368050])
print(pd.DataFrame(ds.loc['300750']).T) #ugly
