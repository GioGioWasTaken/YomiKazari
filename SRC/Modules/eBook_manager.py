from epub_parser import EPUBParser
epub_file=r'' # enter the path to the file

parser = EPUBParser(epub_file)
metadata = parser.extract_metadata()
print(f'Metadata: {metadata}')

content = parser.retrieve_content()
print(f'Content: {content}')

class eBook_manager:
    def __init__(self,metadata,content):
        self.metadata=metadata
        self.content=content
