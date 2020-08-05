#!usr/bin/env python


import re
import folium
from folium.plugins import MeasureControl, HeatMapWithTime, HeatMap, TimestampedGeoJson


class Plotter:
    """Esta clase contiene todos los metodos y las operaciones necesarias para generar mapas"""
    COORDENADAS_MADRID = (40.4167598, -3.7040395)
    ZOOM_START = 13

    def __init__(self, location=COORDENADAS_MADRID, zoom=ZOOM_START):
        self._zoom = zoom
        self._location = location
        self._map = self._initialize_map()
        self._maps_path = './traffic_accidents/resources/out/maps/'

    @property
    def zoom(self):
        return self._location

    @zoom.setter
    def zoom(self, value):
        if value < 1 or value > 17:
            raise ValueError('Zoom no permitido. Pruebe con un valor en el rango 1 - 16')

        else:
            self._location = value

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        if isinstance(value, folium.folium.Map):
            self._map = value

        else:
            raise ValueError('The value must be an d instance of the class folium.Map()')

    def _initialize_map(self):
        """Initializes an empty map with Madrid Central's regions on it"""
        m = folium.Map(location=self.COORDENADAS_MADRID,
                       tiles='OpenStreetMap',
                       zoom_start=self.ZOOM_START)

        gj = folium.GeoJson(data={
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-3.711305, 40.406807],
                    [-3.702612, 40.404997],
                    [-3.693235, 40.407742],
                    [-3.692248, 40.409000],
                    [-3.694617, 40.415505],
                    [-3.690392, 40.424887],
                    [-3.696207, 40.427856],
                    [-3.702162, 40.429122],
                    [-3.705810, 40.429681],
                    [-3.714018, 40.430404],
                    [-3.715059, 40.428918],
                    [-3.711797, 40.424377],
                    [-3.714372, 40.422988],
                    [-3.712870, 40.421534],
                    [-3.714029, 40.410539]
                ]]
            }
        }, name="Madrid Central")

        gj.add_child(folium.Popup('Área de Madrid Central', max_width=900))  # agregar a al proyecto
        gj.add_to(m)
        return m

    def add_traffic_heatmap(self, locations):
        """Generates a Heatmap using an list of traffic station points"""
        heat_map = HeatMap(locations, name='Tráfico', radius=11, min_opacity=0.8,
                           gradient={0.4: 'blue', 0.7: 'lime', 1: 'red'})
        heat_map.add_to(self._map)

    def add_accident(self, data, **kwargs):
        if not(re.search(r'NUM', data.lugar)):
            try:
                folium.Marker(location=(data.lat, data.lon),
                              tooltip=folium.Tooltip(
                                  f'Tipo de colisión: {data.tipo_accidente}<br>'
                                  f'Número de parte: {data.numero_parte}<br>'
                                  f'Fecha: {data.fecha}<br>'
                                  f'Hora: {data.hora}<br>'
                                  f'Lugar: {data.lugar}<br>'
                                  f'Distrito: {data.distrito}<br>'
                                  f'Latitud: {round(data.lat, 5)}<br>'
                                  f'Longitud: {round(data.lon, 5)}<br><br>'
                                  f'Conductor 1 ---<br>'
                                  f'Tipo vehiculo: {data.conductor_1_tipo_vehiculo}<br>'
                                  f'Sexo: {data.conductor_1_sexo}<br>'
                                  f'Edad: {data.conductor_1_edad}<br><br>'
                                  f'Conductor 2 ---<br>'
                                  f'Tipo vehiculo: {data.conductor_2_tipo_vehiculo}<br>'
                                  f'Sexo: {data.conductor_2_sexo}<br>'
                                  f'Edad: {data.conductor_2_edad}<br>'),
                              icon=folium.CustomIcon(icon_image='./mc_map_generator/resources/images/icons/peligro.png',
                                                     icon_size=(12, 12))).add_to(self._map)

            except Exception as e:
                print(e)

    def generate_map(self, file_name):
        """Generates a .html map using a given name"""
        folium.LayerControl().add_to(self._map)
        self._map.add_child(MeasureControl())
        self.map.save(self._maps_path + file_name + '.html')


if __name__ == "__main__":
    pass
