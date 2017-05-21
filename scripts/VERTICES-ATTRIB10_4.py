#-------------------------------------------------------------------------------
# Name:		Polyline Vertices To Txt
# Author:	Alicja Byzdra
# Institution:	UMGDY
# Created:	24-04-2017
#-------------------------------------------------------------------------------

import arcpy
from arcpy import env
import numpy as np

try:

    featureClass = arcpy.GetParameterAsText(0)
    folder = arcpy.GetParameterAsText(1)
    txtFileName = arcpy.GetParameterAsText(2)

    txtFile = open(folder + "\\" + txtFileName + ".txt","w")

    field_names = [f.name for f in arcpy.ListFields(featureClass)]
    if "OBJECTID" in field_names:
        field_names.remove("OBJECTID")
    if "SHAPE" in field_names:
        field_names.remove("SHAPE")
    field_names_str = ""
    for i in field_names:
        field_names_str += i + "\t"

    txtFile.write("ID\tVertex_ID\tX\tY\tZ\t"+field_names_str+"\n")

    attributes = ["OBJECTID","SHAPE@"] + field_names

    vert=0
    with arcpy.da.SearchCursor(featureClass,attributes) as cursor:
        for row in cursor:
            rowCount = [row[atr] for atr in range(len(attributes)) if atr>1]
            rows_str = ""
            for i in rowCount:
                rows_str += str(i) + "\t"
            i=1
            for part in row[1]:
                for pnt in part:
                    xx=pnt.X
                    yy=pnt.Y
                    zz=pnt.Z
                    txtFile.write(str(row[0])+"\t"+str(i)+"\t"+str(xx)+"\t"+str(yy)+"\t"+str(zz)+"\t"+rows_str+"\n")
                    i+=1
                    vert+=1
            #txtFile.write("--------------------------------------------\nID:"+str(row[0])+"\nNumber of vertices:"+str(row[1].pointCount)+"\n--------------------------------------------\n")
    del row
    del cursor

    txtFile.write("\n--------------------------------------------\n"+"Total number of vertices:"+str(vert)+"\n--------------------------------------------\n")

    txtFile.close()

    arcpy.AddMessage("Done")

except:
    arcpy.AddError("Error occurred")
    arcpy.AddMessage(arcpy.GetMessages())