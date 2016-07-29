# ----------------------------------------------------------------------------------------------------
# Usage : ImportMdb {source Directory}  {target FeatureClass}
# ----------------------------------------------------------------------------------------------------

import sys, datetime, os, arcpy, shutil, time, fnmatch, stat, fnmatch

# -------------------------------------------------------------------------------------
def HandleException(e):
    arcpy.AddMessage(e);
    print e
    i = 0
    while i < arcpy.GetMessageCount():
        msg = arcpy.GetMessage(i)
        arcpy.AddMessage(msg)
        print msg
        i += 1

# -------------------------------------------------------------------------------------
def CopyData(source, dest):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Copying data from " + source + " to " + dest)
        arcpy.Append_management(source, dest)

        end = datetime.datetime.now()
        arcpy.AddMessage("  Data copied in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 2

# ----------------------------------------------------------------------------------------------------
def Main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 3:
        arcpy.AddMessage("Wrong usage !")
        return 1

    sourceDirectory = argv[1]
    targetFeatureClass = argv[2]

    # Get All MDB files
    mdbFiles = GetMdbFilePaths(sourceDirectory)

    for mdb in mdbFiles :
        arcpy.env.workspace = mdb
        featureClasses = arcpy.ListFeatureClasses()
        datasets = arcpy.ListDatasets("*", "Feature")
        for ds in datasets :
            fullDs = os.path.join(mdb, str(ds))
            arcpy.env.workspace = fullDs
            featureClasses = arcpy.ListFeatureClasses()
            for fc in featureClasses :
                fullFc = os.path.join(fullDs, str(fc))
                desc = arcpy.Describe(fullFc)
                if len(desc.fields) == 53:
                    status = CopyData(fullFc, targetFeatureClass)
                    if status != 0:
                        print "ERROR    : " + fullFc
                        return status
                    else:
                        print "IMPORTED : " + fullFc
                else:
                    print "SKIPPED  : " + fullFc

    # Then we need to remove dupplicates with Dissolve method
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: "Murs"
    # arcpy.Dissolve_management(in_features="Murs",out_feature_class="C:/Data/Output.gdb/Murs_Uniques_Dissolve2",dissolve_field="ID_MUR;R_CANT;TYPE_OUVRAGE;SOUS_TYPE;SOUS_TYPE1;LOCALISATION;ANNEE_CONSTR;NOM;CONF_TYPE;H_MAX;SURF_VISIBLE;TYPE_TIRANT;N_TIRANT;CONF_TIRANTS;DANGER_POSITION;DANGER_TYPE;DANGER_ETAT;DANGER_GLISSEMENTS;PHOTO_1;PHOTO_2;PHOTO_3;PHOTO_4;PHOTO_5;COURONNEMENT;COURONN_TXT;PIED_OUVRAGE;PIED_OUVRA_TXT;SYS_RETENUE;SYS_RETENUE_TXT;CANALISATION;CANALISATI_TXT;INVESTIG_COMPL_TXT;OBSERVATIONS;ID_KUBA;RCANT_LONG;DANGER_HAUTEUR;DANGER_ANCRAGE;KM_MOYEN;HMAX_X_L;NOTE_2;AUTEUR;DATE_RELEVE;DISTANCE_DEBUT;TYPE_PROFIL;DENSITE_PROFIL;EVALUATION_BA;DENSITE_EVAL_BA;EVAL_TIRANTS;EVAL_TIRANTS_L;SYS_SURVEILLANCE;SHAPE_Length",statistics_fields="#",multi_part="MULTI_PART",unsplit_lines="DISSOLVE_LINES")
    
    return 0

def GetMdbFilePaths(directory) :
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.mdb'):
            file = os.path.join(root, filename)
            matches.append(file)
            arcpy.AddMessage(file)
    
    arcpy.AddMessage(str(len(matches)) + " files found")
    return matches

# -------------------------------------------------------------------------------------
def Initialize(env):
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
def Finalize(result):
    arcpy.AddMessage("EXIT STATUS : " + str(result))
    # raw_input()
    sys.stdout.flush()
    sys.exit(result)

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    Initialize(arcpy.env)
    result = Main()
    Finalize(result)
