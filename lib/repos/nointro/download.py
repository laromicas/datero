from pathlib import Path
import os
import profile
import time
import random

from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By


TMP_FOLDER = f"{os.getcwd()}/tmp/nointro"


def execute_with_retry(method, max_attempts):
    e = None
    for i in range(0, max_attempts):
        try:
            return method()
        except Exception as e:
            print(e)
            time.sleep(1)
    if e is not None:
        raise e


def sleep_time():
    time.sleep(random.randint(1, 6))



# def waitUntilDownloadCompleted(maxTime=600):
#     driver.execute_script("window.open()")
#     # switch to new tab
#     driver.switch_to.window(driver.window_handles[-1])
#     # navigate to chrome downloads
#     # driver.get('chrome://downloads')
#     driver.get('about:downloads')
#     # define the endTime
#     endTime = time.time() + maxTime
#     while True:
#         try:
#             # get the download percentage
#             downloadPercentage = driver.execute_script(
#                 "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
#             # check if downloadPercentage is 100 (otherwise the script will keep waiting)
#             if downloadPercentage == 100:
#                 # exit the method once it's completed
#                 return downloadPercentage
#         except:
#             pass
#         # wait for 1 second before checking the percentage next time
#         time.sleep(1)
#         # exit method if the download not completed with in MaxTime.
#         if time.time() > endTime:
#             break


def is_download_finished():
    firefox_temp_file = sorted(Path(TMP_FOLDER).glob('*.part'))
    chrome_temp_file = sorted(Path(TMP_FOLDER).glob('*.crdownload'))
    downloaded_files = sorted(Path(TMP_FOLDER).glob('*.*'))
    if (len(firefox_temp_file) == 0) and \
       (len(chrome_temp_file) == 0) and \
       (len(downloaded_files) >= 1):
        return True
    else:
        return False

def download_daily():

    options = FirefoxOptions()
    options.add_argument("--headless")
    options.set_capability("marionette", True)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", TMP_FOLDER)
    options.set_preference("browser.download.folderList", 2)

    driver = webdriver.Firefox(options=options)

    driver.implicitly_wait(10)
    driver.get("https://www.google.com")

    driver.get("https://datomatic.no-intro.org")

    sleep_time()
    # driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS)
    text = 'Download'
    download_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Download')]")
    download_button.click()

    sleep_time()
    daily_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Daily')]")
    daily_link.click()

    sleep_time()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    prepare_button = driver.find_element(By.CSS_SELECTOR, "form[name='daily'] input[type='submit']")

    sleep_time()
    prepare_button.click()

    sleep_time()
    download_button = driver.find_element(By.CSS_SELECTOR, "form[name='opt_form'] input[name='lazy_mode']")
    download_button.click()

    while not is_download_finished():
        print("Waiting for download to finish")
        time.sleep(10)

    driver.close()

if __name__ == '__main__':
    download_daily()