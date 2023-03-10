import nltk
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
from nltk import FreqDist

from utils import *
from burstiness import *

msg = ""

def get_perplexity(text):
    train_sentences = [get_answer(text)]

    tokenized_text = [list(map(str.lower, nltk.tokenize.word_tokenize(sent))) 
                    for sent in train_sentences]
    n = 1
    train_data, padded_vocab = padded_everygram_pipeline(n, tokenized_text)
    model = MLE(n)
    model.fit(train_data, padded_vocab)

    test_sentences = [text]
    tokenized_text = [list(map(str.lower, nltk.tokenize.word_tokenize(sent))) 
                    for sent in test_sentences]

    test_data, _ = padded_everygram_pipeline(n, tokenized_text)

    for i, test in enumerate(test_data):
        n = float(model.perplexity(test))

        try:
            if n != float('inf'):
                score = n / get_burstiness(text)
                global msg
                if score < 51:
                    msg = ("Your text is more likely to be generate by an AI since your score was: {0}".format(100 - (score / 2)))
                else:
                    msg = ("Your text is more likely to be generate by a human since your score was: {0}".format((score / 2)))
            else:
                get_perplexity(text)
        except:
            get_perplexity(text)

def return_msg():
    return msg
