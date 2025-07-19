import urban_mapper as um
import pytest


# with_type
# with_mapping
# with_preview
#
# from_place
# from_address
# from_bbox
# from_point
# from_polygon
#
# build
# preview

@pytest.mark.skip()
class TestUrbanLayerFactory:
  """
    It tests a UrbanLayerFactory class.

  """  
  loader = um.UrbanMapper().urban_mapper
  loader = um.UrbanMapper().loader

  file_path = "test/data_files/small_nyc_neighborhoods.csv"
  data_neigborhood_latlong = loader.from_file(file_path).with_columns(latitude_column="latitude", longitude_column="longitude").load()
  data_neigborhood_geom = loader.from_file(file_path).with_columns(geometry_column="geometry").load() 

  def test_from_place(self):
    # layer.with_type("streets_roads")
    pass

  def test_from_address(self):
    pass

  def test_from_bbox(self):
    pass

  def test_from_point(self):
    pass

  def test_from_polygon (self):
    pass

  def test_preview(self):
    pass

