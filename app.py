import bs4 as bs
from urllib.request import urlopen, Request
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

note = input("Enter image string: ") #image label/name
directory = input("Enter name of directory to save: ") #name of folder you want to save images in

#creating directory and change directory
current_dir = os.getcwd()
path = os.path.join(current_dir,directory)
os.mkdir(path)
os.chdir(path)

driver = webdriver.Chrome(executable_path='path to chromedriver')

reg_url = 'https://www.google.co.in/images'

driver.get(reg_url)

insert_string = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
insert_string.send_keys(note)
insert_string.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

source = driver.page_source
soup = bs.BeautifulSoup(source,'lxml')

driver.close()

total = 0
#getting/saving images
for section in soup.find('div',class_="mJxzWe"):
    for img in section.find_all('img'):
        img_src = img.get('data-src')
        if img_src != None:
            total +=1
            try:
                urllib.request.urlretrieve(img_src,str(total)+".jpg")
            except:
                print("slow connection")