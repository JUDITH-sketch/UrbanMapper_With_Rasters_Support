from urban_mapper.modules.loader.loaders.raster_loader import RasterLoader

loader = RasterLoader("data/lower_manhattan_dem.tif")
result = loader._load_data_from_file()
print(result)
