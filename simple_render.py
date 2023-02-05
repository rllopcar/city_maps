buffer_symbology = {'border_width_map_unit_scale': '3x:0,0,0,0,0,0', 
                        'color': '247,247,247,255', 'joinstyle': 'bevel', 
                        'offset': '0,0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 
                        'offset_unit': 'MM', 'outline_color': '82,82,82,255', 
                        'outline_style': 'no', 'outline_width': '0', 'outline_width_unit': 'MM', 
                        'style': 'solid'}

water_symbology = {'border_width_map_unit_scale': '3x:0,0,0,0,0,0', 
                        'color': '198,220,220,255', 'joinstyle': 'bevel', 
                        'offset': '0,0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 
                        'offset_unit': 'MM', 'outline_color': '247,247,247,255',
                        'outline_style': 'no', 'outline_width': '0.26', 'outline_width_unit': 'MM',
                        'style': 'solid'}    

boundary_symbology = {'border_width_map_unit_scale': '3x:0,0,0,0,0,0', 'color': '47,47,47,255', 
                            'joinstyle': 'bevel', 'offset': '0,0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 
                            'offset_unit': 'MM', 'outline_color': '134,134,134,0', 'outline_style': 'no', 
                            'outline_width': '0.26', 'outline_width_unit': 'MM', 'style': 'solid'}

streets_symbology = {'align_dash_pattern': '0', 'capstyle': 'square', 'customdash': '5;2', 'customdash_map_unit_scale': '3x:0,0,0,0,0,0', 
                    'customdash_unit': 'MM', 'dash_pattern_offset': '0', 'dash_pattern_offset_map_unit_scale': '3x:0,0,0,0,0,0', 
                    'dash_pattern_offset_unit': 'MM', 'draw_inside_polygon': '0', 'joinstyle': 'bevel', 'line_color': '83,83,83,255', 
                    'line_style': 'solid', 'line_width': '0', 'line_width_unit': 'MM', 'offset': '0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 
                    'offset_unit': 'MM', 'ring_filter': '0', 'trim_distance_end': '0', 'trim_distance_end_map_unit_scale': '3x:0,0,0,0,0,0', 
                    'trim_distance_end_unit': 'MM', 'trim_distance_start': '0', 'trim_distance_start_map_unit_scale': '3x:0,0,0,0,0,0', 
                    'trim_distance_start_unit': 'MM', 'tweak_dash_pattern_on_corners': '0', 'use_custom_dash': '0', 'width_map_unit_scale': '3x:0,0,0,0,0,0'}

bf_symbology = {'border_width_map_unit_scale': '3x:0,0,0,0,0,0', 'color': '255,255,255,255', 'joinstyle': 'bevel', 'offset': '0,0', 
                    'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM',  'outline_color': '255,255,255,0', 
                    'outline_style': 'solid', 'outline_width': '0', 'outline_width_unit': 'MM', 'style': 'solid'}

CITY_NAME = 'rouen'
buffer_layer = iface.addVectorLayer(f'/Users/rllop/Desktop/PERSONAL/{CITY_NAME}_project/buffer.gpkg', "", "ogr")
boundary_layer = iface.addVectorLayer(f'/Users/rllop/Desktop/PERSONAL/{CITY_NAME}_project/boundary.gpkg', "", "ogr")
water_layer = iface.addVectorLayer(f'/Users/rllop/Desktop/PERSONAL/{CITY_NAME}_project/water.gpkg', "", "ogr")
streets_layer = iface.addVectorLayer(f'/Users/rllop/Desktop/PERSONAL/{CITY_NAME}_project/streets.gpkg', "", "ogr")
bf_layer = iface.addVectorLayer(f'/Users/rllop/Desktop/PERSONAL/{CITY_NAME}_project/bf.gpkg', "", "ogr")

# renderer = bf_layer.renderer()
# props = bf_layer.renderer().symbol().symbolLayer(0).properties()
# props['color'] = 'white'
# bf_layer.renderer().setSymbol(QgsFillSymbol.createSimple(props))
# bf_layer.triggerRepaint()


# BUFFER LAYER
buffer_layer = QgsProject.instance().mapLayersByName("buffer")[0]
renderer = buffer_layer.renderer()
buffer_layer.renderer().setSymbol(QgsFillSymbol.createSimple(buffer_symbology))
buffer_layer.triggerRepaint()

# BOUNDARY LAYER
boundary_layer = QgsProject.instance().mapLayersByName("boundary")[0]
renderer = boundary_layer.renderer()
boundary_layer.renderer().setSymbol(QgsFillSymbol.createSimple(boundary_symbology))
boundary_layer.triggerRepaint()

# WATER LAYER
water_layer = QgsProject.instance().mapLayersByName("water")[0]
renderer = water_layer.renderer()
water_layer.renderer().setSymbol(QgsFillSymbol.createSimple(water_symbology))
water_layer.triggerRepaint()

# STREETS LAYER
streets_layer = QgsProject.instance().mapLayersByName("streets")[0]
renderer = streets_layer.renderer()
streets_layer.renderer().setSymbol(QgsLineSymbol.createSimple(streets_symbology))
streets_layer.triggerRepaint()

# BUILDING FOOTPRINTS LAYER
bf_layer = QgsProject.instance().mapLayersByName("bf")[0]
renderer = bf_layer.renderer()
bf_layer.renderer().setSymbol(QgsFillSymbol.createSimple(bf_symbology))
bf_layer.triggerRepaint()


# e.g. vlayer = iface.activeLayer()
layers = []
layers.append(bf_layer)
layers.append(water_layer)
layers.append(streets_layer)
layers.append(boundary_layer)
layers.append(buffer_layer)


options = QgsMapSettings()
options.setLayers(layers)
options.setBackgroundColor(QColor(255, 255, 255))
options.setExtent(buffer_layer.extent())
options.setOutputSize(QSize(5000, 5000))
options.setOutputDpi(300)


# Calculate Scale
print(options.mapUnits())
print(options.outputSize())
print(options.outputDpi())
print(QgsScaleCalculator())

render = QgsMapRendererParallelJob(options)

def finished():
    img = render.renderedImage()
    # save the image; e.g. img.save("/Users/myuser/render_sample_pixel_as_manual.png","png")
    image_location = f'/Users/rllop/Desktop/PERSONAL/{CITY_NAME}_project/TEST/{CITY_NAME}_map_TEST.png'
    img.save(image_location, "png")
    print("saved")

render.finished.connect(finished)

render.start()