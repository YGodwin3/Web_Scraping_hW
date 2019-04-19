import pandas as pd
import time
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():
    mars_info ={}
    
    executable_path = {"executable_path": "C:\\Users\\Agodw_000\\Desktop\\chromedriver_win32 (4)\\chromedriver.exe"}
    browser= Browser("chrome", **executable_path, headless=False)
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    mars_info["news_title"]=news_title
    mars_info["news_p"]= news_p
    
    
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')
    featured_image= jpl_soup.find('a', class_="button fancybox")["data-fancybox-href"]
    featured_image_url= (f"https://www.jpl.nasa.gov/{featured_image}")
    mars_info["featured_image_url"]= featured_image_url
    
    mars_weather_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    mars_weather_html= browser.html
    mars_weather_soup= bs(mars_weather_html,"html.parser")
    mars_weather= mars_weather_soup.find("div", class_= "js-tweet-text-container").text
    mars_info["mars_weather"]= mars_weather
    
    mars_facts_url= "https://space-facts.com/mars/"
    df=pd.read_html(mars_facts_url)
    df=df[0]
    df.columns=["facts","values"]
    mars_html= df.to_html()
    mars_info["mars_html"]= mars_html
    

    mars_hem_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hem_url)
    hemis_html = browser.html
    soup = bs(hemis_html, 'html.parser')
    titles = ["Cerberus","Schiaparelli","Syrtis","Valles"]
    hemisphere_image_urls=[]
    for title in titles:
        mars_hem_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(mars_hem_url)
        mars_hem_html= browser.html
        mars_hem_soup= bs(mars_hem_html,"html.parser")
        browser.click_link_by_partial_text(title)
        soup6= bs(browser.html,"html.parser")
        mars_hem6= soup6.find("div", class_ = "downloads").find_all("li")[0].find("a")["href"]
        mars_hem_title6= soup6.find("h2",class_="title").text
        hemisphere_image_urls.append({"titles":mars_hem_title6, "url":mars_hem6})
        
    mars_info["hemisphere_image_urls"]=hemisphere_image_urls
    
    browser.quit()
    return mars_info