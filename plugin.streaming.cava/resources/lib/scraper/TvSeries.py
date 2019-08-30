import re
import requests
import sys

from resources.lib import scraper_lib
from resources.lib.scraper.FPTScraper import FPTScraper


class TvSeries(FPTScraper):

    def __init__(self, release_date=None):
        if sys.version_info[0] < 3:
            super(TvSeries, self).__init__(release_date)
        else:
            super().__init__(release_date)

        self.seasons_title_list = []
        self.is_modern_state = True
        self.replacing_chars = ["\n", ";", " "]
    
    def __len__(self):
        return len(self.seasons_title_list)

    def get_result_from_fpt(self, keyword):
        return self.get_fpt_posts(keyword)
    
    def scrape(self, fpt_tvshow_url):
        self.soup = scraper_lib.get_page_soup(fpt_tvshow_url)
        self.seasons_wrapper = self.get_seasons_wrapper()
    
    def replace_chars(self, word):
        for char_to_replace in self.replacing_chars:
            word = word.replace(char_to_replace, '')
        return word.strip()

    def get_episode_info(self, tag):
        episode_urls = []
        if self.is_modern_state:

            episode_wrapper = scraper_lib.get_tag(tag, "ul")

            name = scraper_lib.Element(block=episode_wrapper, el_tag='li',
                el_class="episode_link", get_text=True)
            
            url = scraper_lib.Element(block=episode_wrapper, el_tag='a',
                el_class="myBtn", el_property="data-link")
            try:
                #main link(speedvideo)
                episode_name = name.get_element()
                episode_url = url.get_element()
                episode_urls.append(episode_url)

                #other links
                others_url = scraper_lib.get_hrefs(block=tag, filters=self.streaming_to_scrape)
                episode_urls = episode_urls + others_url
            except:
                episode_name = "nd"
        else:
            #old version
            try:
                soup = scraper_lib.get_soup(tag)
                episode_name = scraper_lib.get_previous_sibling(block=soup, tag='a')
                episode_name = self.replace_chars(episode_name)

                episode_urls = scraper_lib.get_hrefs(block=soup, filters=self.streaming_to_scrape)
            except:
                episode_name = "nd"

        return {episode_name: episode_urls}

    def get_all_season_titles(self):
        #return all seasons title
        if sys.version_info[0] < 3:
            del self.seasons_title_list[:]
        else:
            self.seasons_title_list.clear()

        if self.is_modern_state:
            season_container = scraper_lib.Container(block=self.seasons_wrapper,
                tag='div', container_class='accordion-item')

            title = scraper_lib.Element(block='', el_tag='ul', get_text=True)
        else:
            #old version
            season_container = scraper_lib.Container(block=self.seasons_wrapper,
                tag='p', text=True, recursive=False)

            title = scraper_lib.Element(block='', el_tag='span', get_text=True)

        seasons = season_container.get_container()

        for season in seasons:
            title.block = season
            self.seasons_title_list.append(title.get_element())

    def get_seasons_wrapper(self):
        #return the html tag which cointains all the seasons
        seasons_wrapper = scraper_lib.Container(block=self.soup, tag='div', first=True,
                container_class='seasons-wraper').get_container()

        if seasons_wrapper is not None:
            return seasons_wrapper
        else:
            self.is_modern_state = False

            container = scraper_lib.Container(block=self.soup, tag='div',
                    container_id='info', container_class='pad').get_container()

            return container[-1]
    
    def get_all_episodes(self, episode_wrapper):
        episodes = []
        if self.is_modern_state:

            episodes_wrapper = scraper_lib.Container(block=episode_wrapper, tag='div',
                    container_class='episode-wrap').get_container()
                            
            for episode in episodes_wrapper:
                episodes.append(self.get_episode_info(episode))
        else:
            #old version
            episodes_html = "{0}".format(episode_wrapper).split("<br/>")
            for episode in episodes_html:
                episodes.append(self.get_episode_info(episode.strip()))
        return episodes

    def get_season_by_number(self, season_no):
        #return all episodes of that season
        self.get_all_season_titles()
        if len(self.seasons_title_list) > 0:
            try:
                season_title = self.seasons_title_list[season_no]
            except IndexError:
                season_title = self.seasons_title_list[-1]

            if self.is_modern_state:
                #new version config
                seasons = scraper_lib.Container(self.seasons_wrapper, tag='div',
                    container_class='accordion-item').get_container()
                
                s_title = scraper_lib.Element(block='', el_tag='ul',
                    get_text=True)

                season_content = scraper_lib.Container(block='', tag='div', first=True,
                        container_class='content')    
            else:
                #old version config
                seasons = scraper_lib.Container(self.seasons_wrapper, tag='p',
                    recursive=False).get_container()

                s_title = scraper_lib.Element(block='', el_tag='span',
                    get_text=True)
            
            for season in seasons:
                try:
                    s_title.block = season
                    title = s_title.get_element()
                except:
                    title = "nd"

                if title == season_title:
                    if not self.is_modern_state:
                        content = scraper_lib.get_next_sibling(season)
                    else:
                        season_content.block = season
                        content = season_content.get_container()

                    all_episodes = self.get_all_episodes(content)
                    return all_episodes

        return None




if __name__ == "__main__":
    tv_show = TvSeries()
    res = tv_show.get_fpt_posts('breaking bad')
    url = res[0]['url']
    tv_show.scrape(url)
    tv_show.get_all_season_titles()
    print(tv_show.get_season_by_number(2))

    print()
    print()

    tv_show2 = TvSeries()
    res = tv_show2.get_fpt_posts('mr robot')
    url = res[0]['url']
    tv_show2.scrape(url)
    tv_show2.get_all_season_titles()
    print(tv_show2.get_season_by_number(2))