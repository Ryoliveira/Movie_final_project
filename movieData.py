import omdb
import requests
from bs4 import BeautifulSoup as BS

'''
Technical Movie Options below:
actors, awards, box_office, country, dvd,
director, genre, language, metascore, plot,
poster, production, rated, released, response,
runtime, title, type, website, writer, year,
imdb_id, imdb_rating, imdb_votes

example: movie.movie_technical_info['actors']
'''

API_KEY = 'fc03d7c8'  # API Access Key
omdb.set_default('apikey', API_KEY)


class MovieData:
    def __init__(self, movie_title, fullplot=False,
                 load_all_data=False):  # full plot and load_all_data False by default
        self.movie_technical_info = omdb.get(title=movie_title, fullplot=fullplot, tomatoes=False)
        self.imdb_id = self.movie_technical_info['imdb_id']
        self.trivia = []
        self.goofs = []
        self.quotes = []
        self.crazy_credits = []
        if load_all_data:  # if true, loads all data for current movie
            self.get_trivia()
            self.get_goofs()
            self.get_quotes()
            self.get_crazy_credits()

    def get_trivia(self):
        # Grabs trivia about movie, stores as list
        trivia_page = requests.get('http://www.imdb.com/title/' + self.imdb_id + '/trivia/?ref_=tt_trv_trv')
        trivia_soup = BS(trivia_page.content, 'lxml')
        trivia_data = trivia_soup.find(id='trivia_content')
        self.trivia = [trivia_fact.get_text().lstrip() for trivia_fact in
                       trivia_data.find_all('div', class_="sodatext")]

    def get_goofs(self):
        # Grabs goofs about movie, stores as list
        goof_page = requests.get('http://www.imdb.com/title/' + self.imdb_id + '/goofs/?ref_=tt_trv_trv')
        goof_soup = BS(goof_page.content, 'lxml')
        goof_data = goof_soup.find(id='goofs_content')
        self.goofs = [goof_fact.get_text().lstrip() for goof_fact in goof_data.find_all('div', class_="sodatext")]

    def get_quotes(self):
        # # Grabs quotes from movie, stores as list
        quotes_page = requests.get('http://www.imdb.com/title/' + self.imdb_id + '/quotes/?ref_=tt_trv_trv')
        quotes_soup = BS(quotes_page.content, 'lxml')
        quotes_data = quotes_soup.find(id='quotes_content')
        self.quotes = [quote.get_text().lstrip() for quote in quotes_data.find_all('div', class_="sodatext")]

    def get_crazy_credits(self):
        # Grabs crazy credits about movie, stores as list
        crazycredits_page = requests.get('http://www.imdb.com/title/' + self.imdb_id + '/crazycredits/?ref_=tt_trv_trv')
        crazycredits_page_soup = BS(crazycredits_page.content, 'lxml')
        crazycredits_page_data = crazycredits_page_soup.find(id='crazycredits_content')
        self.crazy_credits = [crazycredits.get_text().lstrip() for crazycredits in
                              crazycredits_page_data.find_all('div', class_="sodatext")]
