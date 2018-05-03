
import nltk
nltk.download('punkt')
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize

text1 = "It's true that the chicken was the best bamboozler in the known multiverse."
tokens = word_tokenize(text1)
print(tokens)