#!/usr/bin/env python
# coding: utf-8
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemispheres(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls,
    }
    # Stop webdriver and return data
    browser.quit()
    return data
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
   
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        return news_title, news_p
    except AttributeError:
        return None, None
    

# ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
        # Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        return img_url
    except AttributeError:
        return None

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df.columns=['description', 'Mars', 'Earth']
        df.set_index('description', inplace=True)
        return df.to_html(classes="table table-hover")
    except BaseException:
        return None

#Deliverable 2
def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
# 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    site_html = browser.html
    html =  soup(site_html, 'html.parser')
    links = html.find_all("div", class_="description")
    for link in links:
        title = link.select_one('h3').text
        sub_url = link.select_one('a').get('href')
        browser.visit(url + sub_url)
        sub_html = browser.html
        sub_parsed = soup(sub_html, 'html.parser')
        list_box = sub_parsed.select_one('ul')
        img_url = list_box.find_all('a')[0].get('href')
        d = {'title': title,
            'img_url': url + img_url}
        hemisphere_image_urls.append(d)
    return hemisphere_image_urls
        

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

