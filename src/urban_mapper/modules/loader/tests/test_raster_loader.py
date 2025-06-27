import pytest
from urban_mapper.modules.loader.loaders.raster_loader import RasterLoader

def test_raster_loader_initialization():
    loader = RasterLoader("fake_path.tif")
    assert str(loader.file_path) == "fake_path.tif"

def test_raster_loader_setters():
    loader = RasterLoader("fake_path.tif")
    loader.set_raster_strategy("points")
    loader.set_sampling_factor(0.5)
    loader.set_band_selection([1,2,3])
    loader.set_nodata_handling("ignore")
    loader.set_max_pixels(10000)
    assert loader.raster_strategy == "points"
    assert loader.sampling_factor == 0.5
    assert loader.band_selection == [1,2,3]
    assert loader.nodata_handling == "ignore"
    assert loader.max_pixels == 10000

def test_raster_loader_load_not_implemented():
    loader = RasterLoader("fake_path.tif")
    with pytest.raises(NotImplementedError):
        loader._load_data_from_file()

