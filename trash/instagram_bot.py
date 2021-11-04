import re
import os
import random
import time
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup():
    return webdriver.Chrome()


def login(driver):
    driver.get('https://www.instagram.com/?hl=en')
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]')))
    element.clear()
    element.send_keys('drobertpaul@gmail.com')
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))
    element.clear()
    element.send_keys('fjdXYnA&jDf*PbT4t;oY')
    element.send_keys(Keys.RETURN)
    print('Successfully logged in user')


def clear_login_popups(driver):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'XTCLo.x3qfX')))
    element = driver.find_element_by_xpath('//button[text()="Not Now"]')
    element.click()
    # element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'aOOlW.HoLwm')))
    # element.click()
    print('Successfully cleared popups')


def get_search_tags():
    tags = []
    with open('./configs/search_tags.txt') as doc:
        for line in doc.readlines():
            tags.append('{0}'.format(line))
    return tags


def get_visted_urls():
    urls = []
    if not os.path.exists('./configs/visted_urls.txt'):
        open('./configs/visted_urls.txt', 'w+')

    with open('./configs/visted_urls.txt') as doc:
        for line in doc.readlines():
            urls.append(r'{0}'.format(line.strip()))
    return urls


def get_comment():
    comments = []
    with open('./configs/comments.txt') as doc:
        for line in doc.readlines():
            comments.append('{0}'.format(line))

    random_index = random.randint(0, len(comments)-1)
    comment = comments[random_index]
    return comment


def update_visted_urls(url):
    with open('./configs/visted_urls.txt', 'a') as doc:
        doc.write('{0}\n'.format(url))


def update_following(user):
    if not os.path.exists('./configs/following.txt'):
        open('./configs/following.txt', 'w+')
    with open('./configs/following.txt', 'a') as doc:
        doc.write('{0}  {1}\n'.format(user, date.today()))


def search_tags(driver, tags):
    for tag in tags:
        try:
            # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'XTCLo.x3qfX')))
            search_url = 'explore/tags/{0}'.format(tag)
            driver.get('https://www.instagram.com/{0}'.format(search_url))
            visted_urls = get_visted_urls()
            if not pick_photo(driver, visted_urls):
                continue
            response = like_photo(driver)
            if response:
                follow(driver)
        except Exception as e:
            print(e)
            continue


def pick_photo(driver, visted_urls: list):
    children = driver.find_elements_by_class_name('v1Nh3.kIKUG._bz0w')
    image_urls = []
    for child in children:
        element = child.find_element_by_tag_name('a')
        url = element.get_attribute(r'href')
        exists = False
        for i in visted_urls:
            if i == url:
                exists = True
            continue
        if exists == False:
            image_urls.append(url)

    index = 0
    while True:
        # random_index = random.randint(0, len(image_urls)-1)
        search_url = image_urls[index]
        update_visted_urls(search_url)
        driver.get(search_url)
        user_input = input('Pick photo? y/n/nn')
        if user_input == 'n':
            index += 1
            continue
        elif user_input == 'nn':
            return False
        break

    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sH9wk._JgwE')))
        return True
    except:
        return False


def follow(driver):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'sqdOP.yWX7d._8A5w5.ZIAjV')))
    user_url = element.get_attribute('href')
    regex = re.findall(r'.com\/(.+)\/', user_url)
    if regex:
        user = regex[0]
        update_following(user)
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'sqdOP.yWX7d.y3zKF')))
    if(element.text == 'Follow'):
        element.click()


def like_photo(driver):
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, '_8-yf5')))
    children = driver.find_elements_by_class_name('_8-yf5')
    for child in children:
        if child.get_attribute('aria-label') != 'Like':
            continue
        response = comment_on_photo(driver)
        if response == True:
            child.click()
            return True
        return False


def comment_on_photo(driver):
    comment = get_comment()
    print(comment)
    comment_input = input(
        'comment on photo? y/n? type `c` for custom comment: ')
    if comment_input == 'c':
        custom_comment_input = input('Enter custom comment: ')
        comment = custom_comment_input
    if comment_input == 'n':
        return False
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Ypffh')))
    element.click()
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'Ypffh')))
    element.send_keys(comment)
    element.send_keys(Keys.RETURN)
    time.sleep(3)
    return True


def start():
    driver = setup()
    login(driver)
    clear_login_popups(driver)
    tags = get_search_tags()
    search_tags(driver, tags)
    driver.quit()
