# ----------------------------------------------------------------------------------------------------
# Usage : RebuildSpatialIndexes {target db}
# ----------------------------------------------------------------------------------------------------

import sys, datetime, os, arcpy
frk = os.path.join(os.getcwd(), '..\\Common')
sys.path.insert(0, frk)
frk = os.path.join(os.getcwd(), '..\\..\\Common')
sys.path.insert(0, frk)
import license, framework

# ----------------------------------------------------------------------------------------------------
def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        arcpy.AddMessage("Wrong usage !")
        return 1

    license.Initialize(arcpy.env)

    objects = ["ADD_GEBIET_MLV", "WGD_TLMNODES_MLV", "TlmData/WGD_TLMSEGMENT_MLV", "RTD_PSTANDORT_MLV", "RTD_VERLAUF_MLV"]
    status = framework.RebuildSpatialIndex(argv[1], objects)

    return status

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main()
    framework.Finalize(result)
