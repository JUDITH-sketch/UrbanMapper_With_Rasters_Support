from ..abc_loader import LoaderBase

class RasterLoader(LoaderBase):
    """
    Loader for raster files (GeoTIFF, JPEG2000, PNG+worldfile).
    For now, this is only a skeleton without reading logic.
    """

    def __init__(self, file_path):
        """
        Initializes the RasterLoader with the path to the raster file.
        """
        super().__init__(file_path)
    
    def set_raster_strategy(self, strategy):
        """
        Sets the raster conversion strategy (e.g., 'points', 'polygons', etc.).
        """
        self.raster_strategy = strategy

    def set_sampling_factor(self, sampling_factor):
        """
        Sets the spatial sampling factor (float between 0 and 1).
        """
        self.sampling_factor = sampling_factor

    def set_band_selection(self, bands):
        """
        Sets the band(s) to load (e.g., [1], [1,2,3], etc.).
        """
        self.band_selection = bands

    def set_nodata_handling(self, nodata_handling):
        """
        Sets the policy for handling nodata values (e.g., 'ignore', 'mask', etc.).
        """
        self.nodata_handling = nodata_handling

    def set_max_pixels(self, max_pixels):
        """
        Sets the maximum number of pixels to load (to avoid memory issues).
        """
        self.max_pixels = max_pixels


    def _load_data_from_file(self):
        """
        load raster data and return a standard keys infos in a dictionnaire. 
        """
        import rasterio
        try:
            with rasterio.open(self.file_path) as src:
                data = src.read(1)  # read the first band
                profile = src.profile
            # return a dictionary with standard keys
            return {
                'data_shape': data.shape,
                'data_dtype': data.dtype.name,
                'crs': str(profile['crs']),
                'transform': str(profile['transform'])
            }
        except Exception as e:
            raise RuntimeError(f"Error in the loading of the raster {e}")

    def preview(self, n=5):
        """
        Method to implement: will return a preview of the raster data.
        For now, raises a NotImplementedError.
        """
        raise NotImplementedError("Raster preview is not yet implemented.")
