from resources.lib import kodiutilsitem
from resources.lib import MovieDb

NEXT_PAGE = "Next Page --->"
tmdb = MovieDb.MovieDb()

def show_moviedb_results(results, media_type, tmdb_type, page=1, keyword=None):
    """
    Show movies or tv shows got from the themoviedb api request.
    
    :param results: list of dictionaries representing themoviedb api request's results
    :param media_type: str
    :param tmdb_type: str represent movie or tv show type
    :param page: int
    :param keyword: str, optional represent user keyboard input
    """
    is_folder = True
    for media in results:
        item_url = {
            'mode': media_type,
            'title': media["titolo"].encode("utf-8"),
            'year': media["anno"],
            }
        
        item_title = media["titolo"].encode("utf-8")

        item_arts = {
            'thumb': tmdb.MOVIEDB_IMAGE_URL.format('500', media["poster"]),
            'fanart': tmdb.MOVIEDB_IMAGE_URL.format('500', media["poster"])
            }
        
        item_info = {'title': media["titolo"].encode('utf-8'),
                    'plot': media["trama"].encode('utf-8'),
                    'year': media["anno"],
                    'mediatype': 'movie'
                    }
        
        kodiutilsitem.add_item(url_dict=item_url, title=item_title, is_folder=is_folder,
                info=item_info, arts=item_arts)
        

    kodiutilsitem.add_menu_item({
        'mode' : 'next',
        'page': page,
        'media_type' : media_type,
        'tmdb_type': tmdb_type,
        'keyword': keyword
        }, NEXT_PAGE)

    kodiutilsitem.end_directory()
