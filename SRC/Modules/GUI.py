# The GUI for YomiKazari!
import sys
import os
from collections import Counter
from controller import open_file_explorer_epub
from ebook_database import EbookDatabase
from SRC.Modules.e_book_object import eBook
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QScrollArea, QLabel, QButtonGroup,QDialog
from PySide6.QtGui import QFont, QPixmap, Qt, QIcon, QPainter
# get path to resources to load later.
current_file_dir = os.path.dirname(os.path.abspath(__file__))
yomi_kazari_dir = os.path.dirname(os.path.dirname(current_file_dir))
resources=os.path.join(yomi_kazari_dir,'SRC','Resources')

class BookshelfWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 200)
        self.setLayout(QHBoxLayout())  # Set a QVBoxLayout for the bookshelf widget
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(os.path.join(resources, 'woodshelf_model V3.png'))
        painter.drawPixmap(self.rect(), pixmap)





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YomiKazari")
        # GENERAL SETTINGS
        font = QFont("Noto Sans", 20)
        self.setStyleSheet("background-color: #222436;")

        # set up a books attribute for future use.
        ebook_db = EbookDatabase('ebooks.db')
        books = ebook_db.get_books()
        self.books = books



        # Create the top bar widget
        top_bar_widget = QWidget()
        top_bar_layout = QHBoxLayout()

        self.top_bar_widget=top_bar_widget

        # Creating add_book with an icon.
        add_book_widget = QWidget()
        add_book_layout = QVBoxLayout()

        add_book = QPushButton()
        add_book_path = os.path.join(resources,'add_book_asset.png')
        add_book_pixmap = QPixmap(add_book_path)
        add_book.setIcon(add_book_pixmap)
        add_book.setIconSize(add_book_pixmap.size())
        add_book_layout.addWidget(add_book)

        add_book_text = QLabel("Add book")
        add_book_text.setFont(font)
        add_book_layout.addWidget(add_book_text)

        add_book_widget.setLayout(add_book_layout)

        # Modify the text size
        add_book.setFont(font)

        # Modify the icon size
        icon_size = add_book_pixmap.size()
        modified_icon_size = icon_size.scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio)
        add_book.setIconSize(modified_icon_size)


        # Creating add_folder with an icon.
        add_folder_widget = QWidget()
        add_folder_layout = QVBoxLayout()

        add_folder = QPushButton()
        add_folder_path = os.path.join(resources,'folder_asset.png')
        add_folder_pixmap = QPixmap(add_folder_path)
        add_folder.setIcon(add_folder_pixmap)
        add_folder.setIconSize(add_folder_pixmap.size())
        add_folder_layout.addWidget(add_folder)

        add_folder_text = QLabel("Add folder")
        add_folder_text.setFont(font)
        add_folder_layout.addWidget(add_folder_text)

        add_folder_widget.setLayout(add_folder_layout)

        # Modify the text size
        add_folder.setFont(font)

        # Modify the icon size
        icon_size = add_folder_pixmap.size()
        modified_icon_size = icon_size.scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio)
        add_folder.setIconSize(modified_icon_size)

        # Creating export_book with an icon.
        export_book_widget = QWidget()
        export_book_layout = QVBoxLayout()

        export_book = QPushButton()
        export_book_path = os.path.join(resources,'export_book_icon.png')
        export_book_pixmap = QPixmap(export_book_path)
        export_book.setIcon(export_book_pixmap)
        export_book.setIconSize(export_book_pixmap.size())
        export_book_layout.addWidget(export_book)

        export_book_text = QLabel("Export book")
        export_book_text.setFont(font)
        export_book_layout.addWidget(export_book_text)

        export_book_widget.setLayout(export_book_layout)

        # Modify the text size
        export_book.setFont(font)

        # Modify the icon size
        icon_size = export_book_pixmap.size()
        modified_icon_size = icon_size.scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio)
        export_book.setIconSize(modified_icon_size)

        # Creating export_folder with an icon.
        export_folder_widget = QWidget()
        export_folder_layout = QVBoxLayout()

        export_folder = QPushButton()
        export_folder_path = os.path.join(resources,'export_folder_icon.png')
        export_folder_pixmap = QPixmap(export_folder_path)
        export_folder.setIcon(export_folder_pixmap)
        export_folder.setIconSize(export_folder_pixmap.size())
        export_folder_layout.addWidget(export_folder)

        export_folder_text = QLabel("Export folder")
        export_folder_text.setFont(font)
        export_folder_layout.addWidget(export_folder_text)

        export_folder_widget.setLayout(export_folder_layout)

        # Modify the text size
        export_folder_widget.setFont(font)

        # Modify the icon size
        icon_size = export_folder_pixmap.size()
        modified_icon_size = icon_size.scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio)
        export_folder.setIconSize(modified_icon_size)

        # Create a search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Enter Book or author name")
        search_bar.setObjectName("searchBar")
        search_bar.setStyleSheet('font-size: 30px;')

        top_bar_layout.addWidget(add_book_widget)
        top_bar_layout.addWidget(add_folder_widget)
        top_bar_layout.addWidget(export_book_widget)
        top_bar_layout.addWidget(export_folder_widget)
        top_bar_layout.addWidget(search_bar)
        top_bar_widget.setLayout(top_bar_layout)

        # Create the main content area widget
        main_content_widget = QWidget()
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins
        main_content_widget.setLayout(main_content_layout)

        # Create the scroll area widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize the widget
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")  # Set transparent background and no border
        self.scroll_area=scroll_area

        covers_layout=QHBoxLayout() # create a layout for the cover grid
        covers_widget=QWidget()
        covers_widget.setLayout(covers_layout)



        # Add the top bar widget and the scroll area to the main content layout
        main_content_layout.addWidget(top_bar_widget)
        main_content_layout.addWidget(scroll_area)
        main_content_layout.addWidget(covers_widget)
        # Set the font and color for the main content widget
        main_content_widget.setFont(font)
        main_content_widget.setStyleSheet("color: white;")

        # Create a button group
        button_group = QButtonGroup()
        button_group.setExclusive( True )
        self.button_group=button_group
        # Add the covers upon init.
        covers_layout = self.display_books_bookshelf(button_group )
        covers_widget.setLayout( covers_layout )
        main_content_widget.layout().update()

        # Set the main content widget as the central widget of the QMainWindow
        self.setCentralWidget(main_content_widget)

        # Add button functionality:

        add_book.clicked.connect( open_file_explorer_epub )
        add_book.clicked.connect( lambda: self.display_books_bookshelf(button_group) )
        covers_widget.setLayout( covers_layout )
        main_content_widget.layout().update()
    def display_books_bookshelf(self,button_group):

        # Read from the current database file
        ebook_db = EbookDatabase('ebooks.db')
        books = ebook_db.get_books()

        # Create a list of all authors
        authors = [book.author for book in books]

        # Create author bookshelves and count the number of books per author
        author_counts = Counter(authors)
        unique_authors = list(author_counts.keys())

        # Create bookshelves for each unique author
        bookshelves = self.create_author_bookshelves(unique_authors)

        # Iterate over the books and add book covers to the corresponding author bookshelf
        for book in books:
            author = book.author
            book_cover_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(book.cover)
            book_cover_label.setPixmap(pixmap)
            book_cover_label.setScaledContents(True)
            book_cover_label.setFixedSize(150, 200)

            # Find the corresponding bookshelf for the author
            bookshelf_layout = bookshelves[author]

            # Create a button for the book cover
            cover_button = QPushButton()
            cover_button.setStyleSheet("background-color: transparent; border: none;")
            cover_button.setIcon(QIcon(pixmap))
            cover_button.setIconSize(book_cover_label.size())
            cover_button.setFixedSize(150, 200)

            # Add the book cover button to the bookshelf widget
            bookshelf_widget = bookshelf_layout.itemAt(0).widget()
            bookshelf_widget.layout().addWidget(cover_button)
            button_group.addButton(cover_button)
            # Connect the buttonClicked signal to the handle_button_selection method
            button_group.buttonClicked.connect(self.handle_button_selection)

        # Add the bookshelves to the covers layout
        covers_layout = QVBoxLayout()
        for bookshelf_layout in bookshelves.values():
            covers_layout.addLayout(bookshelf_layout)

        # Create a widget to hold the covers layout
        covers_widget = QWidget()
        covers_widget.setLayout(covers_layout)

        # Set the widget as the scroll area's widget
        self.scroll_area.setWidget(covers_widget)

    def handle_button_selection(self, button):
        # Set the active button's style sheet
        button.setStyleSheet("background-color: transparent; border: 2px solid red;")

        # Reset the style sheet for other buttons
        for other_button in self.button_group.buttons():
            if other_button != button:
                other_button.setStyleSheet("background-color: transparent; border: none;")
    def create_author_bookshelves(self, authors):
        # Create a dictionary to store bookshelves for each author
        bookshelves = {}
        font = QFont("Noto Sans", 15)
        # Create a bookshelf layout for each unique author
        for author in authors:
            bookshelf_layout = QVBoxLayout()
            author_label = QLabel(author)
            author_label.setFont(font)
            # Create a bookshelf widget
            bookshelf_widget = BookshelfWidget()
            bookshelf_layout.addWidget(bookshelf_widget)
            bookshelf_layout.addWidget(author_label)
            # Store the bookshelf layout in the dictionary
            bookshelves[author] = bookshelf_layout

        return bookshelves


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
