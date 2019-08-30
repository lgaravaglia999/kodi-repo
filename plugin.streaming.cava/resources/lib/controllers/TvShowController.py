from resources.lib.views import TvshowView
from resources.lib.scraper.TvSeries import TvSeries
from resources.lib import kodiutilsitem

def fpt_tvshow(title, release):
	tv_show = TvSeries()
	posts = tv_show.get_fpt_posts(title)
	TvshowView.show_fpt_results(posts, 'fpt_tv')

def fpt_seasons(tvshow_title, page_url):
	tv_series = TvSeries()
	tv_series.scrape(page_url)
	tv_series.get_all_season_titles()
	series_season_list = [tv_series.seasons_title_list[i] for i in range (len(tv_series))]
	TvshowView.show_tv_seasons(tvshow_title, page_url, series_season_list)

def fpt_episodes(tvshow_title, page_url, season_no):
	tv_series = TvSeries()
	tv_series.scrape(page_url)
	episodes = tv_series.get_season_by_number(season_no)
	TvshowView.show_season_episodes(tvshow_title, episodes)

def fpt_episodes_streaming_options(ep_title, *args):
	urls = []
	for key in args:
		if key in kodiutilsitem.STREAMING_SOURCES:
			urls.append(args[key][0])

	TvshowView.show_scraped_url(ep_title, urls)
