import json
import logging

from base import Scraper
from taxclock.settings import scrape_sites, base_urls, IMG_PLACEHOLDER


log = logging.getLogger(__name__)


class NationMedia(Scraper):
    def __init__(self):
        super(NationMedia, self).__init__()
        self.url = scrape_sites['nation']
        self.base = Scraper()

    def scrape_page(self):
        '''Scrapes stories from nation media.
        Usage::
              use the class object
              pass the site url to\
              get_html_content method.
        :param_train_data: the url of the site
        :rtype: the stories image,link, title.
        '''
        result = self.base.get_html_content(self.url)
        if result:
            try:
                data = []
                items = result.find_all(
                    'div', class_='story-teaser top-teaser')
                for item in items:
                    img_src = item.find('img').get('src')
                    if img_src:
                        img_url = base_urls['nation'] + img_src
                    else:
                        img_url = IMG_PLACEHOLDER
                    link = base_urls['nation'] + item.find('a').get('href')
                    get_data = self.base.get_html_content(link)
                    date = get_data.find('h6').text
                    text = get_data.find('h2').text
                    data.append({
                        'link': link,
                        'img': img_url,
                        'title': text,
                        'date_published': date
                    })
            except Exception as err:
                log.error(str(err))
            return data
        else:
            log.error(str(result))
