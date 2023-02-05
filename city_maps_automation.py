import os
import sys
import pandas as pd
from osgeo import ogr
import geopandas as gpd
from utils import create_city_buffer

from qgis.utils import iface
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import QSize
from qgis.core import (QgsApplication,
                        QgsPrintLayout,
                        QgsProject, 
                        QgsRectangle,
                        QgsVectorLayer, 
                        QgsMapSettings, 
                        QgsLayoutItemMap,
                        QgsLayoutPoint,
                        QgsLayoutExporter,
                        QgsMapRendererParallelJob,
                        QgsUnitTypes,
                        QgsLayoutSize)

import warnings
warnings.filterwarnings('ignore')


# INPUT FILEPATHS
CITY_BOUNDARY_FP = "/home/rllop/PERSONAL/toulouse_project/city_boundary.gpkg"
CITY_BUFFER_FP = "/home/rllop/PERSONAL/toulouse_project/city_buffer.gpkg"
CITY_BF_FP = "/home/rllop/PERSONAL/toulouse_project/city_bf.gpkg"
CITY_STREETS_FP = "/home/rllop/PERSONAL/toulouse_project/city_streets.gpkg"
CITY_STREETS_OUTSIDE_FP = "/home/rllop/PERSONAL/toulouse_project/city_streets_outside.gpkg"
CITY_BRIDGES_FP = "/home/rllop/PERSONAL/toulouse_project/city_bridges"

# OUTPUT FILEPATHS
MAP_PNG_FP = "/home/rllop/PERSONAL/toulouse_project/map_TEST.png"

# Create city buffer file
create_city_buffer(CITY_BOUNDARY_FP, CITY_BUFFER_FP)

QGIS_PROJECT_FP = "/home/rllop/PERSONAL/toulouse_project/toulouse_project.qgz"

# supply path to qgis install location
QgsApplication.setPrefixPath("/home/rllop/anaconda3/envs/personal/bin/qgis", True)

# create a reference to the QgsApplication, setting the second argument to False disables the GUI
qgs = QgsApplication([], False)

# load providers
qgs.initQgis()

# Load project
project = QgsProject.instance()
project.read(QGIS_PROJECT_FP)

# Load Layer
buffer_layer = QgsVectorLayer(CITY_BUFFER_FP, "city_buffer", "ogr")
if not buffer_layer.isValid():
    print("Layer failed to load!")
else:
    QgsProject.instance().addMapLayer(buffer_layer)

dict_layers = QgsProject.instance().mapLayers()
layers = [dict_layers[x] for x in dict_layers.keys()]


# Initialize the layout
project = QgsProject.instance()             #gets a reference to the project instance
manager = project.layoutManager()           #gets a reference to the layout manager
layout = QgsPrintLayout(project)            #makes a new print layout object, takes a QgsProject as argument
layoutName = "PrintLayout"

layouts_list = manager.printLayouts()
for layout in layouts_list:
    if layout.name() == layoutName:
        manager.removeLayout(layout)
        
layout = QgsPrintLayout(project)
layout.initializeDefaults()                 #create default map canvas
layout.setName(layoutName)
manager.addLayout(layout)

# set the map extent
map = QgsLayoutItemMap(layout)
map.setRect(40, 40, 40, 40)
layers = QgsProject.instance().mapLayersByName('city_boundary')
layer = layers[0]
print(layer.extent())
map.setExtent(layer.extent())
map.setBackgroundColor(QColor(255, 255, 255))
layout.addLayoutItem(map)

#this accesses a specific layout, by name (which is a string)
layout = manager.layoutByName(layoutName)

#this creates a QgsLayoutExporter object
exporter = QgsLayoutExporter(layout)                

#this exports a pdf of the layout object
exporter.exportToPdf('/home/rllop/PERSONAL/toulouse_project/map_TEST.pdf', QgsLayoutExporter.PdfExportSettings())      

#this exports an image of the layout object
exporter.exportToImage(MAP_PNG_FP, QgsLayoutExporter.ImageExportSettings()) 