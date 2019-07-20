from os import path
import sys

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import scraper_lib

class FPTScraper(object):
    def __init__(self, release_date=None):
        self.release_date = release_date

        self.url_check_domain = "https://www.filmpertutti.group/"
        self.filmpertutti_url = "{0}/?s={1}"

        self.default_domain = "https://www.filmpertutti.media"
        self.domain = self.get_filmpertutti_domain()

        self.streaming_to_scrape = ["speedvideo", "openload", "rapidcrypt.net/open"]

    def get_filmpertutti_domain(self):
        #check and return current domain
        try:
            soup = scraper_lib.get_page_soup(self.url_check_domain)

            wrapper = scraper_lib.Container(block=soup, tag='div', first=True,
                container_class="content").get_container()

            domain_url = scraper_lib.get_hrefs(wrapper, ["filmpertutti."])[0]
            return domain_url
        except:
            return self.default_domain
        
    def get_post_info(self, fpt_post):
        post_title = scraper_lib.Element(block=fpt_post, el_tag="div",
            el_class="title", get_text=True).get_element()
        
        post_ref_url = scraper_lib.Element(block=fpt_post, el_tag="a",
            el_property="href").get_element()

        image = scraper_lib.Element(block=fpt_post, el_tag="a",
            el_property="data-thumbnail").get_element()

        return {"title": post_title, "url": post_ref_url, "image": image}

    def get_fpt_posts(self, keyword):
        #returns url of page to scrape (returns first record if many)
        posts_list = []
        key_search = keyword.replace(" ", "+")
        url_search = self.filmpertutti_url.format(self.domain, key_search)

        soup = scraper_lib.get_page_soup(url_search)

        container = scraper_lib.Container(block=soup, tag='ul',
            first=True, container_class="posts").get_container()

        posts = scraper_lib.Container(block=container, tag='li').get_container()

        for post in posts:
            posts_list.append(self.get_post_info(post))
        
        return posts_list

    def filter_streamings(self, href):
        return href and any(s in href for s in self.streaming_to_scrape)