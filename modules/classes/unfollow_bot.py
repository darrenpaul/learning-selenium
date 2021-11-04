from modules import utils
from datetime import datetime, timedelta
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UnfollowBot:
    def __init__(self) -> None:
        self.followers = []

    def get_all_users(self):
        self.followers = utils.get_following()

    def unfollow_users(self):
        remaining = []
        self.get_all_users()
        for item in self.followers:
            user, added_date = item.split('  ')
            date_limit = datetime.today() - timedelta(days=1)
            added_date = datetime.strptime(added_date, "%Y-%m-%d")
            if date_limit > added_date:
                print('Unfollowing {0}'.format(user))
                if self.unfollow_user(user):
                    utils.add_removed_following(user)
                time.sleep(10)
                self.unfollow_user(user)
                continue
            remaining.append(user)
        utils.remove_all_followings()
        for user in remaining:
            utils.add_following(user)

    def unfollow_user(self, user_string: str):
        try:
            self.driver.get('https://www.instagram.com/{0}/'.format(user_string))

            unfollow_path = r'/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div/span'
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, unfollow_path))
            ).click()

            button_path = r'/html/body/div[5]/div/div/div/div[3]/button[1]'
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, button_path))
            ).click()

            time.sleep(30)
            return True
        except:
            return False
