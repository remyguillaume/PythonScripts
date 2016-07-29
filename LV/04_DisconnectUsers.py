# ----------------------------------------------------------------------------------------------------
# Usage : DisconnectUsers {sde connection} {M Username} {U Username} {U_ESRI Username}
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

    if len(argv) < 5:
        arcpy.AddMessage("Wrong usage !")
        return 1

    license.Initialize(arcpy.env)

    objects = [argv[2], argv[3], argv[4]]
    status = framework.DisconnectUsers(argv[1], objects)

    return status

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main()
    framework.Finalize(result)

