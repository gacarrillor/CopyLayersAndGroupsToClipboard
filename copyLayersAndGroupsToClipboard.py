# -*- coding:utf-8 -*-
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
import os
import time
import tempfile
import codecs

from qgis.core import ( QgsLayerDefinition, QgsProject )
from PyQt4.QtGui import QApplication, QIcon, QAction
from PyQt4.QtXml import QDomDocument

import resources_rc

class CopyLayersAndGroupsToClipboard:

    def __init__( self, iface ):
        self.iface = iface
        self.doc = None
        self.layersElement = None
        self.clipboard = QApplication.clipboard()

    def initGui( self ):
        icon = QIcon()
        icon.addFile( ":/plugins/CopyLayersAndGroupsToClipboard/copy.png" )
        self.actionCopy = QAction( icon, u"Copy selected layers and groups to clipboard (Ctrl+Ins)", self.iface.mainWindow() )
        self.actionCopy.triggered.connect( self.copy )
        self.iface.registerMainWindowAction( self.actionCopy, "Ctrl+Ins" )

        icon = QIcon()
        icon.addFile( ":/plugins/CopyLayersAndGroupsToClipboard/paste.png" )
        self.actionPaste = QAction( icon, u"Paste layers and groups from clipboard (Shift+Ins)", self.iface.mainWindow() )
        self.actionPaste.triggered.connect( self.paste )
        self.iface.registerMainWindowAction( self.actionPaste, "Shift+Ins" )

        self.iface.addPluginToMenu( u"Copy selected layers and groups to clipboard", self.actionCopy )
        self.iface.addPluginToMenu( u"Copy selected layers and groups to clipboard", self.actionPaste )

        self.toolbar = self.iface.addToolBar( "Copy layers and groups to clipboard" )
        self.toolbar.setObjectName("CopyLayersAndGroupsToClipboard")
        self.toolbar.addAction( self.actionCopy )
        self.toolbar.addAction( self.actionPaste )

    def unload( self ):
        self.iface.removePluginMenu( u"Copy selected layers and groups to clipboard", self.actionCopy )
        self.iface.removePluginMenu( u"Paste layers and groups from clipboard", self.actionPaste )
        self.iface.mainWindow().removeToolBar( self.toolbar )

    def copy( self ):
        # Iterate
        selectedNodes = self.iface.layerTreeView().selectedNodes( True )
        if len( selectedNodes) == 0:
            self.iface.messageBar().pushMessage( "Copy layers and groups", "First select at least 1 layer or group in the Layers Panel.", 0, 7 )
            return

        doc = QDomDocument( "QGIS-layers-and-groups" )
        QgsLayerDefinition.exportLayerDefinition( doc, selectedNodes, "", "" )

        tempDir = tempfile.gettempdir()
        xmlFilePath = os.path.join( tempDir, str(time.time()).replace(".","")+".qlr" )
        f = codecs.open( xmlFilePath, 'w', encoding='utf-8' )
        f.write( doc.toString() )
        f.close()

        self.clipboard.setText( "@QGIS-layers-and-groups@{}".format( xmlFilePath ) )
        self.iface.messageBar().pushMessage( "Copy layers and groups", "Selected layers and/or groups were copied to clipboard.", 0, 5 )

    def paste( self ):
        bNoClipboardData = False
        clipboardText = self.clipboard.text()

        if not ( isinstance( clipboardText, str ) or isinstance( clipboardText, unicode ) ):
            self.showNoDataMessage()
            return

        xmlFilePath = clipboardText.split( "@QGIS-layers-and-groups@" )
        if len( xmlFilePath ) != 2:
            self.showNoDataMessage()
            return

        xmlFilePath = xmlFilePath[1] # Get payload

        if not ( os.path.isfile( xmlFilePath ) and os.path.splitext( xmlFilePath )[1] == '.qlr' ):
            self.showNoDataMessage()
            return

        QgsLayerDefinition.loadLayerDefinition( xmlFilePath, QgsProject.instance().layerTreeRoot() )


    def showNoDataMessage( self ):
        self.iface.messageBar().pushMessage( "Copy layers and groups", "The clipboard doesn't contain valid QGIS layers and/or groups to paste.", 1, 7 )
