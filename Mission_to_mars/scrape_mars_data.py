
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
import urllib3
from urllib3.util.retry import Retry

def init_browser():
# @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:\\chromedriver_win32\\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


#--------------------mars news-------------------------
def scrape_news():
    browser = init_browser()
    # News_data ={ }
 
# Visit visitcostarica.herokuapp.com
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
   
    time.sleep(1)

# Scrape page into Soup


    html = browser.html
    # parse HTML with Beautiful soup
    soup = bs(html, 'html.parser')

    abc = soup.select_one("ul.item_list li.slide")
    news_title = abc.find('div', class_='content_title').get_text()
    print(news_title)
    news_p = abc.find('div', class_='article_teaser_body').get_text()
   
    #store data in a dictionary
    
    # close the browser
    browser.quit()
#
    #return results
    # return News_data
    return [news_title,news_p]

    #--------------------------------------------------jpldata-------------------------------

# def init_browser():
# # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {'executable_path': 'C:\\chromedriver_win32\\chromedriver.exe'}
#     return Browser("chrome", **executable_path, headless=False)


def scrape_jpl():
    browser = init_browser()
    # News_data ={ }
 
# Visit visitcostarica.herokuapp.com
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    
    time.sleep(1)

    html = browser.html

    soup = bs(html, 'html.parser')

    browser.find_by_id("full_image").click()

    #find more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    html = browser.html

    soup = bs(html, 'html.parser')

    #find the image url
    img_url = soup.select_one('figure.lede a img').get('src')
    # print(img_url)
    Featured_image_url = f'https://www.jpl.nasa.gov/{img_url}'
    
    
    browser.quit()
    #Return results
    return Featured_image_url
#-----------------------------------------hemisheredata--------------------------------------

# def init_browser():
# # @NOTE: Replace the path with your actual path to the chromedriver
#     executable_path = {'executable_path': 'C:\\chromedriver_win32\\chromedriver.exe'}
#     return Browser("chrome", **executable_path, headless=False)


def scrape_hemsp():
    browser = init_browser()
    
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)  

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    # browser.find_by_tag('h3').click()
    hemisphere_images_url=[]

    for x in range(4):
        browser.find_by_tag('h3')[x].click()
        
        html = browser.html
        soup = bs(html, "html.parser")

        images=soup.find('img',class_='wide-image')['src']
        image_url=f'https://astrogeology.usgs.gov/{images}'

        title=soup.find('h2').text
        browser.back()
        hemisphere_images_url.append({"title": title, "img_url":image_url })
        


    browser.quit()
    return hemisphere_images_url

#------------------------------------------------mars facts----------------------------
def mars_facts():
    # url ='https://space-facts.com/mars/'
    url =  'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Diameter', 'units']
    dict_table = df.to_dict('records')
    return dict_table