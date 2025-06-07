
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def nl_interpreter(sentence):
    sent = preprocess(sentence)
    return sent

