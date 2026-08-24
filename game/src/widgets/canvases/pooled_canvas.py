'''
Mixin that lets a Tk canvas reuse its drawn items across animation frames
instead of the delete("all") + recreate-everything-from-scratch pattern.
Every create_line/create_rectangle/create_oval/create_text/create_polygon
call in this codebase's drawing code goes through Tcl - deleting and
recreating dozens of items every animation tick (every canvas, every ~100ms)
is the main cost behind this app's rendering slowness, and is far worse on
Windows where Tk's GDI-backed canvas backend is slower at this than X11/Quartz.

Usage: a frame callback calls begin_frame(), draws through pooled_item() for
each primitive (in the same order every frame), then end_frame() prunes any
leftover items from a frame that drew fewer things than the last one drew.
Draw calls are matched to last frame's items purely by call order: the Nth
pooled_item() call in a frame reuses the Nth item from last frame if it's
still the same shape kind, moving/restyling it in place instead of recreating
it. This means the set of draw calls a callback makes (and their order) must
be the same every frame it draws the same number of things - which holds
naturally here since these callbacks are a straight-line sequence of draws,
not per-item loops over a variable-length dynamic list (variable-length loops,
e.g. one line per data series, are fine too: each iteration is still one
consistent pooled_item() call site reusing its own slot every frame).
'''

class PooledCanvasMixin:
    _CREATORS = {
        "line": "create_line",
        "rectangle": "create_rectangle",
        "oval": "create_oval",
        "text": "create_text",
        "polygon": "create_polygon",
    }

    def _pool_setup(self):
        self._pool: list[tuple[str, int]] = []
        self._pool_index = 0

    def begin_frame(self):
        self._pool_index = 0

    def end_frame(self):
        # Drew fewer things than last frame (e.g. a toggled-off sprite) -
        # remove whatever's left over past the last item actually touched.
        while len(self._pool) > self._pool_index:
            _, item_id = self._pool.pop()
            self.delete(item_id)

    def pooled_item(self, kind: str, coords, **config) -> int:
        index = self._pool_index
        self._pool_index += 1

        if index < len(self._pool):
            prev_kind, item_id = self._pool[index]
            if prev_kind == kind:
                self.coords(item_id, *coords)
                self.itemconfigure(item_id, **config)
                return item_id
            self.delete(item_id)

        creator = getattr(self, self._CREATORS[kind])
        item_id = creator(*coords, **config)

        if index < len(self._pool):
            # This slot's kind changed from last frame (e.g. a conditional
            # branch drew a different shape here) - the fresh item lands on
            # top of the whole canvas by default, so drop it back below
            # whatever the next pooled item is to keep draw order correct.
            if index + 1 < len(self._pool):
                self.tag_lower(item_id, self._pool[index + 1][1])
            self._pool[index] = (kind, item_id)
        else:
            self._pool.append((kind, item_id))
        return item_id
