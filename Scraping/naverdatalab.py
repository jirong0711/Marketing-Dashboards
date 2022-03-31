from selenium import webdriver
import time
import pandas as pd

url = "https://datalab.naver.com/shoppingInsight/sCategory.naver"

#1 Extract Popular keywords data

##1 'Keyword input' is string type (ex 메이크업) and change it into category id
id = ["50000002", "50000195"]

#1-2 access to naver datalab site 
driver = webdriver.Chrome("location of driver")
driver.get(url)

#1-3 Choose specific category
for i in range(0,2):
    category = driver.find_element_by_css_selector("div.set_period.category")
    scroll = category.find_elements_by_css_selector("ul.select_list.scroll_cst")[i]
    aa = scroll.find_elements_by_tag_name("a")
    for a in aa:
        if a.get_attribute("data-cid") == id[i]:
            driver.execute_script("arguments[0].click();", a)
driver.find_element_by_class_name("btn_submit").click()
time.sleep(2)

#1-4 Extract top-500 data
keyword_ls = []
for p in range(0,25):
    aa = driver.find_element_by_css_selector("ul.rank_top1000_list").find_elements_by_tag_name("a")
    keyword_ls.extend(list(map(lambda x :x.text.split("\n")[1], aa)))
    driver.find_element_by_css_selector("a.btn_page_next").click()


##2 Extract brand name 
brand_ls = []
path = "https://search.shopping.naver.com/search/category?catId=" + id[1]
driver.get(path)

driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/a'))
time.sleep(2)
lis = driver.find_elements_by_xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]/ul/li')
brand_ls.extend(list(map(lambda x: x.text, lis)))


keyword = pd.Series(keyword_ls)
keyword.name = "keyword"
keyword.to_csv("keyword.csv")

brand = pd.Series(brand_ls)
brand.name = "brand"
brand.to_csv("brand.csv")



