import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class title_contains_not(object):

    def __init__(self, title):
        self.title = title

    def __call__(self, driver):
        return self.title not in driver.title

class CloudflareWebdriver(webdriver.Firefox):

    def _cf_cookies(self):
        cf_cookies = {}
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie['name'] == '__cfduid':
                value = cookie['value']
                cf_cookies['__cfduid'] = value
            elif cookie['name'] == 'cf_clearance':
                value = cookie['value']
                cf_cookies['cf_clearance'] = value
        return cf_cookies

    def _user_agent(self):
        user_agent = self.execute_script('return navigator.userAgent')
        user_agent_ = {'user-agent': user_agent}
        return user_agent_

    def _captcha(self):
        get_captcha_field = self.find_element_by_id("challenge-form")
        get_captcha_field.click()

    def _wait(self, time_=600):
        wait = WebDriverWait(self, time_)
        wait.until(title_contains_not('Cloudflare'))

    def get_cf_data(self, url=None, win_w=500, win_h=700, delay=1):
        self.set_window_size(win_w, win_h)
        self.get(url)
        time.sleep(delay)
        self._captcha()
        self._wait()
        headers = self._user_agent()
        cf_cookies = self._cf_cookies()
        self.quit()
        return headers, cf_cookies
