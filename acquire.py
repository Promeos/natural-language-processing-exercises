import pandas as pd
import os
import time
import json
import sys

sys.path.insert(1, './data/')

from bs4 import BeautifulSoup
from requests import get
from time import time
from time import sleep
from random import randint
from IPython.core.display import clear_output
from warnings import warn


def check_local_cache(file_name):
    '''
    Accepts a filename and checks to see if a local
    cached version of the data exists
    
    Returns endpoint data as a pandas DataFrame if a local cache exists
    Returns False if a local cache does not exist.
    
    Parameters
    ----------
    file_name : str
        
    Returns
    -------
    Return cached file as a pandas DataFrame if : os.path.isfile(file_name) == True
    Return False otherwise
    '''
    if os.path.isfile(file_name):
        f = open(file_name)
        data = json.load(f)
        return data
    else:
        return False


def url_request(url):
    '''
    
    '''
    headers = {"User-Agent": "Codeup Data Science"}
    response = get(url, headers=headers)
    return response
    

def web_scrape_in_progress(requests, response, start_time):
    '''
    
    '''
    if response.status_code != 200:
        warn(f"Request{requests}, Status Code {response.status_code}")
    elapsed_time = time() - start_time
    sleep(randint(1, 2))
    requests += 1
    print(f'Request: {requests}; Frequency: {requests/elapsed_time:.2f} requests/s')
    clear_output(wait=True)
    return requests


def get_blog_articles():
    '''
    This function returns 5 articles from https://codeup.com as list of dictionaries.
    
    Each dictionary has a title, date published, and article.
    '''
    file_name = 'blog_posts.json'
    # Check to see if a local cache of data exists
    cache = check_local_cache(file_name=file_name)
    
    # If a local cache does not exist, scrape the blog posts
    if cache is False:
        # Create a counter and timer to display update messages throughout the query
        requests = 0
        start_time = time()
        
        # Create an empty list to store each article as a dictionary.
        blog_posts = []
        
        # The websites we want to scrape
        blog_urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
                     'https://codeup.com/data-science-myths/',
                     'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
                     'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
                     'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

        for url in blog_urls:
            response = url_request(url=url)
            
            requests = web_scrape_in_progress(requests=requests, response=response, start_time=start_time)
            
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('title').text
            date_published = soup.find('time', itemprop='datePublished').text
            article = soup.find('div', class_='jupiterx-post-content').text

            blog_posts.append({'title': title,
                               'date_published': date_published,
                               'article': article})

        pd.DataFrame(blog_posts).to_json(file_name)
        return blog_posts
    else:
        return cache
    

def get_news_articles():
    '''
    This function returns news articles from https://inshorts.com as a list of dictionaries.
    
    Articles with the topics of business, sports, technology, entertainment are scraped.
    
    Each news article has a title, content, and category.
    '''
    file_name = 'news_articles.json'
    cache = check_local_cache(file_name=file_name)
    
    if cache is False:
        requests = 0
        start_time = time()
        
        collection = []
        news_topics = ['business', 'sports', 'technology', 'entertainment']
        
        for topic in news_topics:
            inshorts_url = f'https://inshorts.com/en/read/{topic}'
            
            response = url_request(inshorts_url)

            requests = web_scrape_in_progress(requests=requests, response=response, start_time=start_time)

            soup = BeautifulSoup(response.text, 'html.parser')
            article_containers = soup.find_all('div', class_='news-card z-depth-1')

            for article in article_containers:
                title = article.find('span', itemprop='headline').text
                content = article.find('div', itemprop='articleBody').text
                
                collection.append({'title': title,
                                   'content': content,
                                   'category': topic})
            pd.DataFrame(collection).to_json(file_name)
        return collection
    else:
        return cache
