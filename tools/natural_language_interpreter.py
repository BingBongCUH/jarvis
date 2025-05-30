
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent

def nl_interpreter(sentence):
    sent = preprocess(sentence)
    pattern = 'NP: {<DT>?<JJ>*<NN>}'
    cp = nltk.RegexpParser(pattern)
    cs = cp.parse(sent)
    return cs

sentence = "The quick brown fox jumps over the lazy dog"
print(nl_interpreter(sentence))
