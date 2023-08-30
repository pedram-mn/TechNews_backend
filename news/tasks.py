import json
from celery import shared_task
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from news.JalaliToGeorgian import converter
from news.getZoomitNews import get_all_news
from news.models import Reference, Tag, News


def save_to_db(news):
    news_object = News(title=news['title'], content=news['content'])
    news_object.save()
    news_object = News.objects.get(title=news['title'], content=news['content'])

    reference_object = Reference(link=news['reference']['link'],
                                 author=news['reference']['author'],
                                 date=converter(news['reference']['date']))
    reference_object.save()

    news_object.references.add(Reference.objects.get(link=news['reference']['link']))

    for tag in news['tags']:
        try:
            news_object.tags.add(Tag.objects.get(name=tag))
        except:
            tag_object = Tag(name=tag)
            tag_object.save()
            news_object.tags.add(Tag.objects.get(name=tag))


@shared_task(bind=True)
def extract_zoomit_news(self):
    # initializing chromedriver
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Remote(
        command_executor='http://selenium_hub:4444/wd/hub',
        options=chrome_options
    )

    get_all_news(driver)
    driver.quit()
    with open('./news/news.json', 'r', encoding='utf-8') as f:
        raw_news_list = json.load(f)

    for raw_news in raw_news_list:
        save_to_db(raw_news)

    return "New news saved to database"
