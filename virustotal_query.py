from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

WAIT_TIME = 5
HASH_TIMEOUT = 10
UPLOAD_TIMEOUT = 300
ANALYSIS_TIMEOUT = 300

def initDriver():
    WINDOW_SIZE = "1000,2000"
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None  # Windows workaround
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-feature=IsolateOrigins,site-per-process")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--ignore-certificate-error-spki-list")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    chrome_options.add_argument('disable-infobars')

    driver = webdriver.Chrome(options=chrome_options)
    return driver



def find_element(driver, selectors):
    def expand_shadow_element(driver, element):
        return driver.execute_script('return arguments[0].shadowRoot', element)
    element = driver.find_element(By.CSS_SELECTOR,selectors[0])
    for selector in selectors[1:]:
        element = expand_shadow_element(driver, element) or element
        element = element.find_element(By.CSS_SELECTOR,selector)
    return element


def wait_for_elem(driver, selectors, timeout = WAIT_TIME):
    try:
        return WebDriverWait(driver, timeout).until(lambda driver: find_element(driver, selectors))
    except:
        raise RuntimeError(f"Element not found: {selectors}")



driver = initDriver()

link = "https://www.virustotal.com/gui/home/search/"

data = open("md5hash.txt", "r").read().split("\n")

result =[]
for itemhash in data:
    try: 
        driver.get(link)
        input = wait_for_elem(driver, ['home-view', 'vt-ui-search-bar', '#searchInput'])
        input.send_keys(itemhash)
        input.send_keys(Keys.ENTER)
        
        file_id_element = wait_for_elem(driver, ['file-view', 'vt-ui-file-card', '.hstack.gap-2.fw-bold'])
        WebDriverWait(driver, WAIT_TIME).until(lambda x: file_id_element.text != '')
        file_name = wait_for_elem(driver, ['file-view', 'vt-ui-file-card', '.file-name.text-truncate'])
        WebDriverWait(driver, WAIT_TIME).until(lambda x: file_name.text != '')
        temp = file_id_element.text
        print(itemhash, temp, file_name.text)
        result.append(temp)
        sleep(1)
    except Exception as e:
        print(e)
    
print(result)

