from nltk.corpus import wordnet

word = 'Ate'
synsets = wordnet.synsets(word)

for synset in synsets:
    print('Word:', synset.name())
    print('Definition:', synset.definition())
    print('Examples:', synset.examples())
    print()
