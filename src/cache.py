import os
import pickle


class Cache(dict):
    def __init__(self, cache_file=None, update_threshold=1):
        self.cache_file = cache_file
        if self.cache_file is None:
            raise ValueError("cache_file not defined!")

        self.update_threshold = update_threshold
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
        self.update_count += 1
        if self.update_count < self.update_threshold:
            return

        self.update_count = 0
        try:
            with open(self.cache_file, "wb") as f:
                pickle.dump(dict(self), f)
        except Exception as e:
            print(f"Cache save {self.cache_file} failed: {e}")

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        # self._save_cache()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        # self._save_cache()

    def pop(self, key, default=None):
        result = super().pop(key, default)
        # self._save_cache()
        return result

    def popitem(self):
        result = super().popitem()
        # self._save_cache()
        return result

    def clear(self):
        super().clear()
        # self._save_cache()

    def __delitem__(self, key):
        super().__delitem__(key)
        # self._save_cache()
