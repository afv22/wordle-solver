import os
import pickle


class Cache:
    CACHE_FILE = None

    def __init__(self, cache_file: str = None):
        if cache_file:
            self.CACHE_FILE = cache_file

        if self.CACHE_FILE is None:
            raise ValueError("CACHE_FILE not defined!")

        self.cache = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load precomputed entropy values from file if available."""
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, "rb") as f:
                    self.cache = pickle.load(f)
            except Exception:
                print("Cache load failed.")

    def _save_cache(self) -> None:
        """Save computed entropy values to file."""
        try:
            with open(self.CACHE_FILE, "wb") as f:
                pickle.dump(self.cache, f)
        except Exception:
            print("Cache save failed.")
