#Following the principle of separation of concerns, we will place the underlying
# operations of the buttons inside the GUI, in a dedicated module.
from PySide6.QtWidgets import QFileDialog
from ebook_database import EbookDatabase
from SRC.Modules.e_book_object import eBook
# create a function that opens epub files specifically.
# A separate one for folder seraching, will be implemented below.
def open_file_explorer_epub():
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
    file_dialog.setNameFilter("EPUB Files (*.epub)")

    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        # Process the selected files here
        for file_path in selected_files:
            # add to the book database later, for now: testing.
            ebook_db=EbookDatabase('ebooks.db')
            ebook_db.create_table()
            epub_file = eBook(file_path)
            ebook_db.insert_ebook( epub_file )
            print(f"Selected file: {file_path}")
