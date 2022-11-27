import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pymysql

conn = pymysql.connect(host='15.164.192.100', port=52817, user='caps', password='1234', charset='utf8')

work_name_list = []
work_name_list2 = []
lecture_name = []
work_link_list = []
section_list = []

cur = conn.cursor()
cur.execute('use caps')
cur.execute('select distinct work_name from jobs')

row = cur.fetchone()

while row:
    work_name_list.append(row[0])
    row = cur.fetchone()

options = webdriver.ChromeOptions()
# options.add_argument('--blink-settings=imagesEnabled=false')
# options.add_argument('disable-gpu')

driver = webdriver.Chrome('chromedriver', options=options)
# driver.minimize_window()

driver.implicitly_wait(2)

main_address = 'https://www.inflearn.com/'
driver.get(main_address)

driver.find_element(By.CSS_SELECTOR, '#header > nav > div.container.mobile_container > div > div.mobile_left > span > svg').click()
time.sleep(0.5)

driver.find_element(By.CSS_SELECTOR, '#root > aside > div.category-content > div.menu_list > div:nth-child(1)').click()
time.sleep(0.5)

w = driver.find_element(By.CSS_SELECTOR, '#courses_section > div > div > div > header > div > input')

for i in range(len(work_name_list)):
    w.clear()
    w.send_keys(str(work_name_list[i]))

    try:
        driver.find_element(By.CSS_SELECTOR, '#courses_section > div > div > div > header > div > button').click()
        time.sleep(1)

        cols = driver.find_elements(By.CSS_SELECTOR, '#courses_section > div > div > div > main > div.courses_container > div > div')

        for col in cols[:3]:
            coll = col.find_element(By.CSS_SELECTOR, 'div > a')
            colink = coll.get_attribute('href')

            lecture_name.append(coll.find_element(By.CSS_SELECTOR, 'div.card-content > div.course_title').text)
            work_name_list2.append(work_name_list[i])
            work_link_list.append(colink)

            driver.execute_script('window.open("");')
            driver.switch_to.window(driver.window_handles[1])
            driver.get(colink)
            time.sleep(0.5)

            secs = driver.find_elements(By.CSS_SELECTOR, '#curriculum > div.cd-curriculum__content > div > div')
            ln = ''
            for sec in secs:
                ln = ln + '\n' + sec.find_element(By.CSS_SELECTOR, 'div > div > span[class=cd-accordion__section-title]').text

            section_list.append(ln)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    except NoSuchElementException:
        pass



for j in range(len(work_name_list2)):
    cur.execute('INSERT INTO learn (Num, work_name, lecture_name, work_link, section) VALUES (%s, %s, %s, %s, %s)', (j + 1, work_name_list2[j], lecture_name[j], work_link_list[j], section_list[j]))
    conn.commit()

conn.close()

print("complete")

