import sys
import urlparse

from resources.lib.controllers import TmdbController, MovieController, MainController, TvShowController
from resources.lib import kodiutilsitem 

def route(urls, mode, kwargs):
	"""
	in questo modo chiamo il controller che gli ho assegnato
	passandogli pure gli eventuali parametri richiesti
	"""
	if mode is None:
		kodiutilsitem.create_menu()
	else:
		for url_dict in urls:
			if mode in url_dict:
				url_dict[mode](*kwargs)





if __name__ == '__main__':
	"""
	TODO: TROVARE UN MODO PER GESTIRE LO SCAMBIO DEI VALORI (args e addon_handler)
	"""
	
	base_url = sys.argv[0]
	addon_handle = int(sys.argv[1])
	args = urlparse.parse_qs(sys.argv[2][1:])
	mode = args.get('mode', None)
 	#prende tutti i valori degli argomenti eccetto il mode
	kwargs = [args[arg][0] for arg in args if arg != 'mode']

	URL_LIST = [
		#on menu item click
		{'menu/fpt/keyword': MovieController.fpt_exact_name},
		{'menu/movies/keyword': TmdbController.movie_by_keyword},
		{'menu/movies/most_popular': TmdbController.most_popular_movies},
		{'menu/movies/most_voted': TmdbController.most_voted_movies},
		{'menu/movies/now_playing': TmdbController.now_playing_movies},
		{'menu/tvshow/keyword': TmdbController.tvshow_by_keyword},
		{'menu/tvshow/most_popular': TmdbController.most_popular_tvshow},
		{'menu/tvshow/most_voted': TmdbController.most_voted_tvshow},
		{'menu/tvshow/on_air': TmdbController.on_air_tvshow},

		#movies
		{'movies/selected_scraped_movie': MovieController.fpt_movie},
		{'movies/selected_movie': MovieController.movie_streaming_options},

		#tvshow
		{'tvshow/selected_scraped_tvshow': TvShowController.fpt_tvshow},
		{'tvshow/selected_tvshow': TvShowController.fpt_seasons},
		{'tvshow/selected_season': TvShowController.fpt_episodes},
		{'tvshow/selected_episode': TvShowController.fpt_episodes_streaming_options},

		{'play': MainController.play}
	]

	route(URL_LIST, mode, kwargs)

