# ----------------------------------------------------------------------------------------------------
# Usage : GenerateSegmentsGebietRelations {source db} {dest db}
# ----------------------------------------------------------------------------------------------------

import sys, datetime, os, arcpy
frk = os.path.join(os.getcwd(), '..\\..\\Common')
sys.path.insert(0, frk)
import license, framework

# Global variables
gebietTable = ""
countryTable = ""
countryBufferTable = ""
cantonTable = ""
cantonBufferTable = ""
gemeindeTable = ""
segmentTable = ""
tlmCountryTable = ""
tlmCountryBufferTable = ""
tlmCantonTable = ""
tlmCantonBufferTable = ""
tlmGemeindeTable = ""

# ----------------------------------------------------------------------------------------------------
def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        arcpy.AddMessage("Wrong usage !")
        return 1

    license.Initialize(arcpy.env)

    source = argv[1]
    dest = argv[2]

    initialize(source, dest)

    # Create new FileGDB
    status = framework.CreateFileGdb(dest)
    if status != 0:
        return status

    # Copy data locally (for better performance)
    status = copyDataFromSourceToDest(source, dest)
    if status != 0:
        return status

    # Generate Sub-FeatureClasses for Gebiets
    status = prepareGebiets()
    if status != 0:
        return status

    # Calculate intersections
    status = generateTlmGebietRelations()
    if status != 0:
        return status

    # Copy calculated data to source
    status = copyCalculatedDataToSource(source, dest)
    if status != 0:
        return status

    return status

# ----------------------------------------------------------------------------------------------------
def initialize(source, dest):
    global gebietTable
    global countryTable
    global countryBufferTable
    global cantonTable
    global cantonBufferTable
    global gemeindeTable
    global segmentTable
    global tlmCountryTable
    global tlmCountryBufferTable
    global tlmCantonTable
    global tlmCantonBufferTable
    global tlmGemeindeTable
    global tlmCountrySourceTable
    global tlmCountryBufferSourceTable
    global tlmCantonSourceTable
    global tlmCantonBufferSourceTable
    global tlmGemeindeSourceTable

    gebietTable = dest + "/ADD_GEBIET_MLV"
    segmentTable = dest + "/TlmData/WGD_TLMSEGMENT_MLV"

    countryTable = dest + "/TMP_COUNTRY_MLV"
    countryBufferTable = dest + "/TMP_COUNTRYBUF_MLV"
    cantonTable = dest + "/TMP_CANTON_MLV"
    cantonBufferTable = dest + "/TMP_CANTONBUF_MLV"
    gemeindeTable = dest + "/TMP_GEMEINDE_MLV"

    tlmCountryTable = dest + "/TMP_COUNTRY_TLM_MLV"
    tlmCountryBufferTable = dest + "/TMP_COUNTRYBUF_TLM_MLV"
    tlmCantonTable = dest + "/TMP_CANTON_TLM_MLV"
    tlmCantonBufferTable = dest + "/TMP_CANTONBUF_TLM_MLV"
    tlmGemeindeTable = dest + "/TMP_GEMEINDE_TLM_MLV"

# ----------------------------------------------------------------------------------------------------
def copyDataFromSourceToDest(source, dest):

    objects = ["TlmData", "ADD_GEBIET_MLV"]
    status = framework.CopyDataWithStructure(source, dest, objects)
    if status != 0:
        return status

    return status

# ----------------------------------------------------------------------------------------------------
def prepareGebiets():
    
    # Country
    status = framework.CopyDataWithFilter(gebietTable, countryTable, "GBT_TYPE_CD = 1 AND GBT_BUFSIZE_VL = 0")
    if status != 0:
        return status

    # CountryBuffer
    status = framework.CopyDataWithFilter(gebietTable, countryBufferTable, "GBT_TYPE_CD = 1 AND GBT_BUFSIZE_VL = 5")
    if status != 0:
        return status

    # Canton
    status = framework.CopyDataWithFilter(gebietTable, cantonTable, "GBT_TYPE_CD = 2 AND GBT_BUFSIZE_VL = 0")
    if status != 0:
        return status

    # CantonBuffer
    status = framework.CopyDataWithFilter(gebietTable, cantonBufferTable, "GBT_TYPE_CD = 2 AND GBT_BUFSIZE_VL = 5")
    if status != 0:
        return status

    # Gemeinde
    status = framework.CopyDataWithFilter(gebietTable, gemeindeTable, "GBT_TYPE_CD > 2")
    if status != 0:
        return status

    return status

# ----------------------------------------------------------------------------------------------------
def generateTlmGebietRelations():
    
    # Country
    status = framework.ComputeIntersect(countryTable, segmentTable, tlmCountryTable)
    if status != 0:
        return status

    # CountryBuffer
    status = framework.ComputeIntersect(countryBufferTable, segmentTable, tlmCountryBufferTable)
    if status != 0:
        return status

    # Canton
    status = framework.ComputeIntersect(cantonTable, segmentTable, tlmCantonTable)
    if status != 0:
        return status

    # CantonBuffer
    status = framework.ComputeIntersect(cantonBufferTable, segmentTable, tlmCantonBufferTable)
    if status != 0:
        return status

    # Gemeinde
    status = framework.ComputeIntersect(gemeindeTable, segmentTable, tlmGemeindeTable)
    if status != 0:
        return status

    return status

# ----------------------------------------------------------------------------------------------------
def copyCalculatedDataToSource(source, dest):

    objects = ["TMP_COUNTRY_TLM_MLV", "TMP_COUNTRYBUF_TLM_MLV", "TMP_CANTON_TLM_MLV", "TMP_CANTONBUF_TLM_MLV", "TMP_GEMEINDE_TLM_MLV"]
    status = framework.CopyDataWithStructure(dest, source, objects)
    if status != 0:
        return status

    return status

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main()
    framework.Finalize(result)
