import os
import pickle


class Cache(dict):
    DATA_DIRECTORY = "data/"

    def __init__(self, cache_file: str):
        self.cache_file = self.DATA_DIRECTORY + cache_file
        self._load_cache()

    def _load_cache(self) -> None:
        """Load precomputed values from file if available."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "rb") as f:
                    self.update(pickle.load(f))
            except Exception as e:
                print(f"Cache load {self.cache_file} failed: {e}")

    def _save_cache(self) -> None:
        """Save computed values to file."""
        try:
            with open(self.cache_file, "wb") as f:
                pickle.dump(dict(self), f)
        except Exception as e:
            print(f"Cache save {self.cache_file} failed: {e}")
