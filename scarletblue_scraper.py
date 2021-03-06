#!/usr/bin/env python3

"""This script scrapes the website https://scarletblue.com.au/ for data
and outputs the result in the .xls file.
"""

import xlwt
import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from cloudflare_handler import CloudflareWebdriver

class Scarletblue(scrapy.Spider):
    """Class defines all the attributes and methods required to scrape
    data from the given website and out the results in the .xls file.
    """

    name = "scarletblue"
    url = "https://scarletblue.com.au/"
    driver = CloudflareWebdriver()
    headers, cookies = driver.get_cf_data(url)
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("scarletblue")
    sheet.col(0).width = 256 * 5
    sheet.col(1).width = 256 * 25
    sheet.col(2).width = 256 * 50
    sheet.col(3).width = 256 * 15
    sheet.col(4).width = 256 * 15
    sheet.col(5).width = 256 * 40
    sheet.col(6).width = 256 * 255
    areas_and_cities = []
    row_counter = 1

    def start_requests(self):
        """Standard Scrapy method to start scraping."""
        self.sheet.write(0, 0, "Area")
        self.sheet.write(0, 1, "City")
        self.sheet.write(0, 2, "Name")
        self.sheet.write(0, 3, "Age")
        self.sheet.write(0, 4, "Phone")
        self.sheet.write(0, 5, "E-mail")
        self.sheet.write(0, 6, "Social")
        yield scrapy.Request(url=self.url, 
                            callback=self.parse_areas_for_cities,
                            cookies=self.cookies,
                            headers=self.headers
                            )

    def parse_areas_for_cities(self, response):
        """Get a list of cities in an area and produce further
        requests.
        """
        area_list = response.css("div.hide::attr(data-citymenutarget)")\
                                                                .extract()
        for area in area_list:
            self.areas_and_cities.append((
            area,
            response.css(f"div.hide[data-citymenutarget={area}]>ul>\
                                                li>a::attr(href)").extract()
            ))
        for area_and_cities in self.areas_and_cities:
            for link in area_and_cities[1]:
                yield scrapy.Request(url=link, 
                                    callback=self.parse_cities_for_escorts,
                                    cookies=self.cookies,
                                    headers=self.headers,
                                    meta={'area': area_and_cities[0]}
                                    )

    def parse_cities_for_escorts(self, response):
        """Get a list of persons for a city and produce further
        requests.
        """
        area = response.meta['area']
        escort_links = response.css("div.profile-image-cities:not(.signup)>\
                                    a:not(.favgirl):not(.signup)\
                                            ::attr(href)").extract()
        for link in escort_links:
            yield scrapy.Request(url=link,
                                callback=self.parse_escort_for_data,
                                cookies=self.cookies,
                                headers=self.headers,
                                meta={'area': area}
                                )
    
    def parse_escort_for_data(self, response):
        """Scrape all the required data from the profile and
        output the result in the .xls file.
        """
        area = response.meta['area']
        name = response.css("div.col-lg-12>header>h1::text")\
                                                    .extract_first().strip()
        location = response.css("p.list-group-item-text::text")\
                                                    .extract_first().title()
        age = response.css("p.list-group-item-text::text")\
                                                    .extract()[1]
        phone = response.css("p.list-group-item-text::text")\
                                                    .extract()[2]
        if response.css("a#Profile-Details.email::text")\
                                                    .extract_first() is None:
            email = "Not available"
        else:
            email = response.css("a#Profile-Details.email::text")\
                                                    .extract_first()
        if not response.css("ul.list-group.list-inline>li>div>p>\
                            a:not(a[data-toggle='modal']):not(.email)\
                                            ::attr(href)").extract():
            social = "Not specified"
        else:
            social = response.css("ul.list-group.list-inline>li>div>p>\
                                  a:not(a[data-toggle='modal']):not(.email)\
                                            ::attr(href)").extract()
        self.sheet.write(self.row_counter, 0, area)
        self.sheet.write(self.row_counter, 1, location)
        self.sheet.write(self.row_counter, 2, name)
        self.sheet.write(self.row_counter, 3, age)
        self.sheet.write(self.row_counter, 4, phone)
        self.sheet.write(self.row_counter, 5, email)
        self.sheet.write(self.row_counter, 6, str(social))
        self.row_counter += 1
        self.book.save("scarletblue.xls")

def main():
    """The function called upon script execution."""
    runner = CrawlerRunner()
    print("Fetching data...")
    d = runner.crawl(Scarletblue)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    print("Data written to scarletblue.xls")
    print("Done!")

if __name__ == '__main__':
    main()
