from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import json
import os

sleep_delay = 2  # enter 5 for slow internet
timeout = 5  # enter 40 for slow internet
max_parti = live_parti = 0
min_parti = 70

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)


def wait_find_by_id(id, timeout):
    time.sleep(sleep_delay)
    for i in range(timeout):
        try:
            ele = driver.find_element_by_id(id)
        except:
            time.sleep(sleep_delay)
        else:
            return ele


def wait_find_by_linktext(text, timeout):
    time.sleep(sleep_delay)
    for i in range(timeout):
        try:
            ele = driver.find_element_by_link_text(text)
        except:
            time.sleep(sleep_delay)
        else:
            return ele


def wait_find_by_xpath(xpath, timeout):
    time.sleep(sleep_delay)
    for i in range(timeout):
        try:
            ele = driver.find_element_by_xpath(xpath)
        except:
            time.sleep(sleep_delay)
        else:
            return ele


def wait_find_ELEMENTS_by_xpath(xpath, timeout):
    time.sleep(sleep_delay)
    for i in range(timeout):
        try:
            ele = driver.find_elements_by_xpath(xpath)
        except:
            time.sleep(sleep_delay)
        else:
            return ele


def join_meeting():
    global max_parti, live_parti

    join_arr = wait_find_ELEMENTS_by_xpath('//button[.="Join"]', 3)
    join_arr[0].click()  # first join button
    ele = wait_find_by_xpath(
        '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button', timeout)

    if ele.get_attribute('aria-pressed') == 'true':  # turn off camera
        ele.click()
    ele = wait_find_by_xpath(
        '//*[@id="preJoinAudioButton"]/div/button', timeout)
    if ele.get_attribute('aria-pressed') == 'true':  # turn off microphone
        ele.click()
    wait_find_by_xpath('//button[.="Join now"]', timeout).click()

    print(f"Success at {(datetime.now())}")
    time.sleep(60*5)
    actions = ActionChains(driver)
    button = wait_find_by_xpath('//button[@id="roster-button"]', timeout)
    actions.move_to_element(button).click().perform()
    temp_parti = wait_find_ELEMENTS_by_xpath(
        '//span[@class="toggle-number"][@ng-if="::ctrl.enableRosterParticipantsLimit"]')
    max_parti = live_parti = int(temp_parti[1].text[1:-1])


def hangup():
    global live_parti, max_parti, min_parti
    hangup_button = wait_find_by_xpath('//button[@id="hangup-button"]', 3)
    temp_parti = wait_find_ELEMENTS_by_xpath(
        '//span[@class="toggle-number"][@ng-if="::ctrl.enableRosterParticipantsLimit"]')

    if len(temp_parti) > 1:
        live_parti = int(temp_parti[1].text[1:-1])
    else:
        actions = ActionChains(driver)
        actions.move_to_element(wait_find_by_xpath(
            '//button[@id="roster-button"]', timeout)).click().perform()

    max_parti = max(max_parti, live_parti)
    if live_parti < min_parti and live_parti != 0:
        hangup_button = wait_find_by_xpath('//button[@id="hangup-button"]', 3)
        actions = ActionChains(driver)
        actions.move_to_element(hangup_button).click().perform()
        print(f"Hangup at {(datetime.now())}")
        # open calendar again
        driver.get('https://teams.microsoft.com/_#/calendarv2')
        driver.refresh()
        time.sleep(5)

    if hangup_button == None:
        max_parti = live_parti = 0
        driver.get('https://teams.microsoft.com/_#/calendarv2')
        driver.refresh()
        time.sleep(5)
        join_meeting()


#login code


def init():
    global min_parti
    # open calendar tab in teams
    driver.get('https://teams.microsoft.com/_#/calendarv2')
    time.sleep(1)
    with open(os.path.join(os.path.curdir, 'cred.json')) as f:
        data = json.load(f)
    min_parti = data['min_parti']

    wait_find_by_id('i0116', timeout).send_keys(
        data['username'])       # enter username
    print("hahaha")
    wait_find_by_id('idSIButton9', timeout).click(
    )                    # click next
    wait_find_by_id('i0118', timeout).send_keys(
        data['password'])      # enter password
    wait_find_by_id('idSIButton9', timeout).click(
    )                    # click next
    # click yes to stay signed in
    wait_find_by_id('idSIButton9', timeout).click()
    wait_find_by_linktext('Use the web app instead', timeout).click()
    time.sleep(10)
    # change calender work-week view to day view
    while wait_find_by_xpath('//button[@title="Switch your calendar view"]', timeout).get_attribute('name') != "Day":
        wait_find_by_xpath(
            '//button[@title="Switch your calendar view"]', timeout).click()
        wait_find_by_xpath('//button[@name="Day"]', timeout).click()
    print(f"Login at {(datetime.now())}")
    join_meeting()


def main():
    global driver
    try:
        init()
    except:
        print('init failed, trying again')
        main()
    else:
        while True:
            try:
                hangup()
            except:
                print('join meeting failed, trying again')
                driver.get('https://teams.microsoft.com/_#/calendarv2')

            else:
                time.sleep(10)

# driver code


if __name__ == "__main__":
    main()
