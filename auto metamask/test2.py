import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import keyboard
from selenium.webdriver.support.ui import Select


# Функция для чтения сид-фраз из файла
def read_seed_phrases(file_path):
    with open(file_path, 'r') as file:
        seed_phrases = [line.strip() for line in file]
    return seed_phrases


# Функция для получения списка профилей из Dolphin Anty
def get_dolphin_profile(api_token):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    url = 'https://dolphin-anty-api.com/browser_profiles?limit'
    response = requests.get(url, headers=headers)
    list_browsers = response.json()['data']
    list_id = []
    for i in range(len(list_browsers)):
        list_id.append([list_browsers[i].get('id'), list_browsers[i].get('name')])
    return list_id


# Функция для создания сессии в Dolphin Anty
def create_dolphin_session(profile_id):
    response = session.get(f'http://localhost:3001/v1.0/browser_profiles/{profile_id}/start?automation=1')
    return response.json()


# Функция для завершения сессии в Dolphin Anty
def stop_dolphin_session(profile_id):
    response = session.get(f'http://localhost:3001/v1.0/browser_profiles/{profile_id}/stop')
    return response.json()


# Функция для автоматизации входа в MetaMask с помощью Selenium
def login_metamask_with_selenium(seed_phrase, port, password):
    list_seed_phrase = seed_phrase.split(' ')
    options = webdriver.ChromeOptions()
    options.debugger_address = '127.0.0.1:' + port
    driver = webdriver.Chrome(options=options)

    # Переход на страницу MetaMask в Chrome Web Store
    driver.get("https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn")
    print('Загрузка MetaMask')
    time.sleep(5)

    # Установка MetaMask
    driver.find_element(By.XPATH,
                        '/html/body/c-wiz/div/div/main/div/section[1]/section/div[2]/div/button/span[6]').click()
    time.sleep(2)
    keyboard.send('tab')
    keyboard.send('enter')
    time.sleep(10)

    # Переход на страницу приветствия MetaMask
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/welcome')
    print('Вход в кошелек')
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[0])

    # Принимаем условия использования
    driver.find_element(By.ID, "onboarding__terms-checkbox").click()
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/ul/li[3]/button').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[2]/button[2]').click()
    time.sleep(2)

    # Переход на ввод сид-фразы
    print('Переход на ввод сид-фразы')
    select_el = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select')
    select = Select(select_el)
    select.select_by_value(str(len(list_seed_phrase)))

    # Ввод сид-фразы
    for i in range(len(list_seed_phrase)):
        driver.find_element(By.CSS_SELECTOR, f'[data-testid="import-srp__srp-word-{i}"]').send_keys(list_seed_phrase[i])
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="import-srp-confirm"]').click()
    print('Сид-фраза введена\nПереход на ввод пароля')
    time.sleep(2)

    # Ввод пароля
    driver.find_element(By.CSS_SELECTOR, '[data-testid="create-password-new"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="create-password-confirm"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="create-password-terms"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="create-password-import"]').click()
    time.sleep(2)

    # Завершение настройки
    driver.find_element(By.CSS_SELECTOR, '[data-testid="onboarding-complete-done"]').click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="pin-extension-next"]').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="pin-extension-done"]').click()
    time.sleep(2)
    driver.quit()


# Основной скрипт
if __name__ == "__main__":
    count = 0
    seed_phrases = read_seed_phrases('seed_phrases.txt')
    api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZDVmOWJhOTM4MmRmNGZmOTMwMDFmNGU4OGYxY2ZkMTliNTQzNjkwOGFiZjIwZmRlNjllYmFiNDFjZGMwZjNlZWFmMTdjMThlNmJlNDkxZGYiLCJpYXQiOjE3MjI3NTY4ODAuNDA2NjE3LCJuYmYiOjE3MjI3NTY4ODAuNDA2NjIsImV4cCI6MTcyNTM0ODg4MC4zOTU1MTYsInN1YiI6IjM2MTUxOTIiLCJzY29wZXMiOltdfQ.UDZ1LMTK_NIjmy7JKHQwIiGBlbZNQpFNw25FInn72WaQN6mh947PDTZpzNI6euORRhiINit0IqclSDfOFyjYI75VrLsxVU6SFGsRcb2yTV7eWOZ45Bi83YmbArBRbF-hPyrFOTscxdodc3ZLQxGBRdmHGZ1T00DRn6RC-7UrCwnXgIzFkQf8y7wBnFrf3wr0BxXqlJS3JT-xBddUY3qnjk9h-VdoWHoMtiUsywV5cKM_013A63EmBq9cUwVw7n-yFP4M9GqQpJIo1GdcM9pqSpQ9XKdrkgIVRISYs1PJXgNHri24BxUa7iwN23nhO76OZnpOztiFa1WXhSSj9voxfDYw5P31DkfqmkUhrYSk94-PyPfowzw6XfBDUckVFPbn_00CgWnwMU2IyevvoIH66x5ZcfFhuRaVL85bFAdA_m6u5LBb-VksLl0cptWf-cFYMIWxkwfFdXa56L_9dMo0B-nxojMU2cc-V-3DGe7YtjOjR7OREBIiGvct2-LOEwwdwAJPsbOFMDQxZ-G_dKhhvy228PBnpeEAi0kWfaFUwk3yDIx0bWkyNqB2qug6egCUpOW5Q1T6cpJDMzEXIvlgIxE-fhvP7Zrxk9kbzFrSvKcQCQUmlUWsEySgoWRd5aMZ6drgwNZbTBTkIUdNxpsN3x4YsEHdFhOMZ-46f3lKXn4"

    # Создание сессии для Dolphin Anty
    session = requests.Session()
    session.trust_env = False
    headers = {'Content-Type': 'application/json'}
    body = {"token": api_token}
    api_url = 'http://localhost:3001/v1.0/auth/login-with-token'
    response = session.post(api_url, json=body, headers=headers)

    password = input('Enter password for wallets: ')

    for i in range(len(seed_phrases)):
        seed_phrase = seed_phrases[i]
        print('Получение профилей')

        # Получение профилей Dolphin Anty
        profile_info = get_dolphin_profile(api_token)

        for j in range(len(profile_info)):
            if count == len(seed_phrases):
                print('Вход во все кошельки был выполнен.')
                break

            profile_id = profile_info[j][0]
            profile_name = profile_info[j][1]
            print(f'Вход в профиль {profile_name}')

            # Создание сессии Dolphin Anty
            session_info = create_dolphin_session(profile_id)
            if session_info['success'] == True:
                print(f'Открытие профиля {profile_name}')
                try:
                    port = str(session_info['automation']['port'])
                    login_metamask_with_selenium(seed_phrase, port, password)
                    print(f"Успешный вход в кошелек {profile_name}")
                    count += 1
                except Exception as e:
                    print(f"Ошибка при входе в кошелек {profile_name}: {e}")
                finally:
                    stop_dolphin_session(profile_id)
            else:
                print(f'Ошибка при открытии профиля {profile_name}')
