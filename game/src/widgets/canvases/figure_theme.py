from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from shiboken6 import isValid


def follow_theme(style, canvas, axes: list, lines: dict, legend=None):
    '''
    Dresses a matplotlib figure (on its FigureCanvasQTAgg, canvas) in the
    theme, and again after every theme change: see-through, so the card
    it sits on shows (see themes' module docstring), with the theme's
    text, its outline color for the grid and frame, and each line in the
    data color it's mapped to (line -> a theme color name, e.g. "chart_1"
    or "hot" - see themes.DATA_MATERIALS).
    '''
    # The canvas erases itself with its palette before drawing the figure
    palette = canvas.palette()
    palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.transparent)
    canvas.setPalette(palette)
    canvas.setAutoFillBackground(False)
    # matplotlib marks the canvas opaque, so Qt never repaints the card
    # behind it - a see-through figure then piles up over whatever was
    # last painted there (e.g. every frame of a page transition)
    canvas.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
    figure = canvas.figure

    def apply():
        if not isValid(canvas):
            style.signals.changed.disconnect(apply)
            return
        text, muted, grid = style.color("text"), style.color("muted_text"), style.color("border")
        figure.patch.set_alpha(0.0)
        for ax in axes:
            ax.set_facecolor("none")
            ax.title.set_color(text)
            ax.xaxis.label.set_color(muted)
            ax.yaxis.label.set_color(muted)
            ax.tick_params(colors=muted)
            if ax is axes[0]:  # A twin axis (e.g. twinx) shares the first one's grid
                ax.grid(True, color=grid, linewidth=0.6)
            for spine in ax.spines.values():
                spine.set_color(grid)
        for line, name in lines.items():
            line.set_color(style.color(name))
        if legend is not None:
            frame = legend.get_frame()
            frame.set_facecolor(style.color("widget", opaque=True))
            frame.set_edgecolor(grid)
            for label in legend.get_texts():
                label.set_color(text)
        canvas.draw_idle()

    apply()
    style.signals.changed.connect(apply)
