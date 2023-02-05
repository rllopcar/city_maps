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

print(layout)
# Get Layers by name
layers = QgsProject.instance().mapLayersByName('Bounds')
layer = layers[0]

# set the map extent
map = QgsLayoutItemMap(layout)
map.setRect(20, 20, 20, 20)
ms = QgsMapSettings()
#ms.setLayers([layer]) # set layers to be mapped
# rect = QgsRectangle(ms.fullExtent())
# rect.scale(1.0)
# ms.setExtent(rect)
print(layer.extent())
extent = iface.mapCanvas().extent()
# extent = layer.extent()
map.setExtent(extent)
# map.zoomToExtent(iface.mapCanvas().extent())
layout.addLayoutItem(map)


# this accesses a specific layout, by name (which is a string)
# layout = manager.layoutByName(layoutName)

#this creates a QgsLayoutExporter object
exporter = QgsLayoutExporter(layout)                

#this exports an image of the layout object
MAP_PNG_FP = "/home/rllop/PERSONAL/toulouse_project/map_TEST.png"
exporter.exportToImage(MAP_PNG_FP, QgsLayoutExporter.ImageExportSettings()) 