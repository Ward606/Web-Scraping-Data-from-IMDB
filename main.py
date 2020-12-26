from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from time import sleep
from random import randint

url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'

html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

titles = []
years = []
times = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []
pages = np.arange(1, 1001, 100)

for page in pages:
    page = requests.get('https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100'+ '&start=' + str(page) + '&ref_=adv_prv')
    soup = BeautifulSoup(page.text, 'lxml')
    Movies_info = soup.find_all('div', class_ = 'lister-item mode-advanced')
    sleep(randint(2, 10))


    for movie_info in Movies_info:
        title = movie_info.find('h3', class_ = 'lister-item-header').a.text
        titles.append(title)
        year = movie_info.h3.find('span', class_  = 'lister-item-year text-muted unbold').text
        years.append(year)
        time = movie_info.p.find('span', class_ = 'runtime').text
        times.append(time)
        imdb_rating = movie_info.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', '')
        imdb_ratings.append(imdb_rating)
        try:
            metascore = movie_info.find('div', class_ = 'inline-block ratings-metascore').span.text.replace(' ','')
            metascores.append(metascore)
        except:
            metascores.append(-1)
        try:
            vote_gross = movie_info.find_all('span', attrs = {"name" : "nv"})
            vote = vote_gross[0].text
            votes.append(vote)
            gross = vote_gross[1].text
            us_gross.append(gross)
        except:
            us_gross.append('-')


movies = pd.DataFrame({
    'Movie' : titles,
    'Year'  : years,
    'Runtime': times,
    'IMDBRatings': imdb_ratings,
    'Metascore Rating': metascores,
    'Votes' : votes,
    'US Gross': us_gross

})

movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['Runtime'] = movies['Runtime'].str.extract('(\d+)').astype(int)
movies['IMDBRatings'] = movies['IMDBRatings'].astype(float)
movies['Metascore Rating'] = movies['Metascore Rating'].astype(int)
movies['Votes'] = movies['Votes'].str.replace(',', '').astype(int)
movies['US Gross'] = movies['US Gross'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['US Gross'] = pd.to_numeric(movies['US Gross'], errors='coerce')

movies.to_csv('movies.csv')



