import requests
import nltk
from bs4 import BeautifulSoup

syn_count = 5
def get_synonymfreq(word):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(word))
    soup = BeautifulSoup(response.text, 'lxml')
    headers = []
    for header in soup.findAll(class_="ew5makj1"):
        headers.append(f"{header.em.text} {header.strong.text}")
    synonyms = {"Elementary Level": [], "Middle School Level": [], "High School Level": [], "College Level": []}
    print(f"These are all part of speech options: {' '.join([f'{headers.index(x)+1}. {x}' for x in headers])}")
    index = input("Don't understand the given synonyms with pos? Enter the correct number for more synonyms:  ")
    for syns in soup.findAll(class_="e1ccqdb60")[int(index)-1]:
        for syn in syns.findAll(class_="css-1kg1yv8"):
            response2 = requests.get('https://www.dictionary.com/browse/{}'.format(syn.text.strip()))
            soup2 = BeautifulSoup(response2.text, 'lxml')
            if soup2.find(class_="e1d9ace80") is not None:
                level = soup2.find(class_="e1d9ace80").span.span.text[2:]
                synonyms[level].append(syn.text.strip())
    return headers, synonyms


word = input("Enter word to find synonyms: ")
headers,synonyms = get_synonymfreq(word)
print(f"Here are more synonyms of {word}: ")
for level in synonyms.values():
    for syn in level:
        if syn_count == 0:
            break
        print(syn)
        syn_count -= 1

