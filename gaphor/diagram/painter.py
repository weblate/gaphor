"""The painter module provides different painters for parts of the diagram.

Painters can be swapped in and out.

Each painter takes care of a layer in the diagram (such as grid, items
and handles).
"""

from __future__ import annotations

from cairo import LINE_JOIN_ROUND

from gaphor.core.modeling.diagram import DrawContext, StyledItem
from gaphor.diagram.selection import Selection


class ItemPainter:
    def __init__(self, selection: Selection | None = None):
        self.selection: Selection = selection or Selection()

    def paint_item(self, item, cairo):
        selection = self.selection
        diagram = item.diagram
        style = diagram.style(StyledItem(item, selection))

        cairo.save()
        try:
            cairo.set_line_join(LINE_JOIN_ROUND)
            cairo.set_source_rgba(*style["color"])
            cairo.transform(item.matrix_i2c.to_cairo())

            item.draw(
                DrawContext(
                    cairo=cairo,
                    style=style,
                    selected=(item in selection.selected_items),
                    focused=(item is selection.focused_item),
                    hovered=(item is selection.hovered_item),
                    dropzone=(item is selection.dropzone_item),
                )
            )

        finally:
            cairo.restore()

    def paint(self, items, cairo):
        """Draw the items."""
        for item in items:
            self.paint_item(item, cairo)
