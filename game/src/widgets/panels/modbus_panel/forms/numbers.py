from PySide6.QtCore import Qt

# Spreadsheet-style column alignment: text reads from the left, numbers
# from the right so their decimal points line up
TEXT_ALIGNMENT = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
NUMBER_ALIGNMENT = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

# Blanks as wide as a digit and as a decimal point in the same font - plain
# spaces aren't, and the theme's font may not be monospace
FIGURE_SPACE = " "
POINT_SPACE = " "


def format_number(value: float, decimals: int = 2) -> str:
    value = round(value, decimals)
    if value == 0:
        value = 0.00
    return f"{value:.{decimals}f}".rstrip("0").rstrip(".")


def fraction_width(text: str) -> int:
    '''How many characters text has from its decimal point on (0 if none).'''
    point = text.find(".")
    return 0 if point < 0 else len(text) - point


def align_decimals(texts: list[str]) -> list[str]:
    '''
    Pads each of a column's right-aligned numbers out to the longest
    fraction among them, so their decimal points line up. Placeholders like
    "-" line up as whole numbers; anything else that isn't a number (e.g.
    an error) is left as it is.
    '''
    def is_number(text: str) -> bool:
        try:
            float(text)
            return True
        except ValueError:
            return text == "-"

    width = max((fraction_width(text) for text in texts if is_number(text)), default=0)
    aligned = []
    for text in texts:
        missing = width - fraction_width(text)
        if not is_number(text) or missing == 0:
            aligned.append(text)
        elif "." in text:
            aligned.append(text + FIGURE_SPACE * missing)
        else:
            aligned.append(text + POINT_SPACE + FIGURE_SPACE * (missing - 1))
    return aligned
