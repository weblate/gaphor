from gaphor.core.modeling.properties import attribute
from gaphor.diagram.presentation import (
    Classified,
    ElementPresentation,
    from_package_str,
    text_name,
)
from gaphor.diagram.shapes import (
    Box,
    JustifyContent,
    Text,
    TextAlign,
    draw_border,
    draw_top_separator,
)
from gaphor.diagram.support import represents
from gaphor.diagram.text import FontStyle
from gaphor.SysML.sysml import InterfaceBlock, ValueType
from gaphor.UML.classes.klass import attributes_compartment, operation_watches
from gaphor.UML.classes.stereotype import stereotype_compartments, stereotype_watches
from gaphor.UML.recipes import stereotypes_str
from gaphor.UML.umlfmt import format_operation, format_property


@represents(InterfaceBlock)
class InterfaceBlockItem(Classified, ElementPresentation[InterfaceBlock]):
    def __init__(self, diagram, id=None):
        super().__init__(diagram, id)

        self.watch("show_stereotypes", self.update_shapes).watch(
            "show_parts", self.update_shapes
        ).watch("show_references", self.update_shapes).watch(
            "show_values", self.update_shapes
        ).watch("show_operations", self.update_shapes).watch(
            "subject[NamedElement].name"
        ).watch("subject[NamedElement].name").watch(
            "subject[NamedElement].namespace.name"
        ).watch("subject[Classifier].isAbstract", self.update_shapes).watch(
            "subject[Class].ownedAttribute.aggregation", self.update_shapes
        )
        operation_watches(self, "Block")
        stereotype_watches(self)

    show_stereotypes: attribute[int] = attribute("show_stereotypes", int)

    show_parts: attribute[int] = attribute("show_parts", int, default=False)

    show_references: attribute[int] = attribute("show_references", int, default=False)

    show_values: attribute[int] = attribute("show_values", int, default=False)

    show_attributes: attribute[int] = attribute("show_attributes", int, default=False)

    show_operations: attribute[int] = attribute("show_operations", int, default=False)

    def additional_stereotypes(self):
        from gaphor.RAAML import raaml

        if isinstance(self.subject, raaml.Situation):
            return [self.diagram.gettext("Situation")]
        elif isinstance(self.subject, raaml.ControlStructure):
            return [self.diagram.gettext("ControlStructure")]
        elif isinstance(self.subject, InterfaceBlock):
            return [self.diagram.gettext("interfaceblock")]
        return ()

    def update_shapes(self, event=None):
        self.shape = Box(
            Box(
                Text(
                    text=lambda: stereotypes_str(
                        self.subject, self.additional_stereotypes()
                    )
                ),
                text_name(self),
                Text(
                    text=lambda: from_package_str(self),
                    style={"font-size": "x-small"},
                ),
                style={
                    "padding": (12, 4, 12, 4),
                    "justify-content": JustifyContent.START,
                },
            ),
            *(
                self.show_references
                and self.subject
                and [
                    self.block_compartment(
                        self.diagram.gettext("references"),
                        lambda a: not a.association and a.aggregation != "composite",
                    )
                ]
                or []
            ),
            *(
                self.show_values
                and self.subject
                and [
                    self.block_compartment(
                        self.diagram.gettext("values"),
                        lambda a: isinstance(a.type, ValueType)
                        and a.aggregation == "composite",
                    )
                ]
                or []
            ),
            *(
                self.show_attributes
                and self.subject
                and [attributes_compartment(self.subject)]
                or []
            ),
            *(
                self.show_operations
                and self.subject
                and [
                    self.operations_compartment(
                        self.diagram.gettext("operations"), self.subject
                    ),
                ]
                or []
            ),
            *(self.show_stereotypes and stereotype_compartments(self.subject) or []),
            style={
                "justify-content": JustifyContent.START,
            },
            draw=draw_border,
        )

    def block_compartment(self, name, predicate):
        # We need to fix the attribute value, since the for loop changes it.
        def lazy_format(attribute):
            return lambda: format_property(attribute) or self.diagram.gettext("unnamed")

        return Box(
            Text(
                text=name,
                style={
                    "padding": (0, 0, 4, 0),
                    "font-size": "x-small",
                    "font-style": FontStyle.ITALIC,
                },
            ),
            *(
                Text(text=lazy_format(attribute), style={"text-align": TextAlign.LEFT})
                for attribute in self.subject.ownedAttribute
                if predicate(attribute)
            ),
            style={
                "padding": (4, 4, 4, 4),
                "min-height": 8,
                "justify-content": JustifyContent.START,
            },
            draw=draw_top_separator,
        )

    def operations_compartment(self, name, predicate):
        def lazy_format(operation):
            return lambda: format_operation(operation) or self.diagram.gettext(
                "unnamed"
            )

        return Box(
            Text(
                text=name,
                style={
                    "padding": (0, 0, 4, 0),
                    "font-size": "x-small",
                    "font-style": FontStyle.ITALIC,
                },
            ),
            *(
                Text(text=lazy_format(operation), style={"text-align": TextAlign.LEFT})
                for operation in self.subject.ownedOperation
            ),
            style={
                "padding": (4, 4, 4, 4),
                "min-height": 8,
                "justify-content": JustifyContent.START,
            },
            draw=draw_top_separator,
        )
