from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('chromedriver', options=options)
driver.minimize_window()
com_logo_list = []
com_name_list = []
work_link_list = []
work_name_list = []
workname = '서버개발'
work = workname + ' 채용'


driver.implicitly_wait(5)

driver.get('https://www.google.com')
inputid = driver.find_element(By.CSS_SELECTOR, 'input')
inputid.send_keys(work)
inputid.submit()

clickwork = driver.find_element(By.CLASS_NAME, 'iI6nue.ieGFJe')
clickwork.click()

com_logos = driver.find_elements(By.CLASS_NAME, 'YQ4gaf.zr758c')
for com_logo in com_logos[:5]:
    com_logo_list.append(com_logo.get_attribute('src'))

work_links = driver.find_elements(By.CLASS_NAME, 'pMhGee.Co68jc.j0vryd')
for work_link in work_links[:5]:
    work_link_list.append((work_link.get_attribute('href')))

com_names = driver.find_elements(By.CLASS_NAME, 'vNEEBe')
for com_name in com_names[:5]:
    com_name_list.append(com_name.text)

work_names = driver.find_elements(By.CLASS_NAME, 'BjJfJf.PUpOsf')
for work_name in work_names[:5]:
    work_name_list.append(work_name.text)

print(com_name_list)
print(work_name_list)
print(com_logo_list)
print(work_link_list)
