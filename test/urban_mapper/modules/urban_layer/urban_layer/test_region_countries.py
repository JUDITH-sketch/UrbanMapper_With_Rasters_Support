import urban_mapper as um
from shapely import Polygon
from urban_mapper.modules import RegionCountries
import pytest

@pytest.mark.skip()
class TestRegionCountries:
  """
    It tests a RegionCities class.

  """
  layer = RegionCountries()
  loader = um.UrbanMapper().loader

  file_path = "test/data_files/small_nyc_neighborhoods.csv"
  data_neigborhood_latlong = loader.from_file(file_path).with_columns(latitude_column="latitude", longitude_column="longitude").load()
  data_neigborhood_geom = loader.from_file(file_path).with_columns(geometry_column="geometry").load()  

  def test_from_place(self):
    assert self.layer.from_place("New York, USA") is None

  def test_from_address(self):
    assert self.layer.from_address("760 United Nations Plaza, Manhattan, New York, United States", dist=100.0) is None

  # #Not suppported
  # def test_from_file(self):
  #   pass

  def test_from_bbox(self):
    # (left, bottom, right, top)
    assert self.layer.from_bbox((-74.01, 40.70, -73.97, 40.72)) is None

  def test_from_point(self):
    # Bryan Park
    # (lat, lon) center point
    assert self.layer.from_point((40.7536, -73.9832), dist=250.0) is None

  #TODO: Find a better example
  @pytest.mark.skip()
  def test_from_polygon(self):
    # Bryan Park
    polygon = Polygon([
      [-73.984804, 40.753579], 
      [-73.983932, 40.753211], 
      [-73.983061, 40.752846], 
      [-73.982273, 40.753923], 
      [-73.982487, 40.754018], 
      [-73.983343, 40.754377], 
      [-73.983997, 40.754655], 
      [-73.984085, 40.754635], 
      [-73.984804, 40.753579]
    ])     
    assert self.layer.from_polygon(polygon) is None

  # #Not suppported
  # def test_from_xml(self):
  #   pass

  def test_infer_best_admin_level(sefl):
    pass

  def test_map_nearest_layer(self):
    """
        Lat/Long columns
    """
    self.layer.from_place("New York, USA")
    assert self.layer.map_nearest_layer(
      self.data_neigborhood_latlong,
      longitude_column="longitude", latitude_column="latitude",
      output_column="streets_near"
    ) is not None


    """
        Geometry columns
    """
    self.layer = RegionCountries() # It is not possible to map the same layer twice
    self.layer.from_place("New York, New York, USA")

    assert self.layer.map_nearest_layer(
      self.data_neigborhood_geom,
      geometry_column="geometry",
      output_column="streets_near"
    ) is not None

    """
        Applying threshold
        It is not possible to map_nearest_layer twice
    """
    self.layer = RegionCountries() # It is not possible to map the same layer twice
    self.layer.from_place("New York, New York, USA")

    assert self.layer.map_nearest_layer(
      self.data_neigborhood_geom,
      geometry_column="geometry",
      output_column="streets_near",
      threshold_distance=50
    ) is not None      

  def test_get_layer_bounding_box(self):
    assert self.layer.get_layer_bounding_box() is not None

  def test_preview(self):
    assert isinstance( self.layer.preview(format = "ascii"), str)

    assert isinstance( self.layer.preview(format = "json"), dict)
    
  def test_static_render(self):
    pass    




