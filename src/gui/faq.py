from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy
from PyQt6.QtCore import QMargins
import json


class FAQPage(QWidget):

    def __init__(self, parent=None, filepath="res/faq.json"):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Default spacing between every text block
        layout.setSpacing(3)

        # Read questions and answers
        with open(filepath, "r") as f:
            faq = json.loads(f.read())

        # Add questions and answers
        for i, qa in enumerate(faq):
            question = QLabel(f"<b>{qa['Q']}</b>")
            question.setWordWrap(True)
            answer = QLabel(qa['A'])
            answer.setWordWrap(True)
            layout.addWidget(question)
            layout.addWidget(answer)

            # Add extra space after each question and answer block
            layout.addSpacing(15)

        # Add a stretchable space at the end of the layout
        layout.addStretch()

        # Create a content widget out of this that will be scrollable
        content_widget = QWidget()
        content_widget.setLayout(layout)

        # Make QVBoxLayout scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        # Create a layout for the scrollable area
        page_layout = QVBoxLayout(self)
        page_layout.addWidget(scroll_area)
