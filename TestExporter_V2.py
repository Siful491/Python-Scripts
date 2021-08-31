import arcpy
import os
from datetime import datetime

mxd = arcpy.mapping.MapDocument(r"E:\Siful\tem\1.EA_A3_v002_RU_10.6_2nd_20210818.mxd")

user_folder = os.getcwd()

element_objects = []

for elm in  arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
    if elm.name:
        element_objects.append(elm)
        

fileds = ['division_code', 'division_name', 'district_code', 'district_name', 'city_code', 'city_name', 'upazila_thana_code',
          'upazila_thana_name', 'municipality_code', 'municipality_name', 'union_ward_code','union_ward_name','mauza_code',
          'mauza_name','village_code','village_name','zone_no','sa_code','ea_code','total_khana','enumerator_geo_code','sa_geo_code','OBJECTID']

df_layer = arcpy.mapping.ListDataFrames(mxd,'Layers')[0]
df_index = arcpy.mapping.ListDataFrames(mxd,'INDEX_01')[0]

highlight = arcpy.mapping.ListLayers(mxd, 'Highlighted', df_layer)[0]
shaded = arcpy.mapping.ListLayers(mxd, 'Shaded', df_layer)[0]
Highlighted_Index = arcpy.mapping.ListLayers(mxd, 'Highlighted_Index', df_index)[0]
SUP_EA_Boundary = arcpy.mapping.ListLayers(mxd, 'SUP_EA_Boundary', df_index)[0]
EA_Boundary_1 = arcpy.mapping.ListLayers(mxd, 'EA_Boundary_1', df_index)[0]

with arcpy.da.SearchCursor(highlight, fileds) as cur:
    
    for row in cur:

        print "="*80

        print "Exporting Oid: " + str(row[22])
        now = datetime.now()
        print "Starting time: " + now.strftime("%H:%M:%S")

        for element in element_objects:

            if element.name == "DivCode":
                element.text = str(row[0])
            elif element.name == "DivCCName":
                element.text = str(row[1])
                
            elif element.name == "ZilaCode":
                element.text = str(row[2])
            elif element.name == "DCCNam":
                element.text = str(row[3])

            elif element.name == "CCCode":
                element.text = str(row[4])
            elif element.name == "CCNam":
                element.text = str(row[5])

            elif element.name == "UpCode":
                element.text = str(row[6])
            elif element.name == "UpNam":
                element.text = str(row[7])

            elif element.name == "MunCode":
                element.text = str(row[8])
            elif element.name == "MunNam":
                element.text = str(row[9])

            elif element.name == "UnCode":
                element.text = str(row[10])
            elif element.name == "UnNam":
                element.text = str(row[11])

            elif element.name == "MauCode":
                element.text = str(row[12])
            elif element.name == "MauCode":
                element.text = str(row[13])

            elif element.name == "VillCode":
                element.text = str(row[14])
            elif element.name == "VillNam":
                element.text = str(row[15])

            elif element.name == "ZonCode":
                element.text = str(row[16])
            elif element.name == "SUPCode":
                element.text = str(row[17])
            elif element.name == "EAcomCode":
                element.text = str(row[18])
            elif element.name == "Total_HH_EA":
                element.text = str(row[19])

        out_folder = user_folder + '\\' + row[0] + '_' + row[1] + '\\' + row[2] + '_' + row[3] + '\\' + row[6] + '_' + row[7] + '\\' + row[16] + '_' + row[7]

        if os.path.exists(out_folder) == False:
            os.makedirs(out_folder)


        highlight.definitionQuery = "enumerator_geo_code=" + "'" + row[20] + "'"
        shaded.definitionQuery = "enumerator_geo_code<>" + "'" + row[20] + "'"
        Highlighted_Index.definitionQuery = "sa_geo_code=" + "'" + row[21] + "'"
        SUP_EA_Boundary.definitionQuery = "sa_geo_code=" + "'" + row[21] + "'"
        EA_Boundary_1.definitionQuery = "enumerator_geo_code=" + "'" + row[20] + "'"

        df_layer_ext = highlight.getExtent()
        df_layer.extent = df_layer_ext
        df_layer.scale = df_layer.scale * 1.1

        df_index_ext = Highlighted_Index.getExtent()
        df_index.extent = df_index_ext
        df_index.scale = df_index.scale * 1.1

        out_file = out_folder + "\\" + str(row[20]) + ".jpg"

        arcpy.env.overwriteOutput = True
        arcpy.mapping.ExportToJPEG(mxd, out_file, resolution = 300)

        print "Done: " + out_file
        e_now = datetime.now()
        print "Ending time: " + e_now.strftime("%H:%M:%S")


del mxd
del cur 
