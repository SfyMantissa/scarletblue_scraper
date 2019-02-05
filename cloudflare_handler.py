"""This module defines classes used for Cloudflare-protected website
scraping automation.
"""

import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class title_contains_not(object):
    """A custom wait.until() condtion class."""

    def __init__(self, title):
        """Defines the self.title string to be looked for in a string
        webdriver.title string.
        """
        self.title = title

    def __call__(self, driver):
        """Defines the action upon call."""
        return self.title not in driver.title

class CloudflareWebdriver(webdriver.Firefox):
    """Class defines methods required to open a window with CAPTCHA and
    fetch Cloudflare session cookies and Firefox user-agent after a
    valid CAPTCHA is submitted to store them in Python dictionaries.
    """

    def _cf_cookies(self):
        """Fetch cookies."""
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
        """Fetch user-agent."""
        user_agent = self.execute_script('return navigator.userAgent')
        user_agent_ = {'user-agent': user_agent}
        return user_agent_

    def _captcha(self):
        """Select and autoclick CAPTCHA checkbox."""
        get_captcha_field = self.find_element_by_id("challenge-form")
        get_captcha_field.click()

    def _wait(self, time_=600):
        """Wait until document title no longer contains string
        'Cloudflare'.
        """
        wait = WebDriverWait(self, time_)
        wait.until(title_contains_not('Cloudflare'))

    def get_cf_data(self, url=None, win_w=500, win_h=700, delay=1):
        """Assemble all 'private' methods into a sequence of calls and
        return headers and cf_cookies dictionaries.
        """
        self.set_window_size(win_w, win_h)
        self.get(url)
        time.sleep(delay)
        self._captcha()
        self._wait()
        headers = self._user_agent()
        cf_cookies = self._cf_cookies()
        self.quit()
        return headers, cf_cookies
