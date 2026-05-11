from playwright.sync_api import sync_playwright
from threading import Thread
import pandas as pd
import re
import os
import time
import pickle
class PlaywrightAssistantClass:
    def __init__(self):
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False, slow_mo=50 , args=[
            "--disable-blink-features=AutomationControlled"
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-extensions",
            "--start-maximized",
             ])
            self.context = self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1366, "height": 768},
                locale="en-US",
                timezone_id="America/New_York",
            )
            self.context.add_cookies(cookies)
            self.page = self.context.new_page()
            self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    def navigate(self, url):
        self.page.goto(url)
        self.page.evaluate('document.body.style.zoom="25%"')

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    
    def extract_single_element(self, selector, timeout=500, attr='text'):
        try:
            element = self.page.locator(selector).first
            if attr == 'text':
                return element.text_content(timeout=timeout)
            else:
                return element.get_attribute(attr, timeout=timeout)
        except:
            return ""

    def extract_multiple_elements(self, selector, timeout=500, attr='text'):
        try:
            elements = self.page.locator(selector).all()
            results = []
            for element in elements:
                if attr == 'text':
                    results.append(element.text_content(timeout=timeout))
                else:
                    results.append(element.get_attribute(attr, timeout=timeout))
            return results
        except Exception as e:
            print(e)
            return []

    def save_into_file(self, df, filename, state):
        os.makedirs('./scraped_data', exist_ok=True)
        os.makedirs('./scraped_data/'+state, exist_ok=True)
        p = pd.DataFrame([df])
        p.to_csv(f'./scraped_data/{state}/{filename}.csv', mode='a', index=False, header=not os.path.exists(f'./scraped_data/{state}/{filename}.csv'), encoding='utf-8-sig')
        p.to_csv(f'./scraped_data/{state}.csv', mode='a', index=False, header=not os.path.exists(f'./scraped_data/{state}.csv'), encoding='utf-8-sig')


class GoogleMapsScraper(PlaywrightAssistantClass):
    def __init__(self):
        PlaywrightAssistantClass.__init__(self)

    def search_the_keyword(self, keyword):
        search_url = f"https://www.google.com/maps/search/{keyword.replace(' ', '+')}/"
        self.navigate(search_url)
        time.sleep(5)

    def handle_infinite_scroll(self):
        scrollable_div_selector = '//div[contains(@aria-label, "Results for")]'
        scrollable_div = self.page.locator(scrollable_div_selector).first
        previous_height = None
        while True:
            current_height = scrollable_div.evaluate("el => el.scrollHeight")
            if previous_height == current_height:
                break
            previous_height = current_height
            scrollable_div.evaluate("el => el.scrollTo(0, el.scrollHeight)")
            time.sleep(6)

    def get_all_links_of_listing(self):
        selector = "//a[contains(@href, '/maps/place')]"
        links = self.extract_multiple_elements(selector, timeout=2000, attr='href')
        return links

    def extract_required_data_points(self, sk, city, state, linsting_url):
        title = self.extract_single_element(selector='//div[@class="tAiQdd"]//h1', timeout=4000)
        bn = self.extract_single_element(selector='//button[@class="DkEaL "]')
        website = self.extract_single_element(selector='//a[contains(@aria-label, "Website")]', attr='href')
        address = self.extract_single_element(selector='//button[contains(@aria-label, "Address: ")]', attr='aria-label')
        address_city = address.split(", ")[-3] if address else ""
        data = {
            "Searched Keyword": sk,
            "State": state,
            "Company Name": title,
            "Google Adress" : address,
            "City": address_city if address_city else city,
            "Phone": self.extract_single_element(selector='//button[contains(@aria-label, "Phone: ")]', attr='aria-label').removeprefix("Phone: ").strip(),
            "Website": website.split("?")[0] if website else "",
            "Business Niche": bn if bn else sk.lower(),
            "Google Stars": self.extract_single_element(selector='//div[@class="F7nice "]/span[1]/span[1]'),
            "Google Count": self.extract_single_element(selector='(//span[contains(text(),"reviews")] | //div[@class="F7nice "]/span[2]/span[1]/span)[1]', timeout=3000),
            "Website Status": "yes" if website else "no",
            "Listing URL": linsting_url,
            "Contact Source": "Google Maps"
        }
        return data



def implement_threading(serarch_keyword):
    keyword = serarch_keyword.split(' ')[0]
    city = serarch_keyword.split(' ')[-2].replace(',', '')
    state = serarch_keyword.split(' ')[-1]
    bot = GoogleMapsScraper()
    bot.search_the_keyword(serarch_keyword)
    bot.handle_infinite_scroll()
    links = bot.get_all_links_of_listing()
    for l in links:
        bot.navigate(l)
        time.sleep(1.5)
        data = bot.extract_required_data_points(sk=keyword, city=city, state=state, linsting_url=l)
        print("*"*50)
        for k, v in data.items():
            print(f"{k}: {v}")
        print("*"*50)
        bot.save_into_file(df=data, filename=f"{keyword}_{city}_{state}", state=state)
    bot.close()


th1 = Thread(target=implement_threading, args=("Restaurants Lahore, PK", ))
th1.start()
time.sleep(50)
th2 = Thread(target=implement_threading, args=("HVAC Burbank, CA", ))
th2.start()
time.sleep(25)
th3 = Thread(target=implement_threading, args=("HVAC Hollywood, CA", ))
th3.start()
time.sleep(5)
th4 = Thread(target=implement_threading, args=("HVAC Santa Monica, CA", ))
th4.start()
time.sleep(5)
th5 = Thread(target=implement_threading, args=("HVAC Beverly Hills, CA", ))
th5.start()



th1.join()
th2.join()
th3.join()
th4.join()
th5.join()
