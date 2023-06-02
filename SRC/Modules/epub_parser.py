# This module will handle the parsing and processing of EPUB files.
# It will be responsible for extracting metadata,
# retrieving book content, and providing necessary information to other parts of the application.
import ebooklib
from ebooklib import epub
from PIL import Image
import io
from bs4 import BeautifulSoup
class EPUBParser: # Make a class, in order to keep OOP convetions.
    def __init__(self, epub_path):
        self.epub_path = epub_path

    def extract_metadata(self):
        book = epub.read_epub(self.epub_path) # book object represents the .epub file and provides
        # access to its contents and metadata.
        metadata = {
            'title': book.title,
            'authors': book.get_metadata('DC', 'creator')[0][0],
            'publication_date': book.get_metadata('DC', 'date')[0][0],
            'cover_image': self._get_cover_image(book) # a method described below
            # Add more metadata attributes as needed
        }
        return metadata

    def retrieve_content(self):
        book = epub.read_epub(self.epub_path)
        content = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text()
                content += text + '\n'
        return content

    def _get_cover_image(self, book):
        book = epub.read_epub(self.epub_path)
        cover_image = None
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_COVER: # if a cover is provided in the metadata, we will take it.
                cover_image = item.get_content()
                break
            elif item.get_type() == ebooklib.ITEM_IMAGE and not cover_image: # We will take the first image, assuming there's no cover.
                cover_image = item.get_content()
                print(f"item content: {item.get_content}")
                break
        if cover_image:
            image = Image.open(io.BytesIO(cover_image))
            image.save('cover.jpg')
            return 'cover.jpg'
        else:
            return None # if there is no image at all, we will return None.
            # Note for later: I can add a None functionality,
            # that changes all cover-less books to have some set "None" cover, like a blank page.


# Example usage
epub_file = r'C:\Users\USER1\Downloads\Bardugo_Leigh-_Crooked_Kingdom_Six_of_Crows_2.epub'
parser = EPUBParser(epub_file)

metadata = parser.extract_metadata()
print(f'Metadata: {metadata}')

content = parser.retrieve_content()
print(f'Content: {content}')

#TESTING SUCCESSFUL!