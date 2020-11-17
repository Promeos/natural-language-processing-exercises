import unicodedata
import re
import json

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd


def basic_clean(string):
    '''
    
    '''
    # Remove accented characters
    string = unicodedata.normalize('NFKD', string)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    
    # Remove special characters
    cleaned_string = re.sub('[^a-zA-Z0-9]', '', string)\
                               .lower()
    return cleaned_string


def tokenize(string):
    '''
    
    '''
    tokenizer = ToktokTokenizer()
    tokenized_string = tokenizer.tokenize(string, return_str=True)
    return tokenized_string
    
    
def stem(string):
    '''
    
    '''
    ps = PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    stemmed_string = ' '.join(stems)
    return stemmed_string


def lemmatize(string):
    '''
    
    '''
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    lemmatized_string = ' '.join(lemmas)
    return lemmatized_string


def remove_stop_words(string, add_to_stopwords=[], remove_from_stopwords=[]):
    '''
    
    '''
    stopword_list = stopwords.words('english')
    
    # Thank you Faith
    stopword_list = set(stopword_list) - set(remove_from_stopwords)
    stopword_list = stopword_list.union(set(add_to_stopwords))
    
    words = string.split()
    filtered_words = [word for word in words if word not in stopword_list]
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords