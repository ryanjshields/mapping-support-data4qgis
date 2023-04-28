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

# Desired state to filter by
desired_state = "Nebraska"

# Create an empty list to store the formatted connection strings for US county services
county_services_list = []

# Create a dictionary to store the count for each server owner
county_services_count = {}

# Iterate over each row in the CSV file
for row in reader:

    # Ignore rows where Type is != 2
    if row[1] != '2':
        continue

    # Extract the data from the "Server-owner", "ArcGIS-url", "County", "Town", "State", and "FIPS" columns
    arcgis_url = row[7]
    county = row[3]
    state = row[2]
    fips = row[5]

    # Check if the state matches the desired state
    if state != desired_state:
        continue

    server_owner = state + ': ' + county

    # Create a connection string for federal services where Type is 2 and FIPS length is equal to or greater than 4
    if row[1] == '2' and len(fips) >= 4:
        count = county_services_count.get(server_owner, 0)
        county_services_count[server_owner] = count + 1
        server_owner_counted = f'{server_owner}_{count:03d}'
        connection_string = f'ArcGISFeatureServer/{server_owner_counted}/FeatureServer'
        connection_settings = ('connections-arcgisfeatureserver', server_owner_counted, '', '', arcgis_url, '', '', server_owner, state, county)
        county_services_list.append(connection_settings)

# Add the county services connections to the project using QSettings
for connection_settings in county_services_list:
    connectionType = connection_settings[0]
    connectionName = f"{connection_settings[8]}: {connection_settings[9]} {connection_settings[1]}"
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
