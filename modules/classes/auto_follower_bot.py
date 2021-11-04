import re
import time
import random
from modules import utils
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AutoFollowerBot:
    def __init__(self) -> None:
        self.tags = utils.get_search_tags()

    def get_auto_followers(self):
        count = 0
        current_progress = 0
        total_progress = len(self.tags)
        for tag in self.tags:
            print('Current Tag: {0}'.format(tag))
            try:
                search_url = 'explore/tags/{0}'.format(tag)
                self.driver.get('https://www.instagram.com/{0}'.format(search_url))
                if not self._auto_pick_photo():
                    continue
                if self._auto_like_photo():
                    self._auto_follow()
            except Exception as e:
                print(e)
                continue
            count += 1
            current_progress += 1
            print('Progress: {0}/{1}'.format(current_progress, total_progress))
            if count == 5:
                count = 0
                self.driver.get('https://www.instagram.com/')
                time.sleep(random.randint(60, 120))

    def _auto_get_photos(self) -> list:
        children = self.driver.find_elements_by_class_name('v1Nh3.kIKUG._bz0w')
        image_urls = []
        visited = utils.get_visted_urls()

        scroll_depth = 0
        for i in range(random.randint(1, 4)):
            self.driver.execute_script('window.scrollTo(0, {0});'.format(scroll_depth))
            time.sleep(random.randint(2, 5))
            scroll_depth += random.randint(1, 2000)

        for child in children:
            element = child.find_element_by_tag_name('a')
            url = element.get_attribute(r'href')
            exists = False

            for i in visited:
                if i == url:
                    exists = True
                continue

            if exists == False:
                image_urls.append(url)

        return image_urls

    def _auto_pick_photo(self):
        image_urls = self._auto_get_photos()

        index = random.randint(0, len(image_urls)-1)

        search_url = image_urls[index]

        utils.add_visted_urls(search_url)

        self.driver.get(search_url)

        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'sH9wk._JgwE')))
            return True
        except:
            return False

    def _auto_like_photo(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_8-yf5')))
        children = self.driver.find_elements_by_class_name('_8-yf5')
        for child in children:
            if child.get_attribute('aria-label') != 'Like':
                continue
            if self._auto_comment_on_photo() == True:
                child.click()
                return True
            return False

    def _auto_comment(self, comment_string):
        while True:
            time.sleep(1)
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'Ypffh')))
            element.click()
            time.sleep(1)
            element = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'Ypffh')))
            element.clear()
            time.sleep(random.randint(3, 5))
            element.send_keys(comment_string)
            time.sleep(random.randint(3, 10))
            element.send_keys(Keys.RETURN)
            time.sleep(1)

            try:
                failed_post_path = '/html/body/div[2]/div/div/div/p'
                failed_post = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, failed_post_path)))
                if failed_post and failed_post.text == 'Couldn\'t post comment.':
                    print('failed to post')
                    time.sleep(30)
            except:
                print('posted')
                return True

    def _auto_comment_on_photo(self):
        comment = utils.get_generic_comment()
        print('Current comment is: {}'.format(comment))
        return self._auto_comment(comment)

    def _auto_follow(self):
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sqdOP.yWX7d._8A5w5.ZIAjV')))
        user_url = element.get_attribute('href')
        regex = re.findall(r'.com\/(.+)\/', user_url)
        if regex:
            user = regex[0]
            utils.add_following(user)
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sqdOP.yWX7d.y3zKF')))
        if(element.text == 'Follow'):
            element.click()
