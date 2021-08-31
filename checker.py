import os

luid = []
with arcpy.da.SearchCursor("EA_Boundary","enumerator_geo_code") as cur:
    for i in cur:
        luid += i

luid2 = map (str, luid)

f_path =r'D:\BBS002\Export_Maps\EA_Maps\10_Barishal\RU\09_Bhola'

f_list =  []
for root,dirs,files in os.walk(f_path):
    for f in files:
        t=f.split('.')[0]
        f_list.append(t)


for i in luid2:
    if i not in f_list:
        print 'miss_'+i

