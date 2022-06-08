import folium
import ee
import io
from PIL import Image
import json

def add_ee_layer(self, ee_object, vis_params, name):
    print(type(ee_object))
    try:
        # display ee.Image()
        if isinstance(ee_object, ee.image.Image):
            map_id_dict = ee.Image(ee_object).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)

        # display ee.ImageCollection()
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)

        # display ee.Geometry()
        elif isinstance(ee_object, ee.geometry.Geometry):
            folium.GeoJson(
                data=ee_object.getInfo(),
                name=name,
                overlay=True,
                control=True
            ).add_to(self)

        # display ee.FeatureCollection()
        elif isinstance(ee_object, ee.featurecollection.FeatureCollection):
            ee_object_new = ee.Image().paint(ee_object, 0, 2)
            map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True
            ).add_to(self)

    except:
        print("Could not display {}".format(name))

# Add EE drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

def get_image_path(time):
    return 'maps/' + str(time) + '.png'

def get_json_path(time):
    return 'maps/' + str(time) + '.json'

def img_from_geojson(time):
    # ee.Authenticate()
    ee.Initialize()

    #Получаем последний полигон из geojson
    area = []
    with open(get_json_path(time)) as f:
        data = json.load(f)
    for feature in data['features']:
        area = feature['geometry']['coordinates']

    bounds = ee.Geometry.Polygon(area)
    # // Import the Landsat 8 TOA image collection.
    l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
    image = ee.Image(
        l8
            .filterBounds(bounds)
            # .filterDate('2015-01-01', '2015-12-31')
            .sort('CLOUD_COVER')
            .first()
    )
    # nir = image.select('B5');
    # red = image.select('B4');
    # ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI');

    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
    ndvi_viz = {'min': 0, 'max': 1, 'palette': ["gray", "yellow", "yellowgreen", "green", "darkgreen"]}
    ndvi = ndvi.clip(bounds)

    #Получаем центр карты
    point = bounds.centroid().getInfo()['coordinates']
    # Переворачиваем координаты для folium
    point = [point[1], point[0]]
    # print(point)

    map_ndvi = folium.Map(location=point, zoom_start=11)
    map_ndvi.add_ee_layer(ndvi, ndvi_viz, 'NDVI')

    #Сохраняем карту на диск (png) с помощью selenium
    img_data = map_ndvi._to_png(delay=5)
    img = Image.open(io.BytesIO(img_data))
    img.save(get_image_path(time))