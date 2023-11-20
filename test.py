"""
use a list to create a dict of keys eing the  lenght of each strin

"""
words = [
    "abandon",
    "ability",
    "absence",
    "absolute",
    "abstract",
    "abundance",
    "academic",
    "accelerate",
]

query = ['baadnon', 'baility', 'basnece', 'baelsute', 'barstact', 'badnanceu', 'aademicc', 'aacceelrrt']
length = {}

for q in words:
    sort = ''.join(sorted(q))
    length[sort] = q

anagrams = []
for w in query:
    sort = ''.join(sorted(w))
    word = length.get(sort, None)


    while True:
        word = length.get(sort, None)
        if word:
            del length[sort]
        else:
            break

    anagrams.append({word: w})

print(anagrams)
anagrams = []