from resources.lib.views import TmdbView
from resources.lib.MovieDb import MovieDb
from resources.lib import kodiutilsitem

tmdb = MovieDb()
TV_MEDIA_TYPE = 'tvshow'
MOVIE_MEDIA_TYPE = 'movies'

def movie_by_keyword(page=1):
	keyword = kodiutilsitem.user_input()
	if keyword is not None:
		results = tmdb.search_moviesdb(keyword, page)
		TmdbView.show_moviedb_results(results, MOVIE_MEDIA_TYPE, 'keyword', page, keyword)

def tvshow_by_keyword(page=1):
	keyword = kodiutilsitem.user_input()
	if keyword is not None:
		results = tmdb.search_tvseries(keyword, page)
		TmdbView.show_moviedb_results(results, TV_MEDIA_TYPE, 'keyword', page, keyword)

def most_popular_movies(page=1):
	tmdb_type = 'most_popular'
	results = tmdb.get_most_popular_movies(page)
	TmdbView.show_moviedb_results(results, MOVIE_MEDIA_TYPE, tmdb_type, page)

def most_voted_movies(page=1):
	tmdb_type = 'most_voted'
	results = tmdb.get_most_voted_movies(page)
	TmdbView.show_moviedb_results(results, MOVIE_MEDIA_TYPE, tmdb_type, page)

def now_playing_movies(page=1):
	tmdb_type = 'now_playing'
	results = tmdb.get_now_playing_movies(page)
	TmdbView.show_moviedb_results(results, MOVIE_MEDIA_TYPE, tmdb_type, page)

def most_popular_tvshow(page=1):
	tmdb_type = 'most_popular'
	results = tmdb.get_most_popular_tvseries(page)
	TmdbView.show_moviedb_results(results, TV_MEDIA_TYPE, tmdb_type, page)

def most_voted_tvshow(page=1):
	tmdb_type = 'most_voted'
	results = tmdb.get_most_voted_tvseries(page)
	TmdbView.show_moviedb_results(results, TV_MEDIA_TYPE, tmdb_type, page)

def on_air_tvshow(page=1):
	tmdb_type = 'on_air'
	results = tmdb.get_on_air_tvseries(page)
	TmdbView.show_moviedb_results(results, TV_MEDIA_TYPE, tmdb_type, page)
