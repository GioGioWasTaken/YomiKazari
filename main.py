# YomiKazari - Main File Description:

# This is the main file of the YomiKazari ebook reader application. It serves as the entry point for the program
# execution and orchestrates the various components of the application. The main.py file is responsible for setting
# up the application, defining the control flow, integrating different modules, and executing the application.

# Features of the main.py file include:
# - Application setup and configuration
# - Control flow definition for user interactions and events
# - Integration of modules and packages
# - Execution of the ebook reader application

# As the project progresses, the main.py file will act as a central hub that brings together different
# functionalities and facilitates the smooth operation of the YomiKazari ebook reader.

# Author: GioGioBestCat
# Date: 2.06.2023
from SRC.Modules import ebook_database
from SRC.Modules.e_book_object import eBook

if __name__ == '__main__':
    # Perform any initialization or setup tasks here

    # Create an instance of the EbookDatabase class
    ebook_db = ebook_database.EbookDatabase('ebooks.db')

    # Create the ebooks table if it doesn't exist
    ebook_db.create_table()

    # Insert ebook
    epub_file1 = eBook(r'C:\Users\iyars\PycharmProjects\YomiKazari\SRC\Resources\Bardugo, Leigh - Six of Crows.epub')
    ebook_db.insert_ebook(epub_file1)
    # Delete an ebook
    # ebook_db.delete_ebook('Book Title')



