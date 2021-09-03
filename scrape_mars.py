import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_page = {}

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Parse latest news title & description
    title = soup.find('div', class_='content_title').text
    mars_page['news_title'] = title
    body_text = soup.find('div', class_='article_teaser_body').text
    mars_page['news_description'] = body_text
    
    url_ = 'https://spaceimages-mars.com/'
    browser.visit(url_)

    # browser.links.find_by_partial_text('FULL IMAGE').click()
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image_url = soup.find('img', class_='headerimage fade-in')['src']
    mars_page['featured_image'] = url_ + featured_image_url

    url1 = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url1)
    mars_table = tables[0]
    html_table = mars_table.to_html()
    mars_page['mars_earth_table'] = html_table
    # mars_page['mars_earth_table'] = html_table.replace('\n', '')


    url2 = 'https://marshemispheres.com/'
    browser.visit(url2)

    links = browser.find_by_css('a.product-item img')
    links


    hemispheres = []

    for x in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item img')[x].click()
        link = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = link['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text 
        
        hemispheres.append(hemisphere)
        browser.back()

    mars_page['mars_hemispheres'] = hemispheres
    # hemispheres = []
    
    # for x in range(len(links)):
    #     browser.find_by_css('a.product-item img')[x].click()
    #     link = browser.links.find_by_text('Sample').first
    #     mars_page['img_url'] = link['href']
    #     mars_page['title'] = browser.find_by_css('h2.title').text
    #     hemispheres.append(mars_page)
    #     browser.back()

    #     mars_page.append(hemispheres)

    # Quit the browser
    browser.quit()
    print(mars_page)
    return mars_page

if __name__ == '__main__':
    scrape()