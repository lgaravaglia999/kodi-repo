from resources.lib.views import MovieView
from resources.lib.scraper.Movies import Movies
from resources.lib import kodiutilsitem

def fpt_movie(title, release):
	movie = Movies()
	posts = movie.get_result_from_fpt(title)
	MovieView.show_fpt_results(posts, 'fpt_movie')

def fpt_exact_name():
	keyword = kodiutilsitem.user_input()
	if keyword is not None:
		movie = Movies()
		direct_url = movie.get_by_exact_name(keyword)
		movie.scrape(direct_url)
		movie_urls = movie.get_movies_url()
		movie_title = keyword
		MovieView.show_scraped_url(movie_title, movie_urls)

def movie_streaming_options(title, url):
	movie = Movies()
	movie.scrape(url)
	movie_urls = movie.get_movies_url()
	MovieView.show_scraped_url(title, movie_urls)

