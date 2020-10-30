# -*- coding: utf-8 -*-
"""QGIS Toggle Labels Widget

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = '(C) 2019 by Nyall Dawson'
__date__ = '18/01/2019'
__copyright__ = 'Copyright 2019, North Road'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
from qgis.PyQt.QtCore import (
    QTranslator,
    QCoreApplication
)
from qgis.PyQt.QtWidgets import (
    QWidget,
    QCheckBox,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy
)
from qgis.core import (
    QgsApplication,
    QgsMapLayer
)
from qgis.gui import (
    QgisInterface,
    QgsGui,
    QgsLayerTreeEmbeddedWidgetProvider
)

VERSION = '1.0.1'


class LayerTreeToggleLabelsWidget(QWidget):
    """
    Layer tree widget for toggling the labels in a layer
    """

    def __init__(self, layer):
        super().__init__()
        self.layer = layer

        self.setAutoFillBackground(False)
        self.checkbox = QCheckBox(self.tr("Show Labels"))
        layout = QHBoxLayout()
        spacer = QSpacerItem(1, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        layout.addWidget(self.checkbox)
        layout.addItem(spacer)
        self.setLayout(layout)

        # init from layer
        if self.layer.type() == QgsMapLayer.VectorLayer:
            self.checkbox.setChecked(self.layer.labelsEnabled())
            self.checkbox.toggled.connect(self.toggled)

    def toggled(self, active):
        """
        Triggered when the checkbox is toggled.
        """
        self.layer.setLabelsEnabled(active)
        self.layer.triggerRepaint()


class LayerTreeToggleLabelsProvider(QgsLayerTreeEmbeddedWidgetProvider):
    """
    Layer tree provider for toggle labels widgets
    """

    def id(self):  # pylint: disable=missing-docstring
        return 'labels_toggle'

    def name(self):  # pylint: disable=missing-docstring
        return QCoreApplication.translate('ToggleLabelsWidget', 'Toggle labels')

    def createWidget(self, layer, _):  # pylint: disable=missing-docstring
        return LayerTreeToggleLabelsWidget(layer)

    def supportsLayer(self, layer):  # pylint: disable=missing-docstring
        return layer.type() == QgsMapLayer.VectorLayer


class ToggleLabelsWidgetPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface: QgisInterface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        super().__init__()
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QgsApplication.locale()
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.provider = None

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.provider = LayerTreeToggleLabelsProvider()
        QgsGui.layerTreeEmbeddedWidgetRegistry().addProvider(self.provider)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        QgsGui.layerTreeEmbeddedWidgetRegistry().removeProvider(self.provider.id())
        self.provider = None
