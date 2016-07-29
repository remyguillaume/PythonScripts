import sys, os, arcpy

def Main(argv=None):
    Input_shp = "C:\Data\Output2.gdb\Shapes2"
    i = 0;
    with arcpy.da.UpdateCursor(Input_shp, ['SHAPE@XY']) as Cursor:
        for row in Cursor:
            Cursor.updateRow([[row[0][0] + 10019820, row[0][1]]])
            print str(i)
            i += 1

    print "Done."

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Initialize(arcpy.env)
    result = Main()
    # Finalize(result)