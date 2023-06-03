from SRC.Modules.epub_parser import EPUBParser

class eBook:
    def __init__(self, epub_file):
        parser = EPUBParser(epub_file)
        self.metadata = parser.extract_metadata()
        self.content = parser.retrieve_content()
        self.author=self.metadata.get('authors')
        self.date = self.metadata.get('publication_date')
        self.title = self.metadata.get('title')
        self.cover = self.metadata.get('cover_image')


# Example usage
if __name__ == '__main__':
  epub_file = r''  # Enter the path to the file
  ebook = eBook(epub_file)
  print(f'Metadata: {ebook.metadata}')
  print(f'Content: {ebook.content}')
