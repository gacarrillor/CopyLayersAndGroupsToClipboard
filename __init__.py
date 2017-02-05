"""
/***************************************************************************
 CopyLayersAndGroupsToClipboard
                                 A QGIS plugin
 Copy selected layers and groups from Layers Panel to clipboard, so that they can be pasted in other QGIS instances.
                             -------------------
        begin                : 2017-02-05
        copyright            : (C) 2017 by German Carrillo, GeoTux
        email                : gcarrillo@linuxmail.org
***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
def name():
    return "Copy layers and groups to clipboard"
def description():
    return "Copy selected layers and groups from Layers Panel to clipboard, so that they can be pasted into other QGIS instances."
def version():
    return "Version 1.0"
def icon():
    return "paste.png"
def qgisMinimumVersion():
    return "2.0"
def classFactory(iface):
    from copyLayersAndGroupsToClipboard import CopyLayersAndGroupsToClipboard
    return CopyLayersAndGroupsToClipboard(iface)
