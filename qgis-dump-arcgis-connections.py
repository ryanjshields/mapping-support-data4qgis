"""
This script should be run from the Python console inside QGIS.

Removes all connections from the QGIS browser that are ArcGIS Feature Server types. Written as part of a workflow to pull in and remove servers from mappingsupport.com

Script by Ryan Shields

Licence GPLv3
"""

print("Starting script...")

# Create an instance of QSettings
settings = QSettings()

# Begin a new group with the name 'connections/arcgisfeatureserver'
settings.beginGroup('connections/arcgisfeatureserver')

# Remove all keys and values from the current group
settings.remove("")

# End the current group
settings.endGroup()

# Reload the QGIS browser to reflect the changes
iface.reloadConnections()

print("Connections removed...")