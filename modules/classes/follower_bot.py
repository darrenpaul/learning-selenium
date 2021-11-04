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


class FollowerBot:
    def __init__(self) -> None:
        self.tags = utils.get_search_tags()

    def get_followers(self):
        for tag in self.tags:
            try:
                search_url = 'explore/tags/{0}'.format(tag)
                self.driver.get('https://www.instagram.com/{0}'.format(search_url))
                if not self._pick_photo():
                    continue
                if self._like_photo():
                    self._follow()
            except Exception as e:
                print(e)
                continue

    def _get_photos(self) -> list:
        children = self.driver.find_elements_by_class_name('v1Nh3.kIKUG._bz0w')
        image_urls = []
        visited = utils.get_visted_urls()

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

    def _pick_photo(self):
        image_urls = self._get_photos()

        print('\n--- How to use ---\n')
        print('Options:')
        print('-'*20)
        print('y --> Yes select photo to like')
        print('n --> No move to next photo')
        print('q --> Quit picking current photo\n')

        index = random.randint(0, len(image_urls)-1)

        while True:
            search_url = image_urls[index]

            utils.add_visted_urls(search_url)

            self.driver.get(search_url)

            raw_input = input('Pick current photo? ')
            if raw_input == 'y':
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'sH9wk._JgwE')))
                    return True
                except:
                    return False
            elif raw_input == 'n':
                index = random.randint(0, len(image_urls)-1)
                continue
            elif raw_input == 'q':
                return False
            else:
                print('ERROR: invalid option please try again')

    def _like_photo(self):
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_8-yf5')))
        children = self.driver.find_elements_by_class_name('_8-yf5')
        for child in children:
            if child.get_attribute('aria-label') != 'Like':
                continue
            if self._comment_on_photo() == True:
                child.click()
                return True
            return False

    def _comment(self, comment_string):
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Ypffh')))
        element.click()
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'Ypffh')))
        element.clear()
        element.send_keys(comment_string)
        time.sleep(2)
        element.send_keys(Keys.RETURN)
        time.sleep(3)

    def _comment_on_photo(self):
        print('\n--- How to use ---\n')
        print('Options:')
        print('-'*20)
        print('y --> Yes apply comment to photo')
        print('n --> No don\'t comment on photo')
        print('s --> Shuffle to get new comment')
        print('c --> Write custom comment\n')
        while True:
            comment = utils.get_comment()
            print('Current comment is: {}'.format(comment))
            raw_input = input(
                'Comment on photo? ')
            if raw_input == 'y':
                self._comment(comment)
                return True
            elif raw_input == 'n':
                return False
            elif raw_input == 's':
                continue
            elif raw_input == 'c':
                custom_raw_input = input('Enter custom comment: ')
                comment = custom_raw_input.strip()
                self._comment(comment)
                return True
            else:
                print('ERROR: invalid option please try again')

    def _follow(self):
        element = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sqdOP.yWX7d._8A5w5.ZIAjV')))
        user_url = element.get_attribute('href')

        regex = re.findall(r'.com\/(.+)\/', user_url)

        user = ''

        if regex:
            user = regex[0].strip()
            utils.add_following(user)

        removed = False
        for u in utils.get_removed_following():
            _user = u.split('  ')[0]
            if _user != user:
                continue
            removed = True
            break

        if removed == False:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'sqdOP.yWX7d.y3zKF')))
            if(element.text == 'Follow'):
                element.click()
