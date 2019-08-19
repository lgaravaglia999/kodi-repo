import sys
import re
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from FPTScraper import FPTScraper

import scraper_lib

class Movies(FPTScraper):

    def __init__(self, release_date=None):
        if sys.version_info[0] < 3:
            super(Movies, self).__init__(release_date)
        else:
            super().__init__(release_date)
        self.replacing_chars = ["\n", ";", " "]
        
    def get_result_from_fpt(self, keyword):
        return self.get_fpt_posts(keyword)
    
    def scrape(self, fpt_movie_url):
        self.soup = scraper_lib.get_page_soup(fpt_movie_url)
        self.movie_container = self.get_movie_container()
    
    def get_movie_container(self):
        return scraper_lib.Container(block=self.soup, tag='div', container_id="info",
            container_class="pad").get_container()[-1]
    
    def get_movies_url(self):
        movies_url = scraper_lib.get_hrefs(self.movie_container, self.streaming_to_scrape)
        return movies_url

if __name__ == "__main__":
    # movie = Movies()
    # direct_url = movie.get_by_exact_name('it 2017')
    # movie.scrape(direct_url)
    # movie_urls = movie.get_movies_url()
    # print(movie_urls)
    # res = movie.get_result_from_fpt('alita')
    # url = res[1]["url"]

    # movie.scrape(url)
    # movie_urls = movie.get_movies_url()
    # print(movie_urls)