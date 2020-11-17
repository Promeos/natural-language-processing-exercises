import unicodedata
import re
import json

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd


def basic_clean(string):
    '''
    This function accepts a string and return a normalized string.
    
    parameters
    ----------
    string : str
        A string to be normalized for natural language processing
    
    returns
    -------
    cleaned_string : str
        A lower-cased string encoded to ASCII and decoded to UTF-8.
    '''
    # Remove accented characters
    string = unicodedata.normalize('NFKD', string.lower())\
            .encode('ascii', 'ignore')\
            .decode('utf-8', 'ignore')
    
    # Remove special characters == Include only alpha-numeric characters
    cleaned_string = re.sub(r'[^a-z0-9\s]', '', string)
    return cleaned_string


def tokenize(string):
    '''
    This function accepts a string and returns a tokenized form of the string
    
    parameters
    ----------
    string : str
        A string to be tokenized for natural language processing.
        
    returns
    -------
    tokenized_string
    
    returns
    -------
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


def remove_stopwords(string, add_to_stopwords=[], remove_from_stopwords=[]):
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


def prep_article_data(df, column='', add_to_stopwords=[], remove_from_stopwords=[]):
    '''

    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   add_to_stopwords=add_to_stopwords, 
                                   remove_from_stopwords=remove_from_stopwords)
    
    df['stemmed'] = df[column].apply(basic_clean).apply(stem)
    
    df['lemmatized'] = df[column].apply(basic_clean).apply(lemmatize)
    
    return df[['title', column, 'stemmed', 'lemmatized', 'clean']]