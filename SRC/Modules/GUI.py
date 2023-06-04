import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QScrollArea, QLabel
from PySide6.QtGui import QFont, QPixmap, QPalette, QColor, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YomiKazari")
        # GENERAL SETTINGS
        font = QFont("Noto Sans", 20)
        self.setStyleSheet("background-color: #222436;")

        # Create the top bar widget
        top_bar_widget = QWidget()
        top_bar_layout = QHBoxLayout()

        # Creating add_book with an icon.
        add_book_widget = QWidget()
        add_book_layout = QVBoxLayout()

        add_book = QPushButton()
        add_book_path = r"C:\Users\USER1\PycharmProjects\YomiKazari\SRC\Resources\add_book_asset.png"
        add_book_pixmap = QPixmap(add_book_path)
        add_book.setIcon(add_book_pixmap)
        add_book.setIconSize(add_book_pixmap.size())
        add_book_layout.addWidget(add_book)

        add_book_text = QLabel("Add book")
        add_book_text.setFont(font)
        add_book_text.setAlignment(Qt.AlignCenter)
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
        add_folder_path = r"C:\Users\USER1\PycharmProjects\YomiKazari\SRC\Resources\folder_asset.png"
        add_folder_pixmap = QPixmap(add_folder_path)
        add_folder.setIcon(add_folder_pixmap)
        add_folder.setIconSize(add_folder_pixmap.size())
        add_folder_layout.addWidget(add_folder)

        add_folder_text = QLabel("Add folder")
        add_folder_text.setFont(font)
        add_folder_text.setAlignment(Qt.AlignCenter)
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
        export_book_path = r"C:\Users\USER1\PycharmProjects\YomiKazari\SRC\Resources\export_book_icon.png"
        export_book_pixmap = QPixmap(export_book_path)
        export_book.setIcon(export_book_pixmap)
        export_book.setIconSize(export_book_pixmap.size())
        export_book_layout.addWidget(export_book)

        export_book_text = QLabel("Export book")
        export_book_text.setFont(font)
        export_book_text.setAlignment(Qt.AlignCenter)
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
        export_folder_path = r"C:\Users\USER1\PycharmProjects\YomiKazari\SRC\Resources\export_folder_icon.png"
        export_folder_pixmap = QPixmap(export_folder_path)
        export_folder.setIcon(export_folder_pixmap)
        export_folder.setIconSize(export_folder_pixmap.size())
        export_folder_layout.addWidget(export_folder)

        export_folder_text = QLabel("Export folder")
        export_folder_text.setFont(font)
        export_folder_text.setAlignment(Qt.AlignCenter)
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
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Show vertical scroll bar
        scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize the widget
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")  # Set transparent background and no border

        # Create the container widget for bookshelves
        bookshelves_widget = QWidget()
        bookshelves_layout = QVBoxLayout()
        bookshelves_layout.setSpacing(30)
        bookshelves_layout.setContentsMargins(0, 0, 0, 0)  # Remove any margins
        bookshelves_widget.setLayout(bookshelves_layout)

        # Add bookshelves to the container widget
        authors_amount = 10  # each bookshelf will correspond to an author. If there are 10 authors, there'll be 10 bookshelves
        for _ in range(authors_amount):
            bookshelf_image = QLabel()
            bookshelf_path = r"C:\Users\USER1\PycharmProjects\YomiKazari\SRC\Resources\woodshelf_model V3.png"
            pixmap = QPixmap(bookshelf_path)
            bookshelf_image.setPixmap(pixmap)
            bookshelves_layout.addWidget(bookshelf_image)

        # Set the container widget as the content of the scroll area
        scroll_area.setWidget(bookshelves_widget)

        # Add the top bar widget and the scroll area to the main content layout
        main_content_layout.addWidget(top_bar_widget)
        main_content_layout.addWidget(scroll_area)

        # Set the font and color for the main content widget
        main_content_widget.setFont(font)
        main_content_widget.setStyleSheet("color: white;")

        # Set the main content widget as the central widget of the QMainWindow
        self.setCentralWidget(main_content_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
