import sys
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def plot_raster_map(raster_path, sample_size=1000, cmap='terrain'):
    """
    Plot a spatial map of raster values (elevation or other) as an image.

    Args:
        raster_path (str or Path): Path to the raster (.tif) file.
        sample_size (int): Maximum number of rows/columns to display (for performance).
        cmap (str): Matplotlib colormap for visualization.
    """
    raster_path = Path(raster_path)
    if not raster_path.exists():
        print(f"File not found: {raster_path}")
        return

    with rasterio.open(raster_path) as src:
        data = src.read(1)
        nodata = src.nodata
        bounds = src.bounds

    # Downsample for visualization if needed
    nrows, ncols = data.shape
    row_step = max(1, nrows // sample_size)
    col_step = max(1, ncols // sample_size)
    data_sample = data[::row_step, ::col_step]

    # Replace nodata with NaN for plotting
    if nodata is not None:
        data_sample = np.where(data_sample == nodata, np.nan, data_sample)

    # Compute extent for imshow (left, right, bottom, top)
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

    plt.figure(figsize=(8, 6))
    im = plt.imshow(
        data_sample,
        cmap=cmap,
        extent=extent,
        origin='upper',
        aspect='equal'
    )
    plt.title(f"Raster Map: {raster_path.name}")
    plt.xlabel("Longitude or X")
    plt.ylabel("Latitude or Y")
    plt.colorbar(im, label='Value')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plot_raster_map.py <raster_file.tif>")
        sys.exit(1)
    raster_file = sys.argv[1]
    plot_raster_map(raster_file)
