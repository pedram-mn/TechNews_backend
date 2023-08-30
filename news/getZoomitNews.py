import json
import time
from django.core.exceptions import ObjectDoesNotExist
from selenium.webdriver.common.by import By
import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'TechNews_back.settings'
django.setup()
from news.models import Reference


link_count = 0


# function for getting last 30 news that open every time press show-more button
def get_30_links(driver):
    global link_count

    # try 5 times to get last 30 links to make sure that errors made by rendering problems solves
    try_count = 0
    while try_count < 5:
        try:
            # list of news links
            list_of_new_links = []

            # main div container of news section
            news_container = driver.find_element(By.XPATH,
                                                 "//*[@id='__next']/div[2]/div[1]/div[3]/div/div/div[2]/div/div[2]")

            # 30 last subsections that contain each news
            list_of_container_children = news_container.find_elements(By.XPATH, "*")[-30:]

            # some news have a div tag that contains ad section, so the last div in the
            # subsection become the main div that contain news details
            list_of_sub_div = []
            for div in list_of_container_children:
                temp = div.find_elements(By.XPATH, "*")
                if len(temp) == 1:
                    list_of_sub_div.append(temp[0])
                else:
                    list_of_sub_div.append(temp[-1])

            # extract news link from elements and append it into the list of links
            for div in list_of_sub_div:
                # try this step for every section and if error happened then ignore that link
                try:
                    a_tag = div.find_elements(By.XPATH, "*")[1].find_elements(By.XPATH, "*")[0]
                    news_link = a_tag.get_attribute("href")
                    list_of_new_links.append(news_link)
                    link_count += 1
                except:
                    print(f'link {link_count + 1} extraction failed..., ignoring the link')
                    time.sleep(1)

            return list_of_new_links
        except:
            try_count += 1
            # wait 1 second after each error
            time.sleep(1)

    print('failed to get last 30 links, returning empty list')
    return []


def click_show_more(driver):
    try_count = 0
    # try hitting button ten times if any error raised
    while try_count < 10:
        try:
            button = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/div[2]/div[1]/div[3]/div/div/div[2]/div/div[3]/button')
            button.click()
            time.sleep(2)  # wait for complete rendering new links
            break
        except:
            try_count -= 1
            print('show more failed')


# function to extract details of each news
def get_news(driver, link):
    # check if news is already saved
    try:
        Reference.objects.get(link=link)
        print('existed news found')
        return 'Existed'
    except ObjectDoesNotExist:
        pass

    # opening the link
    try:
        driver.get(link)
    except:
        print('error occured while openning link')

    # try to extract data 5 times before ignoring it
    try_count = 0
    while try_count < 5:
        try:

            # extracting title
            title = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/main/header/div/div/h1').text

            # extracting tags elements and then make a list of those elements' text
            tags_elements = driver.find_elements(By.XPATH,
                                                 '//*[@id="__next"]/div[2]/div[1]/main/header/div/div/div[1]/div[1]/a/span')
            tags = [el.text for el in tags_elements]

            # extract author name of news
            ref_author = driver.find_element(By.XPATH,
                                             '//*[@id="__next"]/div[2]/div[1]/main/header/div/div/div[2]/a/div/span').text
            # extract date of news
            ref_date = driver.find_element(By.XPATH,
                                           '//*[@id="__next"]/div[2]/div[1]/main/header/div/div/div[1]/span[1]').text

            # extract intro of news and append it later into main content
            intro = driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div[2]/div[1]/main/article/div[3]/div/div/span').text

            # paragraphs of news wrapped with p tag.
            # extract them and join all of their texts together and add it to intro.
            p_tags = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/div[1]/main/article/div[5]/div/div/p')
            content = intro + ''.join([p.text for p in p_tags])

            # return news dictionary
            return {
                'title': title,
                'content': content,
                'tags': tags,
                'reference': {
                    'link': link,
                    'author': ref_author,
                    'date': ref_date
                }
            }

        except:
            try_count += 1

    # returning None for failed extractions
    print('error happened in extracting news, returning None...')
    return None


# function that do the all things and extract and save all news
def get_all_news(driver):
    # list of all news extracted
    all_news = []
    # list of all links
    links_list = []

    # opening zoomit news website
    try:
        driver.get("https://www.zoomit.ir/archive/?sort=Newest&skip=0")
    except:
        print('error occured while openning link')

    # limit of links is 1100 instead of 1000 as a prediction for failed-extracted news
    while len(links_list) < 30:
        links_list += get_30_links(driver)
        click_show_more(driver)
        print(f'{len(links_list)} links extracted')

    print('extracting news...')

    for i in links_list:
        # an exception handling for unpredicted errors
        try:
            news = get_news(driver, i)
        except:
            print('main loop for getting news failed, the link is: ' + i)
            news = None

        if news == 'Existed':
            break

        # append extracted news to list if not equal to None
        if news is not None:
            all_news.append(news)

    print(f'{len(all_news)} new news extracted successfully, saving to file...')

    # write news to json file to save them into database later
    with open('./news/news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, indent=4, ensure_ascii=False)

    print('all extracted news saved to news.json file')
