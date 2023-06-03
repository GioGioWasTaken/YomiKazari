from SRC.Modules.e_book_object import eBook
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
                    cover_image BLOB
                )
            '''
            cursor.execute(ebooks_database)
            conn.commit()

    def insert_ebook(self, ebook):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()

            sql = '''
                INSERT INTO ebooks (title, author, publication_date, content, cover_image)
                VALUES (?, ?, ?, ?, ?)
            '''
            values = (ebook.title, ebook.author, ebook.date, ebook.content, ebook.cover)
            try:
                cursor.execute(sql, values)
                conn.commit()
            except sqlite3.InterfaceError: # temporary code to handle metadata exceptions
                print("Exception detected: an error with one of the metadata attributes has most likely occurred.")
                values = (str(ebook.title), str(ebook.author), str(ebook.date), ebook.content, ebook.cover)
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


# Example usage
if __name__ == '__main__':
    ebook_db = EbookDatabase('ebooks.db')
    ebook_db.create_table()
    epub_file = eBook(r'path_to_epub')# Insert the path to your EPUB file
    ebook_db.insert_ebook(epub_file)
