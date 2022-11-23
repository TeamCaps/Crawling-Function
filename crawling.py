import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('chromedriver', options=options)
driver.minimize_window()

work_name_list = []
work_link_list = []
cp_name_list = []
skill_list = []
intro_work_list = []
prefer_list = []

driver.implicitly_wait(5)

main_address = 'https://career.programmers.co.kr/job?page=1&order=recent' #1 2 4 5 11 12 16 22
driver.get(main_address)

driver.find_element(By.CSS_SELECTOR, '#search-form > div.list-forms.job-position-search > div.form-group.form-category').click()
time.sleep(1)

works = driver.find_elements(By.CSS_SELECTOR, '#search-form > div.list-forms.job-position-search > div.form-group.form-category.show > div > ul > li')

for work in works:
    work.find_element(By.CSS_SELECTOR, 'label > input[type=checkbox]').click()
    time.sleep(1)
    pos = driver.find_elements(By.CSS_SELECTOR, '#list-positions-wrapper > ul > li')
    for po in pos[:5]:
        work_name_list.append(po.find_element(By.CSS_SELECTOR, 'div.item-body > div.position-title-wrapper > h5 > a').text)
        cp_name_list.append(po.find_element(By.CSS_SELECTOR, 'div.item-body > h6 > a').text)
        link = po.find_element(By.CSS_SELECTOR, 'div.item-body > div.position-title-wrapper > h5 > a').get_attribute('href')
        work_link_list.append(link)
        driver.execute_script('window.open("");')
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)

        llll = driver.find_element(By.CSS_SELECTOR, 'body > div.main > div > div.container.container-position-show > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8')

        try:
            skill_list.append(llll.find_element(By.CSS_SELECTOR, 'section.section-stacks > ul').text)
        except NoSuchElementException:
            skill_list.append(' ')

        intro_work_list.append(llll.find_element(By.CSS_SELECTOR, 'section.section-position > div').text)
        prefer_list.append(llll.find_element(By.CSS_SELECTOR,'section.section-preference > div').text)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])


    work.find_element(By.CSS_SELECTOR, 'label > input[type=checkbox]').click()
    time.sleep(1)


print(work_link_list)
print(work_name_list)
print(cp_name_list)
print(skill_list)
print(intro_work_list)
print(prefer_list)



while(True):
    pass