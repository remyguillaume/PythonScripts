# ----------------------------------------------------------------------------------------------------
# Usage : DeleteFeatureClasses {source db}
# ----------------------------------------------------------------------------------------------------

import sys, datetime, os, arcpy
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

    source = argv[1]

    objects = ["TMP_COUNTRY_TLM_MLV", "TMP_COUNTRYBUF_TLM_MLV", "TMP_CANTON_TLM_MLV", "TMP_CANTONBUF_TLM_MLV", "TMP_GEMEINDE_TLM_MLV"]
    status = framework.DeleteStructure(source, objects)
    return status

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main()
    framework.Finalize(result)
