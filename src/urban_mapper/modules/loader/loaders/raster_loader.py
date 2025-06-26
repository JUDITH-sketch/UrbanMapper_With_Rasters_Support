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

    def _load_data_from_file(self):
        """
        Method to implement: will load raster data and return a standard object.
        For now, raises a NotImplementedError.
        """
        raise NotImplementedError("Raster support is not yet implemented.")

    def preview(self, n=5):
        """
        Method to implement: will return a preview of the raster data.
        For now, raises a NotImplementedError.
        """
        raise NotImplementedError("Raster preview is not yet implemented.")
