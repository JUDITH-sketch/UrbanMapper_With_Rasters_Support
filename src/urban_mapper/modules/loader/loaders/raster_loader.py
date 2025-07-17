from ..abc_loader import LoaderBase
import rasterio
from typing import Any
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
from rasterio.transform import xy
from pyproj import CRS, Transformer

class RasterLoader:
    """
    Loader for raster files with block-wise downsampling (average pooling) and centroids as geometry.
    Returns a GeoDataFrame where each row corresponds to an aggregated pixel (block).
    """

    def __init__(self, file_path, block_size=10, **kwargs):   # block_size est le facteur de downsampling (4x4 par défaut)
        self.file_path = file_path
        self.block_size = block_size
        self.meta = None
        self.bounds = None

    def _downsample_band(self, band):
        """
        Effectue le downsampling par blocs et calcule la moyenne pour chaque bloc non-recouvrant.
        """
        h, w = band.shape
        bs = self.block_size

        # Découpe l'image aux dimensions multiples du block_size pour éviter les bords incomplets
        h_ds = h // bs
        w_ds = w // bs
        band_cropped = band[:h_ds * bs, :w_ds * bs]

        # Remodèle pour avoir un 4D (h_blocks, block_size, w_blocks, block_size) puis moyenne par bloc
        band_blocks = band_cropped.reshape(h_ds, bs, w_ds, bs)
        band_ds = band_blocks.mean(axis=(1, 3))  # moyenne sur les axes blocs internes

        return band_ds

    def _load_data_from_file(self) -> gpd.GeoDataFrame:
        try:
            with rasterio.open(self.file_path) as src:
                band = src.read(1)
                transform = src.transform
                crs = src.crs
                nodata = src.nodata

                self.meta = src.meta
                self.bounds = src.bounds

                # Handle NoData: met à NaN pour la moyenne
                if nodata is not None:
                    band = np.where(band == nodata, np.nan, band)

                # Downsampling
                band_ds = self._downsample_band(band)
                h_ds, w_ds = band_ds.shape

                # Génère les indices ligne/colonne de chaque pixel agrégé
                rows, cols = np.indices((h_ds, w_ds))

                # Calcule la position du centre de chaque bloc dans l'image d'origine
                bs = self.block_size
                center_rows = rows * bs + bs // 2
                center_cols = cols * bs + bs // 2

                # Transform raster to world coordinates for block centers
                xs, ys = rasterio.transform.xy(transform, center_rows, center_cols)
                xs = np.array(xs).flatten()
                ys = np.array(ys).flatten()

                # Calcul des valeurs
                values = band_ds.flatten()

                # Geometry = centre (comme un Point)
                geoms = []
                for r, c in zip(center_rows.flatten(), center_cols.flatten()):
                    # (r, c) = ligne et colonne du bloc (dans la grille agrégée)
                    min_row = r - bs // 2
                    min_col = c - bs // 2
                    max_row = min_row + bs
                    max_col = min_col + bs

                    # On récupère les coordonnées des 4 coins du pixel agrégé :
                    corners = [
                        rasterio.transform.xy(transform, min_row, min_col, offset='ul'),  # haut-gauche
                        rasterio.transform.xy(transform, min_row, max_col, offset='ur'),  # haut-droit
                        rasterio.transform.xy(transform, max_row, max_col, offset='lr'),  # bas-droit
                        rasterio.transform.xy(transform, max_row, min_col, offset='ll')   # bas-gauche
                    ]
                    poly = Polygon(corners)
                    geoms.append(poly)

                # Latitude/Longitude par transformation CRS → WGS84
                transformer = Transformer.from_crs(crs, 4326, always_xy=True)
                lon, lat = transformer.transform(xs, ys)
                
                # Aire pour chaque bloc (en unités CRS projeté) — zone du bloc
                if CRS.from_user_input(crs).is_projected:
                    pixel_width = abs(transform.a)
                    pixel_height = abs(transform.e)
                    area = (pixel_width * pixel_height) * (bs * bs)
                    areas = np.full(values.shape, area)
                else:
                    areas = [None] * values.size  # Hors CRS projeté, zone complexe : à raffiner si utile

                # Création du GeoDataFrame
                gdf = gpd.GeoDataFrame({
                    'pixel_id': np.arange(len(values)),
                    'row': rows.flatten(),
                    'col': cols.flatten(),
                    'area': areas,
                    'value': values,
                    'latitude': lat,
                    'longitude': lon,
                    'geometry': geoms
                }, crs=crs)

                return gdf

        except Exception as e:
            raise RuntimeError(f"Error while loading downsampled raster: {e}")


    def preview(self, format: str = "ascii") -> Any:
        """
        Generates a preview of the loaded raster information.

        Args:
            format (str): Output format ("ascii" for text display, "json" for dictionary).

        Returns:
            str or dict: A summary of the raster properties.

        Raises:
            ValueError: If the requested format is not supported.

        """
        # If metadata is not loaded, try to load it
        if self.meta is None:
            try:
                with rasterio.open(self.file_path) as src:
                    self.meta = src.meta
            except Exception as e:
                return f"Unable to open raster: {e}"

        # Get main raster information
        shape = (
            self.meta.get("count", "?"),
            self.meta.get("height", "?"),
            self.meta.get("width", "?")
        )
        dtype = self.meta.get("dtype", "?")
        crs = self.meta.get("crs", "?")

        # Return preview according to requested format
        if format == "ascii":
            return (
                f"Loader: RasterLoader\n"
                f"  File: {self.file_path}\n"
                f"  Dimensions (bands, height, width): {shape}\n"
                f"  Data type: {dtype}\n"
                f"  CRS: {crs}"
            )
        elif format == "json":
            return {
                "loader": "RasterLoader",
                "file": self.file_path,
                "shape": shape,
                "dtype": str(dtype),
                "crs": str(crs)
            }
        else:
            raise ValueError(f"Unsupported format: {format}")


