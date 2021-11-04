from modules import utils, setup_driver
from modules.classes import unfollow_bot, follower_bot, auto_follower_bot

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramBot(unfollow_bot.UnfollowBot, follower_bot.FollowerBot, auto_follower_bot.AutoFollowerBot):

    def __init__(self) -> None:
        unfollow_bot.UnfollowBot.__init__(self)
        follower_bot.FollowerBot.__init__(self)
        auto_follower_bot.AutoFollowerBot.__init__(self)

        self.email = ''
        self.password = ''
        self.driver = None

        self._get_credentials()

    def _get_credentials(self):
        data = utils.get_user_credentials()
        self.email = data['email']
        self.password = data['password']

    def login(self):
        self.driver.get('https://www.instagram.com/?hl=en')

        # Enter user email into input
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="username"]'))).send_keys(self.email)

        # Enter user password into input
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="password"]')))

        # Add password to input
        element.send_keys(self.password)

        # Simulate pressing the enter key
        element.send_keys(Keys.RETURN)

        print('Successfully logged in user')

    def clear_login_popups(self):
        # Wait for element to be present
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'XTCLo.x3qfX')))

        # Click Not Now button
        self.driver.find_element_by_xpath('//button[text()="Not Now"]').click()

        # element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'aOOlW.HoLwm')))
        # element.click()

        print('Successfully cleared popups')

    def setup_driver(self):
        self.driver = setup_driver.setup()

    def get_options(self):
        print('\n--- How to use ---\n')
        print('Type any of the available options followed but the enter key.\nunfollow <enter key press>')
        print('\nAvailable Options:')
        print('-'*20)
        print('options')
        print('follower or 1')
        print('auto follower or 2')
        print('unfollow or 3')
        print('quit\n\n')

    def get_user_input(self):
        self.get_options()
        self.setup_driver()
        self.login()
        self.clear_login_popups()
        try:
            while True:
                raw_input = ''
                raw_input = input('Enter a option: ')
                raw_input = raw_input.strip().lower()
                print(raw_input)
                if raw_input == 'follower' or raw_input == '1':
                    self.get_followers()
                if raw_input == 'auto follower' or raw_input == '2':
                    self.get_auto_followers()
                elif raw_input == 'unfollow' or raw_input == '3':
                    print('running unfollow operation...')
                    self.unfollow_users()
                elif raw_input == 'options':
                    self.get_options()
                elif raw_input == 'quit':
                    self.driver.quit()
                    quit()
                else:
                    print('ERROR: invalid option please try again')
        except:
            self.driver.quit()
