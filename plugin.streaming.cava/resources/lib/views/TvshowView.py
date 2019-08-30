from resources.lib import kodiutilsitem

def show_fpt_results(posts_data, media_type):
    """
    Show all movies/tv shows scraped
    :param posts_data: list of dictionaries representing scraped info
    :param media_type: str
    """
    is_folder = True
    for post in posts_data:
        item_url = {
            'mode': 'selected_tvshow',
            'title': post["title"].encode("utf-8"),
            'fpt_movie_url': post["url"]
            }

        item_title = u''.join(post["title"]).encode("utf-8").strip()
      
        item_arts = {
            'thumb': post["image"],
            'fanart': post["image"]
            }
        kodiutilsitem.add_item(url_dict=item_url, title=item_title,
            is_folder=is_folder, arts=item_arts)
        
    kodiutilsitem.end_directory()

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
            'mode':'selected_season',
            #'series_title': tv_title,
            'season_title': tv_seasons_list[i].encode("utf-8"),
            'page_url': fpt_tv_url,
            'season_no': i
            }
        
        item_title = u''.join(tv_seasons_list[i]).encode("utf-8").strip()

        kodiutilsitem.add_item(url_dict=item_url, title=item_title, is_folder=is_folder)
        
    kodiutilsitem.end_directory()

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
            'mode':'selected_episode',
            'title': ep_title.encode("utf-8")
            }
        
        for url in ep_urls:
            name = kodiutilsitem.get_streaming_source_name(url)
            item_url[name] = url
    
        item_title = u"".join(ep_title).encode("utf-8").strip()

        item_property = {"prop_key": 'IsPlayable', "prop_value": 'true'}

        kodiutilsitem.add_item(url_dict=item_url, title=item_title, is_folder=is_folder,
            properties=item_property)

    kodiutilsitem.end_directory()

def show_scraped_url(movie_title, movie_urls):
    """
    Show playable items with all streaming options for the selected movie.

    :param movie_title: str
    :param movie_urls: list of strings representing movie url
    """
    is_folder = False
    for movie_url in movie_urls:
        streaming_source = kodiutilsitem.get_streaming_source_name(movie_url)

        item_url = {
            'mode':'play',
            'title': movie_title,
            'streaming_url': movie_url
            }
        
        item_title = "{0} [{1}]".format(movie_title, streaming_source)

        item_property = {"prop_key": 'IsPlayable', "prop_value": 'true'}

        kodiutilsitem.add_item(url_dict=item_url, title=item_title, is_folder=is_folder,
            properties=item_property)
                
    kodiutilsitem.end_directory()

