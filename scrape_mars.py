from splinter import Browser
from bs4 import BeautifulSoup
import requests
import lxml.html as lh
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape():
    browser = init_browser()
       
    #url of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
     
    #get latest news article title and description
    title = soup.find("div", class_="content_title").text
    desc = soup.find('div', class_="rollover_description_inner").text
    
    title = title.replace('\n','').replace('\t',"")
    desc = desc.replace('\n','').replace('\t',"")
    
    #get latestSpace Image
    space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_image_url)
    
    space_image_html = browser.html
    soup2 = BeautifulSoup(space_image_html, 'html.parser')
    jpg = soup2.find(class_="fancybox")['data-fancybox-href']
    featured_image_url = (f'https://www.jpl.nasa.gov{jpg}')
    
    #Get latest twitter tweet on weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_response = requests.get(twitter_url)
    twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')
    
    tweet = twitter_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = tweet.text
    
    
    #Get latest facts
    marsfacts_url = 'https://space-facts.com/mars/'
    browser.visit(space_image_url)
    facts_response = requests.get(marsfacts_url)
    facts_soup = BeautifulSoup(facts_response.text, 'html.parser')

    doc = lh.fromstring(facts_response.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    tr_elements = doc.xpath('//tr')
    
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements:
        i+=1
        name=t.text_content()
        col.append((name))

    dataframe = pd.DataFrame(col)
    clean_dataframe = dataframe.replace('\n','', regex=True)
    clean_dataframe = clean_dataframe[0] .str.split(':', 1, expand=True)
    HTML_chart = clean_dataframe.to_html
    
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"},
    {"title": "Cerberus Hemisphere", "img_url": "chttp://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
    {"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
    {"title": "Syrtis Major Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
]

#create dictionary to push to mongo
    data = {
        "news_title": title,
        "news_paragraph": desc,
        "featured_image":featured_image_url,
        "weather": mars_weather,
        "hemispheres": hemisphere_image_urls
    }
        
    return data
    
    

