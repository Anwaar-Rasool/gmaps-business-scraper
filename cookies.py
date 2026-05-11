import undetected_chromedriver as uc 
import pickle
import time

one_year = 60 * 60 * 24 * 365

driver = uc.Chrome(version_main=145)
driver.get('https://www.google.com')
input("Enter to Exit....")
cookies = driver.get_cookies()
for c in cookies:
    if "expiry" in c:
        c["expiry"] = int(time.time()) + one_year
        print("Expiry Done")

playwright_cookies = []

for cookie in cookies:
    playwright_cookie = {
        "name": cookie.get("name"),
        "value": cookie.get("value"),
        "domain": cookie.get("domain"),
        "path": cookie.get("path", "/"),
        "expires": cookie.get("expiry", -1),
        "httpOnly": cookie.get("httpOnly", False),
        "secure": cookie.get("secure", False),
        "sameSite": "Lax"   # default set kar do
    }
    playwright_cookies.append(playwright_cookie)

with open("cookies.pkl", "wb") as cook:
    pickle.dump(playwright_cookies, cook)
    cook.close()