import sys, os, arcpy

def Main(argv=None):
    Input_shp = "C:\Data\Output2.gdb\Murs"
    Cursor = arcpy.UpdateCursor(Input_shp)
    i = 0;
    for Feature in Cursor:
        Midpoint = Feature.shape.positionAlongLine(0.50,True).firstPoint
        Feature.setValue("X", Midpoint.X)
        Feature.setValue("Y", Midpoint.Y)
        print str(i) + ": " + str(Midpoint.X) + " " + str(Midpoint.Y)
        Cursor.updateRow(Feature)
        i += 1

    print "Done."

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Initialize(arcpy.env)
    result = Main()
    # Finalize(result)