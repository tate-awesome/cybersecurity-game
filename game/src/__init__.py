import time
# Before anything else is imported, so startup time (see Performance.app_started) includes every import
STARTED = time.perf_counter()


def __getattr__(name):
    # Lazy so importing a submodule (e.g. the privileged helper's server)
    # doesn't pull in App and Qt. `from src import App` still works.
    if name == "App":
        from .app_core.app import App
        return App
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
