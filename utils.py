import geopandas as gpd
from shapely.geometry import Point

import warnings
warnings.filterwarnings('ignore')


def create_city_buffer(city_boundary_fp, city_buffer_fp, buffer_pct=0.3):
    city_boundary = gpd.read_file(city_boundary_fp)
    city_boundary = city_boundary.to_crs(4326)

    # Create centroid
    if city_boundary.centroid.shape[0] != 1:
        raise ValueError('City boundary has more than 1 feature. Dissolve and try again.')
    else:
        # if city_boundary.shape[0]
        centroid = city_boundary.centroid[0]
        
        city_boundary_points_geom = [Point(x) for x in city_boundary['geometry'].explode(index_parts=True)[0][0].exterior.coords]
        max_distance = max([x.distance(centroid) for x in city_boundary_points_geom])
        
        buffer_geom = centroid.buffer(max_distance*buffer_pct + max_distance)

        buffer = gpd.GeoDataFrame(geometry=[buffer_geom])
        buffer = buffer.set_crs(4326)

        # Save file
        buffer.to_file(city_buffer_fp, driver="GPKG")
