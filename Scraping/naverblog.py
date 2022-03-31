import urllib.request
import json
from selenium import webdriver
import pandas as pd
import re

def cleansing(text):
    pattern = '(\[a-zA-Z0-9\_.+-\]+@\[a-zA-Z0-9-\}+.\[a-zA-Z0-9-.\]+)'
    text = re.sub(pattern=pattern, repl=' ', string=text)

    pattern = '(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+'
    text = re.sub(pattern = pattern, repl=' ', string=text)

    pattern = '((¤¡-¤¾¤¿-¤Ó])+'
    text = re.sub(pattern = pattern, repl= ' ', string=text)

    pattern = '<[^>]*>'
    text = re.sub(pattern = pattern, repl = ' ', string=text)

    pattern = '[\r|\n]'
    text = re.sub(pattern = pattern, repl=' ', string=text)

    pattern = '[^\w\s]'
    text = re.sub(pattern = pattern, repl = " ", string=text)

    pattern = re.compile(r'\s+')
    text = re.sub(pattern = pattern, repl = " ", string=text)
    return text

client_id = "blank"
client_secret = "blank"

keyword = "keyword"
encText = urllib.parse.quote(keyword)


#1 Naver blog API- extract naver blog link related with keywords
link_ls = []
url = "https://openapi.naver.com/v1/search/blog?query=" + encText  + "&sort=date&start=1&display=100"# json °á°ú
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read().decode("utf-8")
    json_body = json.loads(response_body)
    items = json_body["items"]
    for item in items:
        link_ls.append(item["link"])
else:
    print("Error Code:" + rescode)


#2 Parsing content accesing blogs with links
driver = webdriver.Chrome("/Users/jihyunlee/Downloads/chromedriver")
text_ls = []
for link in link_ls:
    text = ""
    driver.get(link)
    try:
        iframes = driver.find_elements_by_css_selector('iframe')
        driver.switch_to.frame('mainFrame')
        container = driver.find_element_by_class_name("se-main-container")
        paras = container.find_elements_by_css_selector(".se-component.se-text.se-l-default")
        for para in paras:
            text += para.text
        text_ls.append(text)
    except:
        try:
            try:
                id = driver.find_element_by_id("postViewArea")
                text_ls.append(id.text)
            except:
                wrap = driver.find_element_by_css_selector(".se_component_wrap.sect_dsc.__se_component_area")
                text_ls.append(wrap.text)
        except:
            pass

naver_blog = pd.Series(text_ls)
naver_blog.name("content")
naver_blog.to_csv("naverblog.csv")

