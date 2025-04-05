import pickle
import os


class Cache:
    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        if self.cache_file is None:
            raise ValueError("CACHE_FILE not defined!")

        self.cache = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load precomputed entropy values from file if available."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "rb") as f:
                    self.cache = pickle.load(f)
            except Exception:
                print("Cache load failed.")

    def _save_cache(self) -> None:
        """Save computed entropy values to file."""
        try:
            with open(self.cache_file, "wb") as f:
                pickle.dump(self.cache, f)
        except Exception:
            print("Cache save failed.")
