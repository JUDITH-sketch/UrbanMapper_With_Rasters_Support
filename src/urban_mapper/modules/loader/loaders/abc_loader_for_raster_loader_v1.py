"""
Initial attempt at creating an abstract base class for raster data loading in UrbanMapper.

This file represents an early development stage where a separate abstract loader
was created specifically for raster data. However, this implementation was later
deprecated as it was understood that UrbanMapper's existing abstract loader
architecture was already sufficient for handling all types of data, including rasters.

Historical Context:
    - Created during initial exploration of UrbanMapper's architecture
    - Attempted to create a raster-specific loader hierarchy
    - Later superseded by the main UrbanMapper loader implementation

Note:
    This file is kept for reference but should not be used in production.
    Use UrbanMapper's main abstract loader implementation instead.

Classes:
    - RasterLoaderBase: Abstract base class for raster loaders (deprecated)
    - GeoTiffLoader: Concrete implementation for GeoTIFF files (deprecated)
"""

from abc import ABC, abstractmethod  # Python module for creating abstract classes
from pathlib import Path  # Python module for handling file paths
from typing import Union, Optional, Any, Dict  # Python module for defining types for variables and functions
import geopandas as gpd  # Python module for handling geospatial data with dataframes
from beartype import beartype  # Python module for checking types of variables and functions at runtime
from urban_mapper.modules.loader.helpers import ensure_coordinate_reference_system  # Urban_mapper module to verify the coordinate reference system
from urban_mapper.config import DEFAULT_CRS  # Urban_mapper module to define application constants
from urban_mapper.utils import file_exists  # Urban_mapper module to verify file existence before loading

import rasterio


# Creating an abstract class for rasters
@beartype
class RasterLoaderBase(ABC):
    """Base Class For `Raster Loaders`.

    This abstract class defines the common interface that all raster loader implementations
    **must implement**. `Raster Loaders` are responsible for reading spatial raster data from various
    file formats and converting them to appropriate data structures for processing.

    Attributes:
        file_path (Path): Path to the raster file to load.
        coordinate_reference_system (str): The coordinate reference system to use.
        additional_loader_parameters (Dict[str, Any]): Additional parameters specific to the loader implementation.
    """

    def __init__(
        self,
        file_path: Union[str, Path],
        coordinate_reference_system: str = DEFAULT_CRS,
        **additional_loader_parameters: Any,
    ) -> None:
        self.file_path: Path = Path(file_path)
        self.coordinate_reference_system: str = coordinate_reference_system
        self.additional_loader_parameters: Dict[str, Any] = additional_loader_parameters

    @abstractmethod
    def _load_data_from_file(self) -> Any:  # Return type will depend on implementation
        """Internal implementation method for loading raster data from a file."""
        ...

    @file_exists("file_path")
    def load_data_from_file(self) -> Any:
        """Load raster data from a file."""
        return self._load_data_from_file()

    @abstractmethod
    def preview(self, format: str = "ascii") -> Any:
        """Generate a preview of the instance's `loader`."""
        pass

# Concrete implementation of a raster loader
class GeoTiffLoader(RasterLoaderBase):
    """Loader for GeoTIFF raster files using Rasterio."""

    def _load_data_from_file(self) -> Any:
        """Load a GeoTIFF file using Rasterio."""
        import rasterio
        
        with rasterio.open(str(self.file_path)) as src:
            # Read the raster data
            data = src.read()
            # Get metadata
            meta = src.meta
            
            # Create a wrapper object that combines data and metadata
            # This could be a custom class or a tuple/dict
            return {"data": data, "meta": meta, "src": src}

    def preview(self, format: str = "ascii") -> Any:
        """Generate a preview of the raster data."""
        if format == "ascii":
            # Generate ASCII preview
            return self._generate_ascii_preview()
        elif format == "json":
            # Generate JSON preview
            return self._generate_json_preview()
        else:
            raise ValueError(f"Unsupported format: {format}")

