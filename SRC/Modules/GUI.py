# The GUI for YomiKazari!
import sys
import os
from collections import Counter
from controller import open_file_explorer_epub
from ebook_database import EbookDatabase
from functools import partial
from pydictionary_EN import getRecords
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QDialog, QLineEdit, QHBoxLayout, QScrollArea, QLabel, QButtonGroup,QTextBrowser
from PySide6.QtGui import QFont, QPixmap, Qt, QIcon, QPainter, QAction, QContextMenuEvent, QCursor
from PySide6.QtCore import Signal, QSize, Qt

# get path to resources to load later.
current_file_dir = os.path.dirname(os.path.abspath(__file__))
yomi_kazari_dir = os.path.dirname(os.path.dirname(current_file_dir))
resources=os.path.join(yomi_kazari_dir,'SRC','Resources')
ebook_db = EbookDatabase( 'ebooks.db' )

class IconButton(QWidget):
    def __init__(self, icon_path, text,font):
        super().__init__()
        self.layout = QVBoxLayout()

        self.button = QPushButton()
        self.pixmap = QPixmap(icon_path)
        self.button.setIcon(self.pixmap)
        self.button.setIconSize(self.pixmap.size())
        self.layout.addWidget(self.button)
        self.button.setStyleSheet("background-color: transparent; border: none;")

        self.label = QLabel(text)
        self.label.setFont(font)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        self.button.setFont(font)

        icon_size = self.pixmap.size()
        modified_icon_size = icon_size.scaled(100, 100, Qt.AspectRatioMode.IgnoreAspectRatio)
        self.button.setIconSize(modified_icon_size)

class BookPopup(QWidget):
    def create_delete_book_closure(self,book):
        def delete_book_closure():
            ebook_db.delete_ebook( book.title )

        return delete_book_closure

    def __init__(self, book, open_book_func):
        super().__init__()
        self.setWindowTitle("Book Popup")

        # Set the main widget for the popup
        layout = QVBoxLayout(self)
        font = QFont("Noto Sans", 20)
        self.setStyleSheet("background-color: #222436;color: white;")

        #create a dedicated layout & container specifically for the cover & open book button
        container=QWidget()
        layout2=QHBoxLayout()

        # create the open book button
        open_book=QPushButton()
        open_book_path = os.path.join(resources,'arrow_icon64.png')
        open_book_pixmap = QPixmap(open_book_path)
        open_book.setIcon(open_book_pixmap)
        open_book.setIconSize(open_book_pixmap.size())
        open_book.setFixedSize(150,200)
        open_book.setStyleSheet("background-color: transparent; border: none;")

        open_book.clicked.connect( partial( open_book_func, book=book ) ) # partial function to prevent immediate execution

        # create the delete book button
        delete_book = QPushButton()
        delete_book_path = os.path.join( resources, 'trashcan_icon.png' )
        delete_book_pixmap = QPixmap( delete_book_path )
        scaled_pixmap = delete_book_pixmap.scaled( QSize( 112.5, 150 ), Qt.AspectRatioMode.KeepAspectRatio,Qt.SmoothTransformation )
        delete_book.setIcon( QIcon( scaled_pixmap ) )
        delete_book.setIconSize( scaled_pixmap.size() )
        delete_book.setFixedSize( 150, 200 )
        delete_book.setStyleSheet( "background-color: transparent; border: none;" )

        delete_book.clicked.connect( partial( ebook_db.delete_ebook, book.title ) )
        # Create and add the widgets to the layout
        cover_label = QLabel()
        cover_pixmap = QPixmap()
        cover_pixmap.loadFromData(book.cover)  # Assuming book.cover is in bytes
        cover_label.setScaledContents(True)
        cover_label.setPixmap(cover_pixmap)
        cover_label.setFixedSize(150,200)

        layout2.addWidget(cover_label)
        layout2.addWidget(open_book)
        layout2.addWidget(delete_book)
        layout2.setSpacing( 10 )
        layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        container.setLayout(layout2)
        layout.addWidget(container)

        self.delete_book=delete_book # the delete book function will affect the entire books database, so we call it outside this class
        # (so we don't have to import the book database into here)

        # Add other book details like author, publication time, and synopsis to the layout
        book_title=QLabel('Title: '+ book.title)
        book_title.setFont(font)
        layout.addWidget(book_title)

        author_label = QLabel('Author name: '+book.author)
        author_label.setFont(font)
        layout.addWidget(author_label)

        published_label = QLabel('Publication date: '+ book.publication_date)
        published_label.setFont(font)
        layout.addWidget(published_label)


        # the synopsis isn't available in the metadata, and will be acquired in the future using methods like webscraping.
        # Adjust the position and size of the popup
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        desired_width = screen_geometry.width() // 10
        self.setGeometry(screen_geometry.width() - desired_width - 20, 0, desired_width, screen_geometry.height())
        self.show()



class BookshelfWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 200)
        self.setLayout(QHBoxLayout())  # Set a QVBoxLayout for the bookshelf widget
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(os.path.join(resources, 'woodshelf_model V3.png'))
        painter.drawPixmap(self.rect(), pixmap)


class DictionaryPopup(QDialog):
    def __init__(self, word_definition, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dictionary Popup")
        self.setStyleSheet("background-color: #222436;")
        self.setFixedSize(500,300)
        # Create a QTextBrowser to display the word definition
        text_browser = CustomTextBrowser() # made the text win my custom version, so you can look up words even in dictionary definitions.
        text_browser.setPlainText(word_definition)
        text_browser.setStyleSheet("color: white;")
        text_browser.setFont(QFont("Noto Sans", 20))

        # Create a button to close the popup
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Create a vertical layout for the popup
        layout = QVBoxLayout(self)
        layout.addWidget(text_browser)
        layout.addWidget(close_button)

        self.setLayout(layout)



class CustomTextBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        selected_text = self.textCursor().selectedText()
        if selected_text:
            custom_action = QAction( f"Search: {selected_text}", self ) # name the action
            custom_action.triggered.connect( self.customActionTriggered )
            self.selected_word = selected_text  # Store the selected word
            menu.addAction( custom_action )
        mouse_pos=QCursor.pos() # get current mouse position
        menu.exec(mouse_pos)

    def contains_english_text(self, text):
        english_letters = [chr( i ) for i in range( 0x0041, 0x005A + 1 )] + [chr( i ) for i in range( 0x0061, 0x007A + 1 )]
        for char in text:
            if char in english_letters:
                return True
        return False

    def customActionTriggered(self):
        # Access the stored selected word and confirm the language is currently available
        if self.contains_english_text( self.selected_word ):
            dictionary_def = getRecords( self.selected_word )  # call the dictionary function from pydict
            if (dictionary_def==None) or (dictionary_def==''):
                dictionary_def="There's no definition to this word in the database. It is likely either a name, or too common to appear here."
            print(dictionary_def, type(dictionary_def))

            popup_window = DictionaryPopup( dictionary_def )
            popup_window.exec()  # Use exec() for modal behavior

            print("Everything finished loading, supposedly.")
        else:
            popup_window=DictionaryPopup("Support for non-EN text lookup is currently under development.")
            popup_window.exec()


class YomiKazariTextWin(QMainWindow):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{book.title} Text Window")
        print(book.title)
        # GENERAL SETTINGS
        font = QFont("Noto Sans", 20)
        self.setStyleSheet("background-color: #222436;")
        # Create a scrollable area to hold the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to act as a container for the content
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        # Create a vertical layout for the content widget
        layout = QVBoxLayout(content_widget)

        # Create a QTextBrowser for the book content
        content_browser = CustomTextBrowser()
        content_browser.setPlainText(book.content)
        content_browser.setStyleSheet("color: white;")
        content_browser.setFont(font)
        layout.addWidget(content_browser)

        # Set the content widget as the central widget
        self.setCentralWidget(scroll_area)

        # Show the window
        self.showMaximized()

    closed = Signal()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YomiKazari")
        # GENERAL SETTINGS
        font = QFont("Noto Sans", 20)
        self.setStyleSheet("background-color: #222436;")
        win_icon=QIcon(os.path.join(resources,"YomiKazariWinIcon.png"))
        self.setWindowIcon(win_icon)
        # set up a books attribute for future use.
        books = ebook_db.get_books()
        self.books = books
        self.books_database=ebook_db
        self.text_win = None  # Attribute to store the YomiKazariTextWin instance

        # Create the top bar widget
        top_bar_widget = QWidget()
        top_bar_layout = QHBoxLayout()

        self.top_bar_widget=top_bar_widget

        self.book_button_map = {}

        add_book_widget = IconButton(os.path.join(resources, 'add_book_pixel.png'), "Add book", font)
        add_folder_widget = IconButton(os.path.join(resources, 'folder_icon_pixel.png'), "Add folder", font)
        export_book_widget = IconButton(os.path.join(resources, 'export_book_pixel.png'), "Export book", font)
        export_folder_widget = IconButton(os.path.join(resources, 'export_folder_pixel.png'), "Export folder", font)

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



        # Add the top bar widget the scroll area and the covers widget to the main content layout
        main_content_layout.addWidget(top_bar_widget)
        main_content_layout.addWidget(scroll_area)
        main_content_layout.addWidget(covers_widget)
        # Set the font and color for the main content widget
        main_content_widget.setFont(font)
        main_content_widget.setStyleSheet("color: white;")

        self.main_content_layout=main_content_layout

        # Create a button group
        button_group = QButtonGroup()
        button_group.setExclusive( True )
        self.button_group=button_group
        # Add the covers upon init.
        covers_layout = self.display_books_bookshelf(button_group )
        covers_widget.setLayout( covers_layout )
        main_content_widget.layout().update()
        self.main_content_widget=main_content_widget
        # Set the main content widget as the central widget of the QMainWindow
        self.setCentralWidget(main_content_widget)





        # Add button functionality:

        add_book_widget.button.clicked.connect( open_file_explorer_epub )
        add_book_widget.button.clicked.connect( lambda: (print( "Books should have refreshed upon click" ),
                                           setattr( self, 'book_button_map', {} ),
                                           self.active_popup.close() if self.active_popup else None,
                                           setattr( "covers_layout", self.display_books_bookshelf( button_group ) ),
                                           main_content_widget.layout().update(),
                                           covers_widget.setLayout( covers_layout )) ) # I know this is a bit messy, will fix in the future to a proper function.

        self.active_popup = None # init value to keep track of the book description popup.


    def display_books_bookshelf(self,button_group):
        ebook_db = EbookDatabase('ebooks.db')
        books = ebook_db.get_books()
        self.books = books

        # Create a list of all authors
        authors = [book.author for book in self.books]

        # Create author bookshelves and count the number of books per author
        author_counts = Counter(authors)
        unique_authors = list(author_counts.keys())
        titles=[book.title for book in self.books]
        print(titles)
        # Create bookshelves for each unique author
        bookshelves = self.create_author_bookshelves(unique_authors)

        # Iterate over the books and add book covers to the corresponding author bookshelf
        for book in self.books:
            author = book.author
            book_cover_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(book.cover)
            book_cover_label.setPixmap(pixmap)
            book_cover_label.setScaledContents(True)
            book_cover_label.setFixedSize(110, 140)

            # Find the corresponding bookshelf for the author
            bookshelf_layout = bookshelves[author]

            # Create a button for the book cover
            cover_button = QPushButton()
            cover_button.setStyleSheet("background-color: transparent; border: none;")
            cover_button.setIcon(QIcon(pixmap))
            cover_button.setIconSize(book_cover_label.size())
            cover_button.setFixedSize(110, 140)

            # Add the book cover button to the bookshelf widget
            bookshelf_widget = bookshelf_layout.itemAt(1).widget()
            bookshelf_widget.layout().addWidget(cover_button)
            bookshelf_widget.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
            button_group.addButton(cover_button)
            self.book_button_map[cover_button]=book
        # Connect the buttonClicked signal to the handle_button_selection method
        button_group.buttonClicked.connect(self.handle_button_selection)
        print(self.book_button_map)
        # Add the bookshelves to the covers layout
        covers_layout = QVBoxLayout()
        for bookshelf_layout in bookshelves.values():
            covers_layout.addLayout(bookshelf_layout)
        self.covers_layout=covers_layout
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
                other_button.setChecked( False )
        # Close the current book popup if it's open
        if self.active_popup:
            self.active_popup.deleteLater()
        book = self.get_book_from_button(button)
        if book:
            popup = BookPopup(book,self.open_book_handler)
            self.active_popup = popup
            self.main_content_layout.addWidget(popup)

            self.active_popup.delete_book.clicked.connect( lambda: (print( "Books should have refreshed upon click" ),
                                           setattr( self, 'book_button_map', {} ),
                                           self.active_popup.close() if self.active_popup else None,
                                           setattr( "covers_layout", self.display_books_bookshelf( self.button_group ) ),
                                           self.main_content_widget.layout().update()) ) # I know this is a bit messy, will fix in the future to a proper function.



            print(f"Current book title {book.title}")
        self.text_win.closed.connect(lambda: (setattr(self,"text_win",None)))
    def get_book_from_button(self, button):
        # Retrieve the book associated with the button
        print(self.book_button_map)
        print(self.book_button_map.get(button))
        return self.book_button_map.get(button)

    def open_book_handler(self,book):
        self.text_win=YomiKazariTextWin(book)
        self.text_win.show()

    def create_author_bookshelves(self, authors):
        # Create a dictionary to store bookshelves for each author
        bookshelves = {}
        font = QFont("Noto Sans", 15)
        # Create a bookshelf layout for each unique author
        for author in authors:
            # Create a bookshelf layout for each unique author
            bookshelf_layout = QVBoxLayout()
            author_label = QLabel( author )
            author_label.setFont( font )

            # Create a bookshelf widget
            bookshelf_widget = BookshelfWidget()

            # Set the layout for the bookshelf widget
            bookshelf_widget.setLayout( bookshelf_layout )

            bookshelf_layout.addWidget( author_label )
            bookshelf_layout.addWidget( bookshelf_widget )

            # Store the bookshelf layout in the dictionary
            bookshelves[author] = bookshelf_layout

        return bookshelves

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    sys.exit(app.exec())
