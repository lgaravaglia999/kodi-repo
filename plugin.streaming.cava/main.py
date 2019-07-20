# -*- coding: utf-8 -*-
import urlparse
import urlresolver
import sys
from urllib import urlencode
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

from resources.lib.streaming_hosts import speedvideo, openload
from resources.lib.scraper.Movies import Movies
from resources.lib.scraper.TvSeries import TvSeries
from resources.lib.MovieDb import MovieDb

import requests

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

NEXT_PAGE = "Next Page --->"
# addon kicks in
mode = args.get('mode', None)

#init objects for scraping
tmdb = MovieDb()
STREAMING_SOURCES = ["speedvideo", "openload", "rapidcrypt"]

def build_url(query):
    return '{0}?{1}'.format(base_url, urlencode(query))

def play_video(path):
    """
    Play a video by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    encoded_path = path.encode("utf-8")
    play_item = xbmcgui.ListItem(path=encoded_path)
    play_item.setInfo('video', {})
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def resolve_url(url):
    duration=7500   #in milliseconds
    message = "Cannot Play URL"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Resolver Error", message, xbmcgui.NOTIFICATION_INFO, duration)
        return False
    else:        
        return stream_url 

def play_video_with_resolver(path):
    """
    Play a video by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    vid_url = play_item.getfilename()
    stream_url = resolve_url(vid_url)
    if stream_url:
        play_item.setPath(stream_url)
    #Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def user_input():
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('CercaFilm')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        search_term = kb.getText()
        return search_term
    else:
        return None

def get_streaming_source_name(url):
    for source in STREAMING_SOURCES:
        if source in url:
            return source
    return "n.d."

def show_scraped_url(movie_title, movie_urls):
    """
    Show playable items with all streaming options for the selected movie.

    :param movie_title: str
    :param movie_urls: list of strings representing movie url
    """
    is_folder = False
    for movie_url in movie_urls:
        streaming_source = get_streaming_source_name(movie_url)

        item_url = {
            'mode':'play',
            'title': movie_title,
            'streaming_url': movie_url
            }
        
        item_title = "{0} [{1}]".format(movie_title, streaming_source)

        item_property = {"prop_key": 'IsPlayable', "prop_value": 'true'}

        add_item(url_dict=item_url, title=item_title, is_folder=is_folder, properties=item_property)
                
    xbmcplugin.endOfDirectory(addon_handle)

def show_fpt_results(posts_data, media_type):
    """
    Show all movies/tv shows scraped

    :param posts_data: list of dictionaries representing scraped info
    :param media_type: str
    """
    is_folder = True
    for post in posts_data:
        item_url = {
            'mode': media_type,
            'title': post["title"].encode("utf-8"),
            'fpt_movie_url': post["url"]
            }

        item_title = u''.join(post["title"]).encode("utf-8").strip()
      
        item_arts = {
            'thumb': post["image"],
            'fanart': post["image"]
            }

        add_item(url_dict=item_url, title=item_title, is_folder=is_folder, arts=item_arts)
        
    xbmcplugin.endOfDirectory(addon_handle)

def show_tv_seasons(tv_title, fpt_tv_url, tv_seasons_list):
    """
    Show all seasons of the selected tv show.
    
    :param tv_title: str
    :param fpt_tv_url: str
    :param tv_seasons_list: list of seasons name
    """
    is_folder = True
    for i in range(len(tv_seasons_list)):
        item_url = {
            'mode':'season',
            'series_title': tv_title,
            'title': tv_seasons_list[i].encode("utf-8"),
            'page_url': fpt_tv_url,
            'season_no': i
            }
        
        item_title = u''.join(tv_seasons_list[i]).encode("utf-8").strip()

        add_item(url_dict=item_url, title=item_title, is_folder=is_folder)
        
    xbmcplugin.endOfDirectory(addon_handle)

def show_season_episodes(tv_title, episodes):
    """
    Show all episodes of the selected season.
    
    :param tv_title: str
    :param episodes: list of dictionaries representing episodes name and a list of urls
    """
    is_folder = True
    for episode in episodes:
        ep_title = list(episode.keys())[0]
        ep_urls = episode[ep_title]

        item_url = {
            'mode':'episode',
            'title': ep_title.encode("utf-8")
            }
        
        for url in ep_urls:
            name = get_streaming_source_name(url)
            item_url[name] = url

        
        item_title = u"".join(ep_title).encode("utf-8").strip()

        item_property = {"prop_key": 'IsPlayable', "prop_value": 'true'}

        add_item(url_dict=item_url, title=item_title, is_folder=is_folder, properties=item_property)

    xbmcplugin.endOfDirectory(addon_handle)

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
        
        add_item(url_dict=item_url, title=item_title, is_folder=is_folder,
                info=item_info, arts=item_arts)
        

    add_menu_item({
        'mode' : 'next',
        'page': page,
        'media_type' : media_type,
        'tmdb_type': tmdb_type,
        'keyword': keyword
        }, NEXT_PAGE)

    xbmcplugin.endOfDirectory(addon_handle)

def add_menu_item(url_dict, item_title, image='DefaultVideo.png'):
    url = build_url(url_dict)
    li = xbmcgui.ListItem(item_title, iconImage=image)

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                        listitem=li, isFolder=True)

def add_item(url_dict, title, is_folder=False, properties=None, info=None, arts=None):
        url = build_url(url_dict)

        kodi_item = xbmcgui.ListItem(title)
        if arts is not None:
            kodi_item.setArt(arts)
        if info is not None:
            kodi_item.setInfo('video', info)
        else:
            kodi_item.setInfo('video', {})
        if properties is not None:
            prop_key = properties["prop_key"]
            prop_value = properties["prop_value"]
            kodi_item.setProperty(prop_key, prop_value)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                            listitem=kodi_item, isFolder=is_folder)


def get_tmdb_movie_results(tmdb_type, page=1, keyword=None):
    if tmdb_type == "keyword":
        results = tmdb.search_moviesdb(keyword, page)
    elif tmdb_type == "most_popular":
        results = tmdb.get_most_popular_movies(page)
    elif tmdb_type == "most_voted":
        results = tmdb.get_most_voted_movies(page)
    elif tmdb_type == "now_playing":
        results = tmdb.get_now_playing_movies(page)
    else:
        results = None
    
    return results

def get_tmdb_tv_results(tmdb_type, page=1, keyword=None):
    if tmdb_type == "keyword":
        results = tmdb.search_tvseries(keyword, page)
    elif tmdb_type == "most_popular":
        results = tmdb.get_most_popular_tvseries(page)
    elif tmdb_type == "most_voted":
        results = tmdb.get_most_voted_tvseries(page)
    elif tmdb_type == "on_air":
        results = tmdb.get_on_air_tvseries(page)
    else:
        results = None

    return results

def route(mode):
    if mode is None:
        add_menu_item({'mode' : 'menu', 'choice' : 'movies', 'type': 'keyword'}, 'Cerca Film')
        add_menu_item({'mode' : 'menu', 'choice' : 'movies', 'type': 'most_popular'}, 'Cerca tra i film piu popolari')
        add_menu_item({'mode' : 'menu', 'choice' : 'movies', 'type': 'most_voted'}, 'Cerca tra i film piu votati')
        add_menu_item({'mode' : 'menu', 'choice' : 'movies', 'type': 'now_playing'}, 'Cerca tra i film in onda al cinema')

        add_menu_item({'mode' : 'menu', 'choice' : 'tv_series', 'type': 'keyword'}, 'Cerca Serie Tv')
        add_menu_item({'mode' : 'menu', 'choice' : 'tv_series', 'type': 'most_popular'}, 'Cerca tra le Serie Tv piu popolari')
        add_menu_item({'mode' : 'menu', 'choice' : 'tv_series', 'type': 'most_voted'}, 'Cerca tra le Serie Tv piu votate')
        add_menu_item({'mode' : 'menu', 'choice' : 'tv_series', 'type': 'on_air'}, 'Cerca tra Serie Tv ancora in corso')

        xbmcplugin.endOfDirectory(addon_handle)

    elif mode[0] == 'menu':
        choice = args['choice'][0]
        tmdb_type = args['type'][0]
        page = 1
        keyword = None

        if choice == "movies":
            media_type = "tmdb_movie"
            if tmdb_type == "keyword":
                keyword = user_input()
                if keyword is not None:
                    results = get_tmdb_movie_results(tmdb_type, page, keyword)        
            else:
                results = get_tmdb_movie_results(tmdb_type, page)

        else:
            media_type = "tmdb_tv_serie"
            if tmdb_type == "keyword":
                keyword = user_input()
                if keyword is not None:
                    results = get_tmdb_tv_results(tmdb_type, page, keyword)
            else:
                results = get_tmdb_tv_results(tmdb_type, page)
        
        show_moviedb_results(results, media_type, tmdb_type, page, keyword)

    elif mode[0] == 'tmdb_movie':
        tmbd_title = args["title"][0]
        movie_release = args["year"][0]
        media_type = "fpt_movie"

        movie = Movies(release_date=movie_release)
        posts = movie.get_result_from_fpt(tmbd_title)

        show_fpt_results(posts, media_type)

    elif mode[0] == 'fpt_movie':
        fpt_title = args["title"][0]
        fpt_movie_url = args["fpt_movie_url"][0]

        movie = Movies()
        movie.scrape(fpt_movie_url)
        movie_urls = movie.get_movies_url()

        show_scraped_url(fpt_title, movie_urls)

    elif mode[0] == 'tmdb_tv_serie':
        tmdb_tv_title = args["title"][0]
        movie_release = args["year"][0]
        media_type = "fpt_tv"

        tv_series = TvSeries()
        posts = tv_series.get_fpt_posts(tmdb_tv_title)

        show_fpt_results(posts, media_type)

    elif mode[0] == 'fpt_tv':
        fpt_title = args["title"][0]
        fpt_tv_url = args["fpt_movie_url"][0]

        tv_series = TvSeries()
        tv_series.scrape(fpt_tv_url)
        tv_series.get_all_season_titles()
        series_season_list = [tv_series.seasons_title_list[i] for i in range (len(tv_series))]

        show_tv_seasons(fpt_title, fpt_tv_url, series_season_list)

    elif mode[0] == 'season':
        tv_title = args["series_title"][0]
        tv_page_url = args["page_url"][0]
        season_no = int(args["season_no"][0])

        tv_series = TvSeries()
        tv_series.scrape(tv_page_url)
        episodes = tv_series.get_season_by_number(season_no)

        show_season_episodes(tv_title, episodes)
    
    elif mode[0] == 'episode':
        episode_title = args["title"][0]

        urls = []
        for key in args:
            if key in STREAMING_SOURCES:
                urls.append(args[key][0])

        show_scraped_url(episode_title, urls)

    elif mode[0] == 'play':
        streaming_url = args['streaming_url'][0]
        streaming_source_name = get_streaming_source_name(streaming_url)

        if streaming_source_name == "speedvideo":
            playable_url = speedvideo.get_stream_url(streaming_url)
            if streaming_url != '' and streaming_url != '404':
                play_video(playable_url)

        elif streaming_source_name == "openload":
            play_video_with_resolver(streaming_url)
        
        elif streaming_source_name == "rapidcrypt":
            playable_url = openload.get_openload(streaming_url)
            play_video_with_resolver(playable_url)

    elif mode[0] == 'next':
        page = int(args['page'][0]) + 1
        media_type = args['media_type'][0]
        tmdb_type = args['tmdb_type'][0]
        keyword = args['keyword'][0]

        if media_type == 'tmdb_movie':
            results = get_tmdb_movie_results(tmdb_type, page, keyword)
        else:
            results = get_tmdb_tv_results(tmdb_type, page, keyword)
        
        show_moviedb_results(results, media_type, tmdb_type, page, keyword)




if __name__ == "__main__":
    route(mode)