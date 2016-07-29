# ----------------------------------------------------------------------------------------------------
# Usage : ChangePathInMxd {source Mxd directory} {target Mxd directory} {source db name} {target sde connection file} {target db name}
# ----------------------------------------------------------------------------------------------------

import sys, datetime, os, arcpy
frk = os.path.join(os.getcwd(), '..\\Common')
sys.path.insert(0, frk)
import license, framework

# ----------------------------------------------------------------------------------------------------
def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) < 6:
        arcpy.AddMessage("Wrong usage !")
        return 1

    license.Initialize(arcpy.env)

    # Delete existing files
    status = framework.DeleteDirectory(argv[2])
    if status != 0:
        return status

    # Copy Mxds to target directory
    status = framework.CreateDirectory(argv[2])
    if status != 0:
        return status

    status = framework.CopyFiles(argv[1], argv[2], "*.mxd", True)
    if status != 0:
        return status

    # Change DataSource for each file
    for file in os.listdir(argv[2]):
        fullFileName = os.path.join(argv[2], file)
        status = framework.ChangeDataSource(fullFileName, argv[3], argv[4], argv[5])
        if status != 0:
            return status

    return 0

# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main()
    framework.Finalize(result)
