import string, sys
import arcpy

ARCGISLICENSES = ["arcview", "arceditor", "arcinfo"]

def ArcView():
    try:
        __Product("ArcView")
    except:
        try:
            __Product("ArcEditor")
        except:
            try:
                __Product("ArcInfo")
            except:
                pass
    __Check("ArcView")

def ArcEditor():
    try:
        __Product("ArcEditor")
    except:
        try:
            __Product("ArcInfo")
        except:
            pass
    __Check("ArcEditor")

def ArcInfo():
    try:
        __Product("ArcInfo")
    except:
        pass
    __Check("ArcInfo")

def __Product(productcode):
    arcpy.setProduct(productcode)

def __Check(productcode):
    try:
        import arcpy
        active = string.lower(arcpy.ProductInfo())
        wanted = string.lower(productcode)
        if ARCGISLICENSES.index(active) >= ARCGISLICENSES.index(wanted):
            arcpy.AddMessage("Lizenz: " + arcpy.ProductInfo())
            return True
        arcpy.AddMessage("Aktuelle Lizenz: " + arcpy.ProductInfo())
        arcpy.AddMessage("Erforderliche Lizenz: " + productcode)
        sys.exit()
    except:
        pass
    print "Erforderliche Lizenz: " + productcode
    sys.exit()


# -------------------------------------------------------------------------------------
def SetEnvironment(env):
    arcpy.env.outputCoordinateSystem = "PROJCS['CH1903_LV03',GEOGCS['GCS_CH1903',DATUM['D_CH1903',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Hotine_Oblique_Mercator_Azimuth_Center'],PARAMETER['False_Easting',600000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Azimuth',90.0],PARAMETER['Longitude_Of_Center',7.439583333333333],PARAMETER['Latitude_Of_Center',46.95240555555556],UNIT['Meter',1.0]]"

    arcpy.env.XYResolution = "0.001 Meters"
    arcpy.env.MResolution = "0.001"
    arcpy.env.ZResolution = "0.001 Meters"
    arcpy.env.XYTolerance = "0.002 Meters"
    arcpy.env.MTolerance = "0.002"
    arcpy.env.ZTolerance = "0.002 Meters"

    arcpy.env.randomGenerator = "0 ACM599"
    arcpy.env.outputZFlag = "Same As Input"
    arcpy.env.outputMFlag = "Same As Input"
    outputZValue = ""
    qualifiedFieldNames = "true"
    extent = "DEFAULT"
    geographicTransformations = ""

# -------------------------------------------------------------------------------------
def Initialize(env):
    ArcEditor()
    SetEnvironment(env)
    arcpy.CheckOutExtension("Network")
