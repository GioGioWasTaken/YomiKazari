import ebooklib
from ebooklib import epub

from PySide6.QtCore import QUrl
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

class EPUBWebEnginePage(QWebEnginePage):
    def __init__(self, epub_path, profile, parent=None):
        super().__init__(profile, parent)
        self.epub_path = epub_path

    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        # Intercept the navigation request
        if url.scheme() == 'epub':
            # Handle internal EPUB links
            content_id = url.path().removeprefix('/')
            content_url = QUrl.fromLocalFile(self.epub_path).resolved(QUrl(content_id))
            self.load(content_url)
            return False

        return super().acceptNavigationRequest(url, navigation_type, is_main_frame)


def retrieve_content(epub_path):
    app = QApplication([])
    window = QMainWindow()

    web_view = QWebEngineView()
    window.setCentralWidget(web_view)

    profile = QWebEngineProfile.defaultProfile()
    page = EPUBWebEnginePage(epub_path, profile, web_view)
    web_view.setPage(page)

    book = epub.read_epub(epub_path)

    # Set the font and background color for the HTML content
    font = QFont("Noto Sans", 20)
    html_style = f'''
        <style>
            body {{
                font-family: {font.family()};
                font-size: {font.pointSize()}pt;
            }}
            body, html {{
                background-color: #222436;
                color: white;
            }}
        </style>
    '''

    content = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html_content = item.get_content().decode('utf-8')
            content += html_content

    # Combine the HTML style and content
    final_html = html_style + content
    print(content)
    # Load the modified HTML into the web view
    web_view.setHtml(final_html, QUrl('epub:///'))

    window.show()
    app.exec()



retrieve_content(r'C:\Users\iyars\Downloads\三日間の幸福 (メディアワークス文庫) (三秋 縋 [縋, 三秋]) (z-lib.org).epub')
