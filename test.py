import nltk
import os
from nltk.corpus import stopwords


comment1 = "hello! $bitcoin - this is . comment with special chars.^%"

removeSpecialChars = comment1.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})

lowerstring = removeSpecialChars.lower().split()

commentfilteroutstopwords = [word for word in lowerstring if word not in stopwords.words('english')]



print(commentfilteroutstopwords)

coin_dictionary = {
    ("bitcoin", "btc", "xbt") : 0,
    ("ethereum", "eth") : 0}


for coin in coin_dictionary:
    if any(ext in commentfilteroutstopwords for ext in coin):
        coin_dictionary[coin] += 1


print(coin_dictionary)

PATH = os.getenv('PATH')

print(PATH)