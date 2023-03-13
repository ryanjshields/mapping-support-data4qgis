"""
This script should be run from the Python consol inside QGIS.

It adds US State-level Government ArcGIS servers as connections in the QGIS Browser.
The sources are pulled directly from the CSV file at mappingsupport.com which regularly tests the status of the server and updates the connection status.
For my workflows I don't leave these connected always. I use qgis-dump-arcgis-connections.py to remove the connections when completed. This ensures that the next time I connect will have most recent updates from mappingsupport.com
Other scripts for connecting to public-facing services for the US Federal Government, as well as counties and towns for each US state.

Script by Ryan Shields (inspired by script from Klas Karlsson to add XYZ tile sources)

Source documentation at https://mappingsupport.com/p/surf_gis/list-federal-state-county-city-GIS-servers.pdf
Licence GPLv3
"""

import csv
import urllib.request
import html
import codecs

# URL for the CSV file
url = "https://mappingsupport.com/p/surf_gis/list-federal-state-county-city-GIS-servers.csv"

# Open the URL and read the data as bytes
response = urllib.request.urlopen(url)
data = response.read()

# Decode the bytes data using a specific encoding
decoded_data = data.decode('utf-8', 'ignore')

# Open the decoded data as a CSV file
reader = csv.reader(decoded_data.splitlines(), delimiter=',')

# Create an empty list to store the formatted connection strings for federal services
state_services_list = []

# Create a dictionary to store the count for each server owner
state_services_count = {}

# Iterate over each row in the CSV file
for row in reader:

    # Ignore rows where Type is != 1
    if row[1] != '2':
        continue

    # Extract the data from the "Server-owner", "ArcGIS-url", "County", "Town", and "State" columns
    server_owner = row[6]
    arcgis_url = row[7]
    state = row[2]
    fips = row [5]

    # Create a connection string for federal services where Type is 1
    if row[1] == '2' and fips != '' and len(fips) <= 2:
        count = state_services_count.get(server_owner, 0)
        state_services_count[server_owner] = count + 1
        server_owner_counted = f'{server_owner}_{count:03d}'
        connection_string = f'ArcGISFeatureServer/{server_owner_counted}/FeatureServer'
        connection_settings = ('connections-arcgisfeatureserver', server_owner_counted, '', '', arcgis_url, '', '', server_owner, state)
        state_services_list.append(connection_settings)

# Add the federal services connections to the project using QSettings
for connection_settings in state_services_list:    
    connectionType = connection_settings[0]
    connectionName = connection_settings[8] + ': ' + connection_settings[1]
    authcfg = connection_settings[2]
    password = connection_settings[3]
    referer = 'MapperSupport.com: ' + connection_settings[7] 
    url = connection_settings[4]
    user = connection_settings[6]
    
    QSettings().setValue("qgis/%s/%s/authcfg" % (connectionType, connectionName), authcfg)
    QSettings().setValue("qgis/%s/%s/password" % (connectionType, connectionName), password)
    QSettings().setValue("qgis/%s/%s/referer" % (connectionType, connectionName), referer)
    QSettings().setValue("qgis/%s/%s/url" % (connectionType, connectionName), url)
    QSettings().setValue("qgis/%s/%s/username" % (connectionType, connectionName), user)
    
# Update GUI
iface.reloadConnections()

print('Layers added')
