from gaphor import UML
from gaphor.diagram.general.generalpropertypages import CommentPropertyPage
from gaphor.diagram.tests.fixtures import find


def test_comment_property_page_body(element_factory):
    subject = element_factory.create(UML.Comment)
    property_page = CommentPropertyPage(subject)

    widget = property_page.construct()
    comment = find(widget, "comment")
    comment.get_buffer().set_text("test")

    assert subject.body == "test"


def test_comment_property_page_update_text(element_factory):
    subject = element_factory.create(UML.Comment)
    property_page = CommentPropertyPage(subject)

    widget = property_page.construct()
    comment = find(widget, "comment")
    subject.body = "test"
    buffer = comment.get_buffer()

    assert (
        buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False) == "test"
    )
