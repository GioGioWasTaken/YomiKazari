#THIS CODE IS NOT MINE. ALL CREDIT GOES TO  https://github.com/aditeyabaral , for creating the pydictionary script.
import sys
from nltk.corpus import wordnet
from spellchecker.spellchecker import SpellChecker
dictionary=SpellChecker()

def getWordCLI():
    try:
        return sys.argv[1]
    except IndexError:
        return "ERROR: Bad input. You must provide a word!"

def checkWord(word):
    """
    Check if word exists in the dictionary.
    If not, it will try to make suggestions.
    """
    if bool(wordnet.synsets(word)):
        return word

    suggestions = []
    candidates = dictionary.candidates(word)
    if candidates:
        candidates = [w for w in candidates if wordnet.synsets(w)]
    if candidates:
        suggestions.append(f"The word might have been misspelled. Perhaps the word is: {candidates[0]}?")
        if len(candidates) > 1:
            suggestions.append("Other possibilities include: " + ", ".join(candidates[1:]))
        return "\n".join(suggestions)
    else:
        return "Word not found."

def getRecords(word):
    """Search a word in the dictionary and return its coincidences"""
    word = checkWord(word)
    syn = wordnet.synsets(word)
    dform = {
        "n": "noun",
        "v": "verb",
        "a": "adjective",
        "r": "adverb",
        "s": "adjective satellite",
    }
    output = []
    ctr1 = 1
    ctr2 = 97
    antonyms = []
    for i in syn[:5]:
        ctr2 = 97
        definition, examples, form = i.definition(), i.examples(), i.pos()
        output.append(str(ctr1) + ". " + dform[form] + " - " + word)
        output.append("Definition: " + definition.capitalize() + ".")
        ctr1 += 1
        if len(examples) > 0:
            output.append("Usage:")
            for j in examples:
                output.append(chr(ctr2) + ". " + j.capitalize() + ".")
                ctr2 += 1
        output.append("")
        for j in i.lemmas():
            try:
                antonyms.append(j.antonyms()[0].name())
            except IndexError:
                pass
    if len(antonyms) > 0:
        output.append("Antonyms:")
        output.append(",".join(antonyms))
    return "\n".join(output)



if __name__ == "__main__":
    #word = getWordCLI()
    getRecords("Hate")
