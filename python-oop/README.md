# Python OOP examples

Each script is a self-contained example and can be run from the project root:

```bash
python3 python-oop/01_classes_and_objects.py
```

The examples progress from basic classes to attributes and methods, encapsulation, inheritance, multiple inheritance with mixins, polymorphism, abstract interfaces, composition, and advanced decorators.

The scripts intentionally use type hints, `main()` entry points, validation, and standard-library data structures so they are useful as small best-practice references rather than only syntax demonstrations.

## Advanced decorator examples

The advanced section separates decorators by their actual standard-library location:

- `09_properties_and_validation.py`: built-in `@property` and a reusable descriptor.
- `10_cached_properties.py`: `functools.cached_property` and explicit cache invalidation.
- `11_context_managers.py`: `contextlib.contextmanager`, `asynccontextmanager`, and a class-based context manager.
- `12_method_decorators.py`: type-safe custom method decorators using `functools.wraps`, `ParamSpec`, and decorator stacking.
- `13_dispatch_and_ordering.py`: `functools.singledispatchmethod` and `total_ordering`.
- `14_caching_methods.py`: `functools.cache` and bounded `lru_cache` on pure static methods.
- `15_class_decorators_and_registries.py`: a class decorator for an explicit plugin registry.

`property` is a built-in decorator. `cached_property`, `cache`, `lru_cache`, `singledispatchmethod`, `total_ordering`, and `wraps` come from `functools`. Context manager decorators come from `contextlib`.

These examples favor patterns used in larger codebases: immutable value objects, narrow public APIs, explicit cache ownership, exception-safe resource cleanup, metadata-preserving decorators, typed interfaces, bounded caches, and isolated registries.
