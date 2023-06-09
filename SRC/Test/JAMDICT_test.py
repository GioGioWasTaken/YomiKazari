# I'm planning on implementing dictionary lookup in my app
# In order to do this, I'm using Jamdict. I will be extracting the definitions
# and then transferring them into designated variables, to be displayed in the GUI.
from jamdict import Jamdict
import re
jam = Jamdict()
def parse_entry(word):
    result = jam.lookup(word) # get entry info using jamdict
    result_text = result.entries[0].text() # get the text
    print( result_text, type( result_text ) ) # print it for cross-checking
    parts = result_text.split(":") # start to parse it, step 1, parts.

    tmp_word = parts[0].strip().replace("(", "").replace(")", "")
    # split the word into the furi part, and the kanji part.
    furi_word = tmp_word.split()[0]
    kanji_word=tmp_word.split()[1]
    # Extract definitions using regular expression pattern
    definitions = re.findall(r'\d+\.\s.+?(?=\s\d+\.|$)', parts[1])
    # this regular expression matches the numeric part, followed by a period, a space, and lazily matches any characters until either a space followed by a numeric part is encountered or the end of the string.
    difference = ''
    # The purpose of the difference variable is to display furigana on top of kanji

    if not (furi_word == kanji_word):
        difference_list = []
        for char in furi_word:
            if char not in kanji_word:
                difference_list.append( char )
        print( difference_list )
        for char in difference_list:
            difference += char

    return furi_word, kanji_word, definitions, difference


furi_word, kanji_word, definitions, difference = parse_entry('食べる')

print(f"Furi Word: {furi_word}")
print(f"Kanji Word: {kanji_word}")
print(f"Definitions: {definitions}")
print(f"Difference: {difference}")