"""Shared function caching with ``cache`` and bounded ``lru_cache``."""

from functools import cache, lru_cache


class PathService:
    @staticmethod
    @lru_cache(maxsize=256)
    def normalize(raw_path: str) -> str:
        """Cache a pure, bounded, frequently repeated transformation."""
        return "/".join(part for part in raw_path.strip("/").split("/") if part)

    @classmethod
    def clear_caches(cls) -> None:
        cls.normalize.cache_clear()


class Fibonacci:
    @staticmethod
    @cache
    def calculate(number: int) -> int:
        if number < 0:
            raise ValueError("number cannot be negative")
        if number < 2:
            return number
        return Fibonacci.calculate(number - 1) + Fibonacci.calculate(number - 2)


def main() -> None:
    print(PathService.normalize("/api//v1/users/"))
    PathService.normalize("/api//v1/users/")
    print(PathService.normalize.cache_info())
    print(Fibonacci.calculate(30))


if __name__ == "__main__":
    main()
