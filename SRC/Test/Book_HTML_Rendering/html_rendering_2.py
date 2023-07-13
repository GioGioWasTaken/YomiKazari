from PySide6.QtWidgets import QApplication, QMainWindow, QTextBrowser
import ebooklib
from ebooklib import epub
import html2text


def retrieve_content(epub_path):
    app = QApplication([])
    window = QMainWindow()

    text_browser = QTextBrowser()
    window.setCentralWidget(text_browser)

    book = epub.read_epub(epub_path)

    # Set the font and background color for the QTextBrowser widget
    font = text_browser.font()
    font.setFamily("Noto Sans")
    font.setPointSize(20)
    text_browser.setFont(font)
    text_browser.setStyleSheet("background-color: #222436; color: white;")

    content = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html_content = item.get_content().decode('utf-8')

            # Convert HTML to plain text using html2text
            converter = html2text.HTML2Text()
            converter.protect_links=True
            plain_text = converter.handle(html_content)

            content += plain_text + '\n'

    # Set the content in the QTextBrowser widget
    text_browser.setPlainText(content)

    window.show()
    app.exec()
retrieve_content(r'C:\Users\iyars\Downloads\Bardugo_Leigh_-_Six_of_Crows.epub')
