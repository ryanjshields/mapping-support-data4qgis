"""
This script should be run from the Python consol inside QGIS.

Removes all connections from the QGIS browser that are ArcGIS Feature Server types. Written as part of a workflow to pull in and remove serers from mappingsupport.com

Script by Ryan Shields

Licence GPLv3
"""

settings = QSettings()
settings.beginGroup('qgis/connections-arcgisfeatureserver')
settings.remove("")
settings.allKeys()
settings.endGroup()
iface.reloadConnections()
