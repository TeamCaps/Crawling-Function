import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pymysql

conn = pymysql.connect(host='15.164.192.100', port=52817, user='caps', password='1234', charset='utf8')

cur = conn.cursor()
cur.execute('use caps')
#sql = 'INSERT INTO jobs ' #(cp_name, work_link, cp_logo, work_name, skill, intro_work, prefer, Num) VALUES (%s, %s, %s, %s, %s, %s, %s, %d)'

options = webdriver.ChromeOptions()
# options.add_argument('--blink-settings=imagesEnabled=false')
# options.add_argument('disable-gpu')

driver = webdriver.Chrome('chromedriver', options=options)
driver.minimize_window()

work_name_list = []
work_link_list = []
cp_name_list = []
cp_logo_list = []
skill_list = []
intro_work_list = []
prefer_list = []
summary_list = []


driver.implicitly_wait(1)

main_address = 'https://career.programmers.co.kr/job?page=1&order=recent' #1 2 4 5 11 12 16 22
driver.get(main_address)

driver.find_element(By.CSS_SELECTOR, '#search-form > div.list-forms.job-position-search > div.form-group.form-category').click()
time.sleep(1)

works = driver.find_elements(By.CSS_SELECTOR, '#search-form > div.list-forms.job-position-search > div.form-group.form-category.show > div > ul > li')

for work in works:
    work_name = work.find_element(By.CSS_SELECTOR, 'label')
    work_name.find_element(By.CSS_SELECTOR, 'input[type=checkbox]').click()
    time.sleep(1)
    pos = driver.find_elements(By.CSS_SELECTOR, '#list-positions-wrapper > ul > li')
    for po in pos:
        work_name_list.append(work_name.text)
        cp_name_list.append(po.find_element(By.CSS_SELECTOR, 'div.item-body > h6 > a').text)
        cp_logo_list.append(po.find_element(By.CLASS_NAME,'company-logo').get_attribute('src'))
        link = po.find_element(By.CSS_SELECTOR, 'div.item-body > div.position-title-wrapper > h5 > a').get_attribute('href')
        work_link_list.append(link)
        driver.execute_script('window.open("");')
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)

        try:
            llll = driver.find_element(By.CSS_SELECTOR, 'body > div.main > div > div.container.container-position-show > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8')

            sumas = llll.find_elements(By.CSS_SELECTOR, 'section.section-summary > table > tbody > tr')
            lns = ''
            for suma in sumas:
                ln = suma.find_element(By.CSS_SELECTOR, 'td.t-label').text + ' : ' + suma.find_element(By.CSS_SELECTOR, 'td.t-content').text
                lns = lns + '\n' + ln

            summary_list.append(lns)

            try:
                skill_list.append(llll.find_element(By.CSS_SELECTOR, 'section.section-stacks > ul').text)
            except NoSuchElementException:
                skill_list.append(' ')

            try:
                intro_work_list.append(llll.find_element(By.CSS_SELECTOR, 'section.section-position > div').text)
            except NoSuchElementException:
                intro_work_list.append(' ')

            try:
                prefer_list.append(llll.find_element(By.CSS_SELECTOR, 'section.section-preference > div').text)
            except NoSuchElementException:
                prefer_list.append(' ')

        except NoSuchElementException:
            skill_list.append(' ')
            intro_work_list.append(' ')
            prefer_list.append(' ')

        driver.close()
        driver.switch_to.window(driver.window_handles[0])


    work.find_element(By.CSS_SELECTOR, 'label > input[type=checkbox]').click()
    time.sleep(0.5)



for i in range(len(summary_list)):
    cur.execute('INSERT INTO jobs (cp_name, work_link, cp_logo, work_name, skill, intro_work, prefer, Num, cp_preview) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (cp_name_list[i], work_link_list[i], cp_logo_list[i], work_name_list[i], skill_list[i], intro_work_list[i], prefer_list[i], i + 1, summary_list[i]))
    conn.commit()



conn.close()

print("complete")

