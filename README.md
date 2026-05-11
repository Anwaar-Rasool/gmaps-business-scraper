# 🗺️ Google Maps Business Scraper

A multi-threaded Google Maps scraper built with **Playwright** that extracts business data (name, address, phone, website, ratings, and more) from Google Maps listings. It uses browser cookies for session persistence and saves scraped data to organized CSV files.

---

## 📁 Project Structure

```
google-maps-scraper/
│
├── google_maps.py        # Main scraper logic and threading
├── cookies.py            # Cookie extraction and serialization script
├── cookies.pkl           # Saved browser session cookies (auto-generated)
└── scraped_data/         # Output directory (auto-generated)
    ├── <State>.csv       # Aggregated CSV per state
    └── <State>/
        └── <keyword>_<city>_<state>.csv   # CSV per keyword-city combo
```

---

## ✨ Features

- **Anti-detection**: Disables `navigator.webdriver`, sets a realistic user-agent, viewport, locale, and timezone.
- **Cookie-based session**: Reuses Google browser cookies to avoid login prompts and CAPTCHAs.
- **Infinite scroll handling**: Automatically scrolls the results panel until all listings are loaded.
- **Multi-threaded scraping**: Runs multiple keyword-city searches in parallel using Python threads.
- **Structured CSV output**: Saves data both per city and aggregated per state.
- **Extracted data points**: Business name, address, city, phone, website, niche, Google stars, review count, listing URL, and more.

---

## 🔧 Requirements

### Python Version
- Python 3.8+

### Dependencies

Install via pip:

```bash
pip install playwright pandas undetected-chromedriver
playwright install chromium
```

| Package                  | Purpose                              |
|--------------------------|--------------------------------------|
| `playwright`             | Browser automation for scraping      |
| `pandas`                 | CSV file creation and management     |
| `undetected-chromedriver`| Cookie extraction without detection  |
| `pickle`                 | Cookie serialization                 |

---

## 🚀 Getting Started

### Step 1 — Extract & Save Cookies

Before scraping, you must capture a valid Google session using `cookies.py`. This opens a real Chrome browser window, lets you log in or interact with Google, then saves the cookies.

```bash
python cookies.py
```

> Once the browser opens and Google loads, press **Enter** in the terminal to save the cookies and exit.

This generates a `cookies.pkl` file that `google_maps.py` will load automatically.

---

### Step 2 — Run the Scraper

```bash
python google_maps.py
```

The script launches multiple threads, each targeting a different keyword-city combination:

| Thread | Search Keyword              |
|--------|-----------------------------|
| th1    | HVAC California City, CA      |
| th2    | HVAC Burbank, CA            |
| th3    | HVAC Hollywood, CA          |
| th4    | HVAC Santa Monica, CA       |
| th5    | HVAC Beverly Hills, CA      |

---

## ⚙️ Configuration

### Changing Search Keywords

In `google_maps.py`, modify the `Thread` calls at the bottom:

```python
th1 = Thread(target=implement_threading, args=("Plumbers New York, NY", ))
th2 = Thread(target=implement_threading, args=("Dentists Chicago, IL", ))
```

**Keyword format:** `"<Business Type> <City>, <State/Country>"`

### Thread Delays

`time.sleep()` calls between thread starts prevent simultaneous browser launches from crashing:

```python
th1.start()
time.sleep(10)   # Wait before launching next thread
th2.start()
```

Adjust these delays based on your system's available RAM and CPU.

---

## 📊 Output Data Format

Each CSV row contains the following fields:

| Field            | Description                              |
|------------------|------------------------------------------|
| `Searched Keyword` | The business type searched (e.g., HVAC) |
| `State`          | State/country code from the keyword      |
| `Company Name`   | Business name from Google Maps           |
| `Google Address` | Full address string                      |
| `City`           | Extracted or inferred city               |
| `Phone`          | Business phone number                    |
| `Website`        | Business website URL (cleaned)           |
| `Business Niche` | Category button text or keyword fallback |
| `Google Stars`   | Average star rating                      |
| `Google Count`   | Number of reviews                        |
| `Website Status` | `yes` if website exists, `no` otherwise  |
| `Listing URL`    | Full Google Maps listing URL             |
| `Contact Source` | Always `"Google Maps"`                   |

**Output paths:**
- `./scraped_data/<State>/<keyword>_<city>_<state>.csv` — Per city file
- `./scraped_data/<State>.csv` — Aggregated state-level file

---

## 🏗️ Architecture Overview

```
cookies.py
    └── Opens Chrome via undetected-chromedriver
    └── Captures & serializes cookies → cookies.pkl

google_maps.py
    ├── PlaywrightAssistantClass       # Base browser controller
    │   ├── __init__()                 # Load cookies, launch Chromium
    │   ├── navigate(url)              # Go to URL + zoom out
    │   ├── extract_single_element()   # Get one element's text/attr
    │   ├── extract_multiple_elements()# Get list of elements
    │   └── save_into_file()           # Append row to CSV
    │
    ├── GoogleMapsScraper              # Scraper logic (extends base)
    │   ├── search_the_keyword()       # Open Maps search URL
    │   ├── handle_infinite_scroll()   # Scroll until all results load
    │   ├── get_all_links_of_listing() # Collect all listing hrefs
    │   └── extract_required_data_points() # Parse each listing page
    │
    └── implement_threading(keyword)   # Orchestrates one full scrape job
        └── Called in parallel via Thread()
```

---

## ⚠️ Notes & Limitations

- **Headless mode is disabled** (`headless=False`) to reduce bot detection. You will see browser windows open during scraping.
- **Cookie expiry** is set to 1 year from extraction time in `cookies.py`.
- Scraping Google Maps may violate [Google's Terms of Service](https://policies.google.com/terms). Use responsibly and only for permitted use cases.
- If Google shows a CAPTCHA, re-run `cookies.py` to refresh cookies.
- The `time.sleep()` values in `implement_threading` and the scroll loop may need tuning depending on network speed.

---

## 📌 Example Usage

```python
# Add a new search in google_maps.py
th6 = Thread(target=implement_threading, args=("Electricians Austin, TX", ))
th6.start()
th6.join()
```

---

## 👤 Author

**Muhammad Anwaar Rasool**  
Automation & Web Scraping Engineer

---

## 📄 License

This project is for educational and personal use only. The author is not responsible for any misuse of this tool.
