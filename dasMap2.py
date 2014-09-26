import time
import datetime
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

def dasMap():
  try:
    print ' - converting census poly to raster'
    arcpy.PolygonToRaster_conversion(censusPoly, popField, 'censusGrid', 'MAXIMUM_AREA','#',landCoverGrid)

    print ' - reclassifying land cover to weights'
    nlcdRcls = arcpy.gp.ReclassByASCIIFile_sa(landCoverGrid, reclassTable, 'nlcdRcls', 'NODATA')

    print ' - removing exclusions from land cover'
    nlcdExcl = arcpy.gp.Times_sa('nlcdRcls', exclusions, 'nlcdExcl')

    print ' - calculating sum of weights in census blocks'
    wghtsSum = arcpy.gp.ZonalStatistics_sa(censusPoly, censusID, 'nlcdExcl', 'wghtsSum', 'SUM', 'DATA')

    print ' - dividing land cover weights to get proportion per block'
    wghtsDivide = arcpy.gp.Divide_sa('nlcdExcl', 'wghtsSum', 'wghtsDivide')

    print ' - multiply population grid by proportion wghts to get count per pixel'
    popGrid = arcpy.gp.Times_sa('censusGrid', 'wghtsDivide', 'popGrid')
  except:
    print arcpy.GetMessages(2)


# inputs ----------------
censusPoly = 'Q:/arcdata/states/ia/ForDanMajka/PopDensity_Dasymetric.gdb/CensusBlockGroup4County_01mrge'
censusID = 'BLOCKID10'
popField = 'POP10'
landCoverGrid = 'Q:/arcdata/states/ia/ForDanMajka/PopDensity_Dasymetric.gdb/NLCD_2011_01exp'
reclassTable = 'Q:/arcdata/states/ia/ForDanMajka/nlcd_reclass_das_dmowska.txt' # Reclass wghts from Dmowska et al.
exclusions = 'Q:/arcdata/states/ia/ForDanMajka/PopDensity_Dasymetric.gdb/roads_0_1'
outputDir = 'Q:/arcdata/states/ia/ForDanMajka/dasOutput3.gdb'

# environment settings
env.workspace = outputDir
arcpy.env.snapRaster = landCoverGrid
arcpy.env.cellsize = landCoverGrid


# call functions ----------
dasMap()
print '--- DONE! ---'
