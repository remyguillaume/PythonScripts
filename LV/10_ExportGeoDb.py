# ----------------------------------------------------------------------------------------------------
# Usage : Export {source db}  {target db}
# ----------------------------------------------------------------------------------------------------

import sys, datetime, os, arcpy
frk = os.path.join(os.getcwd(), '..\\Common')
sys.path.insert(0, frk)
import license, framework

# ----------------------------------------------------------------------------------------------------
def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        arcpy.AddMessage("Wrong usage !")
        return 1

    license.Initialize(arcpy.env)

    # Create new FileGDB
    status = framework.CreateFileGdb(argv[2])
    if status != 0:
        return status

    # Export Data to new Fgdb
    objects = ["ADD_DATAOWNER_MLV",
               "ADD_MANDANT_MLV",
               "CTD_CATALOG_MLV",
               "CTD_CATITEM_MLV",
               "ADD_GEBIET_MLV",
               "ADD_SWISSNAME_MLV",
               "ADR_MDT_GBT_MLV",
               "RTD_LSTANDORT_MLV",
               "WGD_TLMNODES_MLV",
               "TlmData",
               "WGR_TLM_GBT_MLV",
               "WGD_WEG_MLV",
               "WGD_BVRK_MLV",
               "RTD_PSTANDORT_MLV",
               "ADD_PHOTO_MLV",
               "ADD_DOCUMENT_MLV",
               "RTR_LST_MDT_MLV",
               "RTD_ROUTENFELD_MLV",
               "RTD_VERLAUF_MLV",
               "RTD_ROUTE_MLV",
               "RTD_RTEVERSION_MLV",
               "RTR_RVE_MDT_MLV",
               "RTR_PST_RTE_MLV",
               "RTD_RTEBSFTG_MLV",
               "RTD_RTEBGEINTG_MLV",
               "RTD_RTENODE_MLV",
               "RTD_RTESEGMENT_MLV",
               "RTD_ETAPPE_MLV",
               "PZD_CHANGESET_MLV",
               "PZD_PENDENZ_MLV",
               "PZD_RECIPIENT_MLV",
               "JOB_JOB_MLV",
               "EXP_WEG_MLV",
               "EXP_RSL_MLV",
               "EXP_ROUTE_MLV",
               "EXP_PSTANDORT_MLV",
               "EXP_METADATA_MLV",
               "EXP_LSTANDORT_MLV",
               "EXP_EXPORTINFO_MLV",
               "EXP_ETAPPE_MLV",
               "WGD_GISTOOLBOX_MLV"]
    status = framework.CopyDataWithStructure(argv[1], argv[2], objects)
    if status != 0:
        return status

    # Delete all indexes
    objects = ["ADD_DATAOWNER_MLV",
               "ADD_MANDANT_MLV",
               "CTD_CATALOG_MLV",
               "CTD_CATITEM_MLV",
               "ADD_GEBIET_MLV",
               "ADD_SWISSNAME_MLV",
               "ADR_MDT_GBT_MLV",
               "RTD_LSTANDORT_MLV",
               "WGD_TLMNODES_MLV",
               "WGR_TLM_GBT_MLV",
               "WGD_WEG_MLV",
               "WGD_BVRK_MLV",
               "RTD_PSTANDORT_MLV",
               "ADD_PHOTO_MLV",
               "ADD_DOCUMENT_MLV",
               "RTR_LST_MDT_MLV",
               "RTD_ROUTENFELD_MLV",
               "RTD_VERLAUF_MLV",
               "RTD_ROUTE_MLV",
               "RTD_RTEVERSION_MLV",
               "RTR_RVE_MDT_MLV",
               "RTR_PST_RTE_MLV",
               "RTD_RTEBSFTG_MLV",
               "RTD_RTEBGEINTG_MLV",
               "RTD_RTENODE_MLV",
               "RTD_RTESEGMENT_MLV",
               "RTD_ETAPPE_MLV",
               "PZD_CHANGESET_MLV",
               "PZD_PENDENZ_MLV",
               "PZD_RECIPIENT_MLV",
               "JOB_JOB_MLV",
               "EXP_WEG_MLV",
               "EXP_RSL_MLV",
               "EXP_ROUTE_MLV",
               "EXP_PSTANDORT_MLV",
               "EXP_METADATA_MLV",
               "EXP_LSTANDORT_MLV",
               "EXP_EXPORTINFO_MLV",
               "EXP_ETAPPE_MLV",
               "TlmData/WGD_TLMSEGMENT_MLV"]
    status = framework.DeleteAllAttributeIndexes(argv[2], objects)
    if status != 0:
        return status

    # Delete unused tables
    objects = ["ADD_DATAOWNER_MLV",
               "ADD_MANDANT_MLV",
               "CTD_CATALOG_MLV",
               "CTD_CATITEM_MLV",
               "JOB_JOB_MLV",
               "EXP_METADATA_MLV",
               "EXP_EXPORTINFO_MLV"]
    status = framework.DeleteStructure(argv[2], objects)
    if status != 0:
        return status

    # Clear Export and log table content
    objects = ["EXP_WEG_MLV",
               "EXP_RSL_MLV",
               "EXP_ROUTE_MLV",
               "EXP_PSTANDORT_MLV",
               "EXP_LSTANDORT_MLV",
               "EXP_ETAPPE_MLV"]
    status = framework.DeleteData(argv[2], objects)
    if status != 0:
        return status

    return status

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main()
    framework.Finalize(result)
