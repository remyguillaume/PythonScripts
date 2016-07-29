import sys, datetime, os, arcpy, shutil, time, fnmatch, stat

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# DATABASE TOOLS
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
def DeleteStructure(source, objectList):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Deleting existing Data ---")
        # The foreign keys and reference that exists on those objects 
        # must have been deleted with an SQL script before
        for object in objectList:
            obj = os.path.join(source, object)
            if arcpy.Exists(obj):
                arcpy.AddMessage("--> Deleting " + object + "...")
                arcpy.Delete_management(obj)

        end = datetime.datetime.now()
        arcpy.AddMessage("Objects deleted in " + str(end - start) + " ---")
        return 0

    except Exception, e:
        HandleException(e)
        return 100

# -------------------------------------------------------------------------------------
def CopyDataWithStructure(source, dest, objectList):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Copying data with structure ---")
        for object in objectList:
            src = os.path.join(source, object)
            dst = os.path.join(dest, object)
            arcpy.AddMessage("--> Copying " + object + "...")
            arcpy.Copy_management(src, dst)

        end = datetime.datetime.now()
        arcpy.AddMessage("Data with structure copied in " + str(end - start) + " ---")
        return 0

    except Exception, e:
        HandleException(e)
        return 101

# -------------------------------------------------------------------------------------
def CopyData(source, dest, objectList):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Copying data only...")
        for object in objectList:
            src = os.path.join(source, object)
            dst = os.path.join(dest, object)
            arcpy.AddMessage("--> Copying " + object + "...")
            arcpy.Append_management(src, dst)

        end = datetime.datetime.now()
        arcpy.AddMessage("Data copied in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 102

# -------------------------------------------------------------------------------------
def DeleteData(source, objectList):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Deleting data only...")
        for object in objectList:
            src = os.path.join(source, object)
            arcpy.AddMessage("--> Deleting " + object + "...")
            arcpy.DeleteRows_management(src)

        end = datetime.datetime.now()
        arcpy.AddMessage("Data deleted in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 103

# -------------------------------------------------------------------------------------
def AddObjectId(object):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Adding objectId column...")
        arcpy.AddGlobalIDs_management(object)

        end = datetime.datetime.now()
        arcpy.AddMessage("ObjectId column added in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 104

# -------------------------------------------------------------------------------------
def RebuildSpatialIndex(source, objectList):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Rebuilding spatial index...")
        for object in objectList:
            arcpy.AddMessage("--> Rebuilding spatial index for " + object + "...")
            obj = source + '/' + object
            arcpy.AddSpatialIndex_management(obj)

        end = datetime.datetime.now()
        arcpy.AddMessage("Spatial indexes rebuilt in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 105

# -------------------------------------------------------------------------------------
def CreateFileGdb(path):
    try:
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        if not (os.path.exists(dirname)):
             os.mkdir(dirname)

        arcpy.CreateFileGDB_management(dirname, filename)
        return 0

    except Exception, e:
        HandleException(e)
        return 106

# -------------------------------------------------------------------------------------
def DeleteColumn(source, object, columnName):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("--> Deleting column " + columnName + " in " + object + "...")
        src = os.path.join(source, object)
        arcpy.DeleteField_management(src, columnName)

        end = datetime.datetime.now()
        arcpy.AddMessage("Column deleted in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 107

# -------------------------------------------------------------------------------------
def AddColumn(source, object, columnName, columnType, columnLength):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("--> Adding column " + columnName + " in " + object + "...")
        src = os.path.join(source, object)
        arcpy.AddField_management(src, columnName, columnType, "", "", columnLength)

        end = datetime.datetime.now()
        arcpy.AddMessage("Column added in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 108

# -------------------------------------------------------------------------------------
def DeleteAllAttributeIndexes(source, objectList):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Deleting all attribute indexes...")
        for object in objectList:
            src = os.path.join(source, object)
            arcpy.AddMessage("--> Deleting attribute indexes for " + object + "...")
            indexes = arcpy.ListIndexes(src)
            for index in indexes:
                if (index.fields[0].type == "OID"):
                    arcpy.AddMessage("    --> Skipping ObjectId index " + index.name)
                elif (index.fields[0].type == "Geometry"):
                    arcpy.AddMessage("    --> Skipping Geometry index " + index.name)
                else:
                    arcpy.AddMessage("    --> Deleting index " + index.name + "...")
                    arcpy.RemoveIndex_management(src, index.name)

        end = datetime.datetime.now()
        arcpy.AddMessage("All attribute indexes deleted in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 109
    
# -------------------------------------------------------------------------------------
def CopyDataWithFilter(source, dest, filter):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Copying " + source + " to " + dest + " [" + filter + "]...")
        arcpy.Select_analysis(source, dest, filter)

        end = datetime.datetime.now()
        arcpy.AddMessage("Data copied in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 110

# -------------------------------------------------------------------------------------
def ComputeIntersect(source1, source2, dest):
    try:
        start = datetime.datetime.now()
        arcpy.AddMessage("Computing Intersect between " + source1 + " and " + source2 + "...")

        arcpy.Intersect_analysis([source1, source2], dest , "ALL", "", "LINE")

        end = datetime.datetime.now()
        arcpy.AddMessage("Intersect computed in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 111

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# DIRECTORIES/FILES TOOLS
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
def Backup(path):
    try:
        if (os.path.exists(path)):
            dirname = os.path.dirname(path)
            filename = os.path.basename(path)
            dt = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            savePath = os.path.join(dirname, "Olds", str(dt), filename)
            shutil.move(path, savePath)
            # We have to wait for a while, otherwise the directory is not 
            # complete deleted while we attempt to recreate it
            time.sleep(1) 

        return 0

    except Exception, e:
        HandleException(e)
        return 200

# -------------------------------------------------------------------------------------
def DeleteDirectory(path):
    try:
        if (os.path.exists(path)):
            shutil.rmtree(path)
            # We have to wait for a while, otherwise the directory is not 
            # complete deleted while we attempt to recreate it
            time.sleep(1) 
        
        return 0

    except Exception, e:
        HandleException(e)
        return 201

# -------------------------------------------------------------------------------------
def CreateDirectory(path):
    try:
        if not (os.path.exists(path)):
            os.mkdir(path)

        return 0

    except Exception, e:
        HandleException(e)
        return 202

# -------------------------------------------------------------------------------------
def CopyFiles(source, target, pattern="*", makeWritable=False):
    try:
        for file in os.listdir(source):
            if (fnmatch.fnmatch(file, pattern)):
                sourceFullFileName = os.path.join(source, file)
                shutil.copy2(sourceFullFileName, target)
                if (makeWritable):
                    # Make them writable
                    os.chmod(os.path.join(target, file), stat.S_IWRITE)

        return 0

    except Exception, e:
        HandleException(e)
        return 203

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# ANALYSIS TOOLS
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
def SpatialJoin(targetFeatures, joinFeatures, outputFeatures, operation):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Executing spatial join ---")
        # This crashes when called outside of ArcMap.
        # Don't know why yet.
        # This part has to be done manually for the moment
        '''
        arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outputFeatures, "JOIN_ONE_TO_MANY", "KEEP_COMMON", fieldMapping, operation)
                                   match_option="WITHIN",
                                   search_radius="#",
                                   distance_field_name="#")
        arcpy.SpatialJoin_analysis(
            target_features="C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV",
            join_features="C:/Temp/tempS3.gdb/S3_BUFWEG_MLV",
            out_feature_class="C:/Temp/tempS3.gdb/S3_MISSWEG_MLV2",
            join_operation="JOIN_ONE_TO_MANY",
            join_type="KEEP_COMMON",
            field_mapping="""TLM_ID "TLM_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_ID,-1,-1;TLM_SRC_ID "TLM_SRC_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_SRC_ID,-1,-1;TLM_OBJEKTART_ID "TLM_OBJEKTART_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_OBJEKTART_ID,-1,-1;TLM_VERKBESCHR_ID "TLM_VERKBESCHR_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_VERKBESCHR_ID,-1,-1;TLM_KUNSTBAUTE_ID "TLM_KUNSTBAUTE_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_KUNSTBAUTE_ID,-1,-1;TLM_KEISEL_ID "TLM_KEISEL_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_KEISEL_ID,-1,-1;TLM_ISUBERBRUC_BL "TLM_ISUBERBRUC_BL" true true false 2 Short 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_ISUBERBRUC_BL,-1,-1;TLM_CREATEUSER_VL "TLM_CREATEUSER_VL" true true false 50 Text 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_CREATEUSER_VL,-1,-1;TLM_CHANGE_DT "TLM_CHANGE_DT" true true false 8 Date 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_CHANGE_DT,-1,-1;TLM_CHANGEUSER_VL "TLM_CHANGEUSER_VL" true true false 50 Text 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_CHANGEUSER_VL,-1,-1;TLM_BELAGSART_ID "TLM_BELAGSART_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_BELAGSART_ID,-1,-1;TLM_UBERBRUC_ID "TLM_UBERBRUC_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_UBERBRUC_ID,-1,-1;TLM_ISDELETED_BL "TLM_ISDELETED_BL" true true false 2 Short 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_ISDELETED_BL,-1,-1;TLM_WEGUSE_CD "TLM_WEGUSE_CD" true true false 2 Short 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_WEGUSE_CD,-1,-1;TLM_CREATE_DT "TLM_CREATE_DT" true true false 8 Date 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_CREATE_DT,-1,-1;TLM_STUFE_ID "TLM_STUFE_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_STUFE_ID,-1,-1;TLM_NODE1_ID "TLM_NODE1_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_NODE1_ID,-1,-1;TLM_NODE2_ID "TLM_NODE2_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_NODE2_ID,-1,-1;TLM_ISOBSOLETE_BL "TLM_ISOBSOLETE_BL" true false false 2 Short 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,TLM_ISOBSOLETE_BL,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,C:/Temp/tempS3.gdb/TlmData/WGD_TLMSEGMENT_MLV,SHAPE_Length,-1,-1;SEG_ID "WEG_ID" true false false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_ID,-1,-1;SEG_TLM_ID "WEG_TLM_ID" true false false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_TLM_ID,-1,-1;SEG_LVART_CD "WEG_LVART_CD" true false false 2 Short 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_LVART_CD,-1,-1;SEG_ZUSTAND_ID "WEG_ZUSTAND_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_ZUSTAND_ID,-1,-1;SEG_ZUSTERL_TX "WEG_ZUSTERL_TX" true true false 255 Text 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_ZUSTERL_TX,-1,-1;SEG_FUEHRART_ID "WEG_FUEHRART_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_FUEHRART_ID,-1,-1;SEG_REALSTAND_ID "WEG_REALSTAND_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_REALSTAND_ID,-1,-1;SEG_WNDART_ID "WEG_WNDART_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_WNDART_ID,-1,-1;SEG_FAGOBFQUAL_TX "WEG_FAGOBFQUAL_TX" true true false 255 Text 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_FAGOBFQUAL_TX,-1,-1;SEG_ISDELETED_BL "WEG_ISDELETED_BL" true false false 2 Short 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_ISDELETED_BL,-1,-1;SEG_ISSGLTRAIL_BL "WEG_ISSGLTRAIL_BL" true false false 2 Short 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_ISSGLTRAIL_BL,-1,-1;SEG_CREATE_DT "WEG_CREATE_DT" true false false 8 Date 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_CREATE_DT,-1,-1;SEG_CREATEUSER_VL "WEG_CREATEUSER_VL" true false false 32 Text 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_CREATEUSER_VL,-1,-1;SEG_CHANGE_DT "WEG_CHANGE_DT" true false false 8 Date 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_CHANGE_DT,-1,-1;SEG_CHANGEUSER_VL "WEG_CHANGEUSER_VL" true false false 32 Text 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_CHANGEUSER_VL,-1,-1;SEG_EIGVERB_ID "SEG_EIGVERB_ID" true true false 38 Guid 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_EIGVERB_ID,-1,-1;SEG_EIGVERBERL_TX "SEG_EIGVERBERL_TX" true true false 255 Text 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SEG_EIGVERBERL_TX,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,C:/Temp/tempS3.gdb/S3_BUFWEG_MLV,SHAPE_Area,-1,-1""",
            match_option="WITHIN",
            search_radius="#",
            distance_field_name="#")
        '''
        end = datetime.datetime.now()
        arcpy.AddMessage("Spatial join executed in " + str(end - start) + " ---")
        return 0

    except Exception, e:
        HandleException(e)
        return 500

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# MXD TOOLS
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
def ChangeDataSource(sourceFile, sourceDbName, targetDataSource, targetDbName):
    try:
        start = datetime.datetime.now()

        arcpy.AddMessage("Changing DataSource of " + os.path.basename(sourceFile) + " to " + targetDbName + "...")

        mxd = arcpy.mapping.MapDocument(sourceFile)
        for dataframe in arcpy.mapping.ListDataFrames(mxd):
            for lyr in arcpy.mapping.ListLayers(mxd, "", dataframe):
                if lyr.supports("DATASOURCE") and lyr.supports("datasetName"):
                    arcpy.AddMessage("--> Processing layer " + str(lyr.name.encode('ascii','ignore')) + "...")
                    newDsName = str(lyr.datasetName).replace(sourceDbName, targetDbName)
                    lyr.replaceDataSource(targetDataSource, "SDE_WORKSPACE", newDsName, False)

        arcpy.RefreshTOC()
        arcpy.RefreshActiveView()
        mxd.save()
        del mxd

        end = datetime.datetime.now()
        arcpy.AddMessage("DataSource changed in " + str(end - start))
        return 0

    except Exception, e:
        HandleException(e)
        return 300

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# ADMIN TOOLS
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
def DisconnectUsers(sdeGdb, userNames):
    try:
        connectedUsers = arcpy.ListUsers(sdeGdb)
        for user in connectedUsers:
            if user.Name in userNames:
                arcpy.AddMessage("--> Disconnecting " + user.Name)
                arcpy.DisconnectUser(sdeGdb, user.ID)

        return 0

    except Exception, e:
        HandleException(e)
        return 400

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# GENERAL TOOLS
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
def HandleException(e):
    arcpy.AddMessage(e);
    i = 0
    while i < arcpy.GetMessageCount():
        arcpy.AddMessage(arcpy.GetMessage(i))
        i += 1

# -------------------------------------------------------------------------------------
def Finalize(result):
    arcpy.AddMessage("EXIT STATUS : " + str(result))
    # raw_input()
    sys.stdout.flush()
    sys.exit(result)
