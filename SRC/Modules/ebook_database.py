from SRC.Modules.e_book_object import eBook
from SRC.Modules.e_book_object import eBook_in_db
import sqlite3
class EbookDatabase:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()

            ebooks_database = '''
                CREATE TABLE IF NOT EXISTS ebooks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    publication_date TEXT,
                    content TEXT,
                    cover_image TEXT
                )
            '''
            cursor.execute(ebooks_database)
            conn.commit()

    def insert_ebook(self, ebook):
        with sqlite3.connect( self.db_file ) as conn:
            cursor = conn.cursor()

            sql = '''
                INSERT INTO ebooks (title, author, publication_date, content, cover_image)
                VALUES (?, ?, ?, ?, ?)
            '''
            # Read the image file as bytes
            image_data=None # account for cases where no cover is provided.
            if ebook.cover:
                with open( ebook.cover, "rb" ) as image_file:
                    image_data = image_file.read()

            values = (ebook.title, ebook.author, ebook.published, ebook.content, image_data)
            try:
                cursor.execute( sql, values )
                conn.commit()
            except sqlite3.InterfaceError: # temporary code to handle metadata exceptions
                print("Exception detected: an error with one of the metadata attributes has most likely occurred.")
                values = (str(ebook.title), str(ebook.author), str(ebook.published), ebook.content, image_data)
                cursor.execute(sql, values)
                conn.commit()
    def delete_ebook(self, title):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()

            sql = '''
                DELETE FROM ebooks WHERE title = ?
            '''
            cursor.execute(sql, (title,))
            conn.commit()

    def get_books(self):
        books=[]
        # Connect to the database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve the books
        cursor.execute("SELECT * FROM ebooks")
        rows = cursor.fetchall()

        # Iterate over the retrieved rows and create book objects
        for row in rows:
            book = eBook_in_db(row[0], row[1], row[2],row[3],row[4],row[5])
            books.append(book)

        # Close the database connection
        conn.close()

        return books
# Example usage
if __name__ == '__main__':
    ebook_db = EbookDatabase('ebooks.db')
    ebook_db.create_table()
    epub_file = eBook(r'path_to_epub') # Insert the path to your EPUB file
    ebook_db.insert_ebook(epub_file)
