#defining map document object and dataframe object
mxd = arcpy.mapping.MapDocument("current")
df = mxd.activeDataFrame

#listing taget layer object
layer = arcpy.mapping.ListLayers(mxd, "EA_Boundary", df)[0]

#appending all the sa_geo_code to a pre defined list
l = []
with arcpy.da.SearchCursor(layer,"sa_geo_code") as cur:
    for i in cur:
        l+= i

#listing unique sa_geo_code
s = set(l)
s2 = list(s)

#calculating total ea number for each sa without reprint maps
for i in s2:
    layer.definitionQuery = "sa_geo_code=" + "'"+i+"'"+"AND re_print IS NULL"
    with arcpy.da.UpdateCursor(layer,["enumerator_geo_code","total_ea","total_khana","t_khana"]) as cur2:
        result = []
        t_khana = []
        t_khana_int = map(int, t_khana)
        for row in cur2:
            result.append(str(row[0]))
            t_khana.append(str(row[2]))

        cur2.reset()

        for i in cur2:
            i[1]=str(len(result)).zfill(2)
            i[3]= sum(t_khana_int)
            cur2.updateRow(i)
            
