import re
import requests

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


def search_google(keywords):
    search_term = (" OR ".join(keywords)).replace(" ", "+")

    response = requests.get(f"https://www.google.com/search?q={search_term}").text
    return [x for x in re.findall("href=\"/url\?q=(.*?)\"", response) if "google.com" not in x]


def get_body_text(url):
    html = requests.get(url).text.replace("\n", " ")
    text = [re.sub("<.*?>|&#?[0-9a-zA-Z]+;", "", x) for x in re.findall("<p.*?>(.*?)</p>", html)]

    return " ".join(text)

def summarizer(text, compactness=1.1):
    stop_words = set(stopwords.words("english"))
    all_words = word_tokenize(text)
    all_words = [PorterStemmer().stem(word) for word in all_words]

    word_frequency = dict()
    sentences = sent_tokenize(text)
    sentence_value = dict()

    for word in all_words:
        word = word.lower()
        if word in stop_words:
            continue

        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1

    for sentence in sentences:
        for index, word_value in enumerate(word_frequency, start=1):
            if word_value in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += index
                else:
                    sentence_value[sentence] = index

    for sentence in sentence_value:
        sentence_value[sentence] = int(sentence_value[sentence] / len(sentence))

    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]

    average = int(sum_values / len(sentence_value))

    summary = ''
    continuous = True
    for sentence in sentences:
        if sentence in sentence_value and sentence_value[sentence] > (compactness * average):
            summary += (" " if continuous else "\n\n") + sentence
            continuous = True
        else:
            continuous = False

    return summary


def process_keywords(keywords):
    return summarizer("\n\n".join([get_body_text(url) for url in search_google(keywords)]))

if __name__ == "__main__":
    link = "https://en.wikipedia.org/wiki/Magnetohydrodynamics"
    print(summarizer(get_body_text(link)))
