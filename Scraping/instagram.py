from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

def select_first(driver):
    first = driver.find_element_by_css_selector("div._9AhH0")
    first.click()
    time.sleep(4)

#extract information of feeds
def get_content(soup, num):
    #1 extract html of current page 
     html = driver.page_source
     soup = BeautifulSoup(html, "lxml")

    #2 content
    try:
        content = soup.select("div.C4VMK > span")[0].text
        print(content)
    except:
        content = ''

    #3 id 
    try:
        id = soup.select("div.e1e1d")[0].text
        id  = id.replace("인증됨", "")
    except:
        id = ''

    #4 number of likes
    try:
        like = soup.select("div.Nm9Fw > button")[0].text[4:-1]
    except:
        like = 0

    #5 date
    try:
        date = soup.select('time._1o9PC.Nzb55')[0]["datetime"][:10]
    except:
        date = ''

    #6 hastags
    tags = re.findall(r'#[^\s#,\\]+', content)
    tags = list(map(lambda s:s.replace("#", ""), tags))


    #7 url 가져오기
    url_address = driver.current_url

    #8 썸네일 이미지
    try:
        image = soup.select("div.KL4Bh > img")[num]["src"]
    except:
        image = ''

    data = [content, id, like, date, tags, url_address, image]

    return data

    #9 인플루언서 정보 가져오기


def move_next(driver):
    try:
        right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
        right.click()
        time.sleep(4)
    except:
        pass

#1 Access to Instagram page
driver = webdriver.Chrome("/Users/jihyunlee/Downloads/chromedriver")
keyword = input("키워드를 입력하시오 > ")
url = "https://www.instagram.com/explore/tags/"+keyword
driver.get(url)
driver.implicitly_wait(4)


#2 Login 

driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()
# driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()
driver.implicitly_wait(3)
elem_login = driver.find_element_by_name("username")
elem_login.clear() #Delete 'default' on the search window
elem_login.send_keys("id") 
time.sleep(1)

elem_login = driver.find_element_by_name('password')
elem_login.clear()
elem_login.send_keys("passwords")
time.sleep(3)
driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button/div').click()
time.sleep(3)


driver.get(url)
select_first(driver)
results = []
target = 350

for i in range(target):
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    data = get_content(soup, i)
    results.append(data)
    try:
        move_next(driver)
        time.sleep(5)
    except:
        pass

total_data = pd.DataFrame(results, index = [i for i in range(target)], columns = ["content", "id", "like", "date", "tags", "url_address", "image"])

# total_data.to_csv("insta.csv", encoding='utf-8')

