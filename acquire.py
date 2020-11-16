import pandas as pd
import os
from bs4 import BeautifulSoup
import time
from requests import get
from time import time
from time import sleep
from random import randint
from IPython.core.display import clear_output


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
        return pd.read_csv(file_name, index_col=False)
    else:
        return False



def get_blog_articles():
    '''
    This function returns 5 articles from https://codeup.com as list of dictionaries.
    
    Each dictionary has a title, date published, and article.
    '''
    file_name = 'blog_posts.csv'
    data = check_local_cache(file_name)
    
    if data != False:
        return data
    
    else:
        requests = 0
        start_time = time()
        blog_posts = []
        headers = {"User-Agent": "Codeup Data Science"}

        blogs= ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
                'https://codeup.com/data-science-myths/',
                'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
                'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
                'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

        for blog in blogs:
            response = get(blog, headers=headers)

            sleep(randint(1,3))
            requests += 1
            elapsed_time = time() - start_time

            print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
            clear_output(wait=True)

            if response.status_code != 200:
                warn(f"Request{topic}, Status Code {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('title').text
            date_published = soup.find('time', itemprop='datePublished').text
            article = soup.find('div', class_='jupiterx-post-content').text

            blog_posts.append({'title': title,
                               'date_published': date_published,
                               'article': article})
            
        pd.DataFrame(blog_posts).to_csv(file_name)
        return blog_posts
    

def get_news_articles():
    '''
    This function returns news articles from https://inshorts.com as a list of dictionaries.
    
    Articles with the topics of business, sports, technology, entertainment are scraped.
    
    Each news article has a title, content, and category.
    '''
    requests = 0 
    file_name = 'news_articles.csv'
    data = check_local_cache(file_name)
    
    if data != False:
        return data
    
    else:
        
        topics = ['business', 'sports', 'technology', 'entertainment']
        collection = []
        start_time = time()

        for topic in topics:
            inshorts_url = f'https://inshorts.com/en/read/{topic}'
            headers = {'User_Agent': 'Promeos'}

            response = get(inshorts_url, headers)

            sleep(randint(1, 3))

            requests += 1
            elapsed_time = time() - start_time
            print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
            clear_output(wait=True)

            if response.status_code != 200:
                warn(f"Request{response}, Status Code {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            article_containers = soup.find_all('div', class_='news-card z-depth-1')

            for article in article_containers:
                title = article.find('span', itemprop='headline').text
                content = article.find('div', itemprop='articleBody').text
                collection.append({'title': title,
                                   'content': content,
                                   'category': topic})
            pd.DataFrame(collection).to_csv(file_name)
    return collection