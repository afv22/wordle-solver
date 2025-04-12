import os
import pickle


class Cache(dict):
    DATA_DIRECTORY = "data/"

    def __init__(self, cache_file: str, write_threshold: int = 1):
        self.cache_file = self.DATA_DIRECTORY + cache_file
        self.write_threhsold = write_threshold
        self.update_count = 0
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

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.update_count += 1
        if self.update_count >= self.write_threhsold:
            self._save_cache()
            self.update_count = 0
