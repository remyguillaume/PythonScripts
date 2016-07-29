# For Http calls
import httplib, urllib, json, sys, getpass, datetime, arcpy

# Defines the entry point into the script
def main(argv=None):

    start = datetime.datetime.now()

    serverName = "<ESRI servername>"
    serverPort = "6080"
    username = 'arcgis'
    password = '<arcgis user password>'
    
    dbName = argv[0];
    serviceName = argv[1];
    operation = argv[2];
    serviceType = argv[3];

    serviceUrl = "/arcgis/admin/services/" + dbName + "/" + serviceName + "." + serviceType + "/"
    
    # Get a token
    token = getToken(username, password, serverName, serverPort)
    if token == None:
        arcpy.AddError("Could not generate a token with the username and password provided.")
        return

    if operation == "STOP" or operation == "RESTART":
        stopUrl = serviceUrl + "STOP"
        processRequest(stopUrl, token, serverName, serverPort)

    if operation == "START" or operation == "RESTART":
        startUrl = serviceUrl + "START"
        processRequest(startUrl, token, serverName, serverPort)

    end = datetime.datetime.now()
    arcpy.AddMessage("Service stopped, started or restarted successfully in " + str(end - start) + ".")
   

def processRequest(url, token, serverName, serverPort):
    
    params = urllib.urlencode({'token': token, 'f': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # Connect to URL and post parameters    
    httpConn = httplib.HTTPConnection(serverName, serverPort)

    httpConn.request("POST", url, params, headers)
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        arcpy.AddError("Error while executing stop or start. Please check the parameters and try again.")
        return
    else:
        responseData = response.read()
                
        # Check that data returned is not an error object
        if not assertJsonSuccess(responseData):
           arcpy.AddError("Error returned when starting/stopping service " + responseData + ".")

    httpConn.close()


# A function to generate a token given username, password and the adminURL.
def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"
    
    params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'f': 'json'}) 
    # add ", 'encrypted': 'true'" in ordre to pass encrypted user & password
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", tokenURL, params, headers)
    
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        arcpy.AddError("Error while fetching tokens from admin URL. Please check the URL and try again.")
        return
    else:
        data = response.read()
        httpConn.close()
        
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            return
        
        # Extract the token from it
        token = json.loads(data)
        return token['token']
        

# A function that checks that the input JSON object 
#  is not an error object.
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        arcpy.AddError("Error: JSON object returns an error. " + str(obj))
        return False
    else:
        return True
    
        
# Script start
if __name__ == "__main__":
   main(sys.argv[1:])
