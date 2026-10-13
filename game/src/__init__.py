import time
# Before anything else is imported, so startup time (see Performance.app_started) includes every import
STARTED = time.perf_counter()

from .app_core.app import App
