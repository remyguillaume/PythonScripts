# ----------------------------------------------------------------------------------------------------
# Usage : ImportDataFromGeoDb {source db}  {target db} {Include segments ?}
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

    if len(argv) < 3:
        arcpy.AddMessage("Wrong usage !")
        return 1

    importTlm = True;
    if len(argv) == 4 and argv[3] == 'FALSE':
        importTlm = False;

    license.Initialize(arcpy.env)

    if importTlm:
        objects = ["WGR_TLM_GBT_MLV", "WGD_WEG_MLV", "WGD_BVRK_MLV", "RTD_ROUTE_MLV", "RTD_ROUTENFELD_MLV", "RTD_RTEVERSION_MLV", "RTD_LSTANDORT_MLV", "RTR_LST_MDT_MLV", "RTD_RTEBSFTG_MLV", "RTD_RTENODE_MLV", "RTD_RTESEGMENT_MLV", "RTD_RTEBGEINTG_MLV", "RTR_PST_RTE_MLV", "RTR_RVE_MDT_MLV", "RTD_ETAPPE_MLV", "PZD_CHANGESET_MLV", "PZD_PENDENZ_MLV", "PZD_RECIPIENT_MLV", "ADD_DOCUMENT_MLV", "ADD_PHOTO_MLV"]
    else:
        objects = ["RTD_VERLAUF_MLV", "RTD_PSTANDORT_MLV", "WGD_WEG_MLV", "WGD_BVRK_MLV", "RTD_ROUTE_MLV", "RTD_ROUTENFELD_MLV", "RTD_RTEVERSION_MLV", "RTD_LSTANDORT_MLV", "RTR_LST_MDT_MLV", "RTD_RTEBSFTG_MLV", "RTD_RTENODE_MLV", "RTD_RTESEGMENT_MLV", "RTD_RTEBGEINTG_MLV", "RTR_PST_RTE_MLV", "RTR_RVE_MDT_MLV", "RTD_ETAPPE_MLV", "PZD_CHANGESET_MLV", "PZD_PENDENZ_MLV", "PZD_RECIPIENT_MLV", "ADD_DOCUMENT_MLV", "ADD_PHOTO_MLV"]

    # framework.DeleteData(argv[2], objects) ==> does not work with tables, which are not referenced as GeoDB object
    status = framework.CopyData(argv[1], argv[2], objects)

    return status

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main()
    framework.Finalize(result)
