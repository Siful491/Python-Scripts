import arcpy
import os

mxd = arcpy.mapping.MapDocument(r'E:\Siful\tem\1.EA_A3_v002_RU_10.6_2nd_20210818.mxd')
out_path = r'E:\Siful\tem\New folder'

for page in range(1, mxd.dataDrivenPages.pageCount + 1):
    mxd.dataDrivenPages.currentPageID = page
    df = mxd.activeDataFrame
    df_in = arcpy.mapping.ListDataFrames(mxd, "INDEX_01")[0]
    layer = arcpy.mapping.ListLayers(mxd, "Shaded", df)[0]
    
    layer_in_hi = arcpy.mapping.ListLayers(mxd, "Highlighted_Index", df_in)[0]
    layer_in_su = arcpy.mapping.ListLayers(mxd, "SUP_EA_Boundary", df_in)[0]
    layer_in_ea = arcpy.mapping.ListLayers(mxd, "EA_Boundary_1", df_in)[0]
    
    div_name = mxd.dataDrivenPages.pageRow.division_code + '_' + mxd.dataDrivenPages.pageRow.division_name
    dis_name = mxd.dataDrivenPages.pageRow.district_code + '_' + mxd.dataDrivenPages.pageRow.district_name
    up_name = mxd.dataDrivenPages.pageRow.upazila_thana_code + '_' + mxd.dataDrivenPages.pageRow.upazila_thana_name
    zone_name = mxd.dataDrivenPages.pageRow.zone_no + '_' + mxd.dataDrivenPages.pageRow.upazila_thana_name
    file_name = mxd.dataDrivenPages.pageRow.enumerator_geo_code
    sa_geo = mxd.dataDrivenPages.pageRow.sa_geo_code

    out_folder = os.path.join(out_path, div_name, dis_name, up_name, zone_name)
    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)
    layer.definitionQuery = "enumerator_geo_code<>" "'" +file_name+ "'"
    
    layer_in_hi.definitionQuery = "sa_geo_code=" "'" +sa_geo+ "'"
    layer_in_su.definitionQuery = "sa_geo_code=" "'" +sa_geo+ "'"
    layer_in_ea.definitionQuery = "enumerator_geo_code=" "'" +file_name+ "'"
    ext = layer_in_su.getExtent()
    df_in.extent=ext
    
    arcpy.env.overwriteOutput = True
    arcpy.mapping.ExportToJPEG(mxd, out_folder + "\\" + file_name+ '.jpg', resolution = 300)
    print file_name



del mxd   
