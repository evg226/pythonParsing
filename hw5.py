import time

from pymongo import MongoClient, errors
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = MongoClient('mongodb://localhost:27017')
db = client['emails']
doc = db.mailru

driver = webdriver.Chrome(service=Service('./chromedriver'))

driver.get('https://account.mail.ru/login')
login = driver.find_element(By.NAME, 'username')
login.send_keys("study.ai_172@mail.ru")
login.submit()
time.sleep(1)
password = driver.find_element(By.NAME, 'password')
password.send_keys("NextPassword172#")
password.submit()

emailsContainer = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'dataset__items')))

data = []
dataId = None
last = None

while True:
    emails = emailsContainer.find_elements(By.XPATH, "//a[contains(@class,'llc')]")
    for email in emails:
        dataId = email.get_attribute('data-id')
        if dataId not in data and dataId is not None:
            data.append(dataId)
    if dataId == last or dataId is None:
        break
    else:
        element = f"a[data-id='{dataId}']"
        driver.execute_script(
            f'const last = document.querySelector("{element}");console.log(last);last.scrollIntoView()')
        last = dataId
        time.sleep(1)

print(len(data))
for id in data:
    driver.get(f'https://e.mail.ru/inbox/{id}/')
    address = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'letter-contact')]"))).text
    date = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'letter__date')]"))).text
    subject = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(@class,'thread-subject')]"))).text
    body = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'letter__body')]"))).get_attribute('innerHTML')
    try:
        doc.insert_one({'_id': id, 'address': address, 'date': date, 'subject': subject, 'body': body})
    except errors.DuplicateKeyError:
        pass
