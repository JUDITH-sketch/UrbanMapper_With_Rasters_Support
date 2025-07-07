from ..abc_loader import LoaderBase
import rasterio  # Pour lire les fichiers raster
from typing import Any  # Pour l'annotation de type dans preview

import rasterio  # Pour lire les fichiers raster
from typing import Any  # Pour l'annotation de type dans preview

class RasterLoader(LoaderBase):
    """
    Loader pour fichiers raster (GeoTIFF, TIFF, etc.).

    Ce loader permet de charger des fichiers raster et d'obtenir un aperçu rapide de leurs propriétés.
    Il utilise la librairie rasterio pour la lecture des fichiers.

    Attributes:
        file_path (str): Chemin vers le fichier raster à charger.
        data (numpy.ndarray): Tableau contenant les données raster chargées.
        meta (dict): Métadonnées du raster (dimensions, CRS, etc.).

    Exemple:
        >>> loader = RasterLoader(file_path="mon_raster.tif")
        >>> raster = loader._load_data_from_file()
        >>> print(loader.preview())
    """

    def __init__(self, file_path: str):
        """
        Initialise le RasterLoader avec le chemin du fichier raster.

        Args:
            file_path (str): Chemin vers le fichier raster à charger.
        """
        # Appel du constructeur parent
        super().__init__(file_path)
        # Initialisation des attributs pour stocker les données et les métadonnées
        self.data = None
        self.meta = None

    def _load_data_from_file(self) -> Any:
        """
        Charge les données raster depuis le fichier et stocke les métadonnées.

        Returns:
            numpy.ndarray: Les données raster chargées (tableau numpy).

        Raises:
            RuntimeError: Si le fichier ne peut pas être lu.
        """
        try:
            # Ouvre le fichier raster avec rasterio
            with rasterio.open(self.file_path) as src:
                # Lit toutes les bandes du raster
                self.data = src.read()
                # Stocke les métadonnées du raster
                self.meta = src.meta
            # Retourne les données raster
            return self.data
        except Exception as e:
            # En cas d'erreur, lève une exception avec un message explicite
            raise RuntimeError(f"Erreur lors du chargement du raster : {e}")

    def preview(self, format: str = "ascii") -> Any:
        """
        Génère un aperçu du raster chargé.

        Args:
            format (str): Format de sortie ("ascii" pour affichage texte, "json" pour dictionnaire).

        Returns:
            str ou dict: Un résumé des propriétés du raster.

        Raises:
            ValueError: Si le format demandé n'est pas supporté.

        Exemple:
            >>> loader = RasterLoader(file_path="mon_raster.tif")
            >>> loader._load_data_from_file()
            >>> print(loader.preview())
        """
        # Si les métadonnées ne sont pas chargées, tente de les charger
        if self.meta is None:
            try:
                with rasterio.open(self.file_path) as src:
                    self.meta = src.meta
            except Exception as e:
                return f"Impossible d'ouvrir le raster : {e}"

        # Récupère les informations principales du raster
        shape = (
            self.meta.get("count", "?"),
            self.meta.get("height", "?"),
            self.meta.get("width", "?")
        )
        dtype = self.meta.get("dtype", "?")
        crs = self.meta.get("crs", "?")

        # Retourne l'aperçu selon le format demandé
        if format == "ascii":
            return (
                f"Loader: RasterLoader\n"
                f"  Fichier: {self.file_path}\n"
                f"  Dimensions (bandes, hauteur, largeur): {shape}\n"
                f"  Type de données: {dtype}\n"
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
            raise ValueError(f"Format non supporté : {format}")


