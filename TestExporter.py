import arcpy
import os
from datetime import datetime

mxd = arcpy.mapping.MapDocument(r"E:\Siful\tem\1.EA_A3_v002_RU_10.6_2nd_20210818.mxd")

user_folder = os.getcwd()

div_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DivCode")[0]
div_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DivCCName")[0]

dis_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZilaCode")[0]
dcc_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "DCCNam")[0]

city_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCCode")[0]
city_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "CCNam")[0]

up_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "UpCode")[0]
up_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "UpNam")[0]

mun_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "MunCode")[0]
mun_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "MunNam")[0]

un_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "UnCode")[0]
un_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "UnNam")[0]

mou_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "MauCode")[0]
mou_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "MauNam")[0]

vill_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VillCode")[0]
vill_name_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "VillNam")[0]

zone_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "ZonCode")[0]
sup_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "SUPCode")[0]
ea_code_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "EAcomCode")[0]
total_hh_title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Total_HH_EA")[0]

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

        print "="*85

        print "Exporting Oid: " + str(row[22])
        now = datetime.now()
        print "Starting time: " + now.strftime("%H:%M:%S")
        
        div_code_title.text = str(row[0])
        div_name_title.text = str(row[1])

        dis_code_title.text = str(row[2])
        dcc_name_title.text = str(row[3])

        city_code_title.text = str(row[4])
        city_name_title.text = str(row[5])

        up_code_title.text = str(row[6])
        up_name_title.text = str(row[7])

        mun_code_title.text = str(row[8])
        mun_name_title.text = str(row[9])

        un_code_title.text = str(row[10])
        un_name_title.text = str(row[11])

        mou_code_title.text = str(row[12])
        mou_name_title.text = str(row[13])

        vill_code_title.text = str(row[14])
        vill_name_title.text = str(row[15])

        zone_code_title.text = str(row[16])
        sup_code_title.text = str(row[17])
        ea_code_title.text = str(row[18])
        total_hh_title.text = str(row[19])

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
