import re
import requests
import random

import sumy
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


def search_google(keywords):
    arr = [
        re.sub(r"&?amp;.*$", "", x) 
        for x in re.findall(
            "href=\"/url\?q=(.*?)\"", 
            requests.get("https://www.google.com/search?q=%s" % (" ".join(keywords))).text
        ) if "google.com" not in x
    ]
    return arr


def get_body_text(url):
    html = requests.get(url).text.replace("\n", " ")
    html = re.sub("<script.*?>(.*?)</script>", "", html)
    html = re.sub("<nav.*?>(.*?)</nav>", "", html)
    html = re.sub("<header.*?>(.*?)</header>", "", html)
    html = re.sub("<footer.*?>(.*?)</footer>", "", html)
    html = re.sub("<style.*?>(.*?)</style>", "", html)
    html = re.sub("<noscript.*?>(.*?)</noscript>", "", html)
    # html = re.sub("<href.*?>(.*?)</href>", "", html)
    html = re.sub("<a.*?>(.*?)</a>", "", html)
    text = [re.sub("<.*?>|&#?[0-9a-zA-Z]+;", "", x).replace("Read more", "") for x in re.findall("<p.*?>(.*?)</p>", html)]

    return " ".join(text)

def summarizer(text, keywords):

    # stop_words = set(stopwords.words("english"))
    # all_words = word_tokenize(text)
    # all_words = [PorterStemmer().stem(word) for word in all_words]
    #
    # word_frequency = dict()
    # sentences = sent_tokenize(text)
    # sentence_value = dict()
    #
    # for word in all_words:
    #     word = word.lower()
    #     if word in stop_words:
    #         continue
    #
    #     if word in word_frequency:
    #         word_frequency[word] += 1
    #     else:
    #         word_frequency[word] = 1
    #
    # for sentence in sentences:
    #     for index, word_value in enumerate(word_frequency, start=1):
    #         if word_value in sentence.lower():
    #             if sentence in sentence_value:
    #                 sentence_value[sentence] += index
    #             else:
    #                 sentence_value[sentence] = index
    #
    #     for keyword in keywords:
    #         if PorterStemmer().stem(keyword) in sentence:
    #             sentence_value[sentence] += 1000
    #
    # for sentence in sentence_value:
    #     sentence_value[sentence] = sentence_value[sentence] / len(sentence) # + 0.0001 * len(sentence)
    #
    # sum_values = 0
    # for sentence in sentence_value:
    #     sum_values += sentence_value[sentence]
    #
    # average = int(sum_values / len(sentence_value))
    #
    # closest = 999999999999999999
    # compactness2 = 0
    # for compactness in range(10, 20, 1):
    #     summary = ''
    #     continuous = True
    #     for sentence in sentences:
    #         if sentence in sentence_value and sentence_value[sentence] > (compactness/10 * average):
    #             summary += (" " if continuous else "\n\n") + sentence
    #             continuous = True
    #         else:
    #             continuous = False
    #
    #     dist = abs(5000 - len(summary))
    #     closest = min(dist, closest)
    #     if closest == dist: compactness2 = compactness/10
    #
    # summary = [[]]
    # continuous = True
    # for sentence in sentences:
    #     if sentence in sentence_value and sentence_value[sentence] > (compactness2 * average):
    #         if continuous: summary[-1].append(sentence)
    #         else: summary.append([sentence])
    #         continuous = True
    #     else:
    #         continuous = False
    #
    # return " ".join(sorted(summary, key=lambda x: sum([len(y) for y in x]))[-random.randint(1, 5)])

    parser = PlaintextParser.from_string(text, Tokenizer('english'))

    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)
    return " ".join([str(x) for x in summary])


def process_keywords(keywords):
    texts = []
    for url in search_google(keywords)[:4]:
        try:
            texts.append(get_body_text(url))
        except requests.exceptions.ConnectionError:
            continue

    try:
        summaries = [summarizer(x, keywords) for x in texts]
        return [x for x in summaries if len(x) > 5][0]
    except ZeroDivisionError: return "No results found."


if __name__ == "__main__":
    from keybert import KeyBERT
    text = "Eric Cantona tells Cristiano Ronaldo his failure to 'accept that he is NOT 25 any more' - and not helping " \
           "Man United's youngsters in the process - led to his bitter exit, as he likens end of career to 'dying'"
    kw_model = KeyBERT()
    res = [t[0] for t in kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words=None, use_mmr=True, top_n=3)]
    print(process_keywords(res))
