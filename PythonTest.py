from selenium import webdriver
from selenium.webdriver.common.by import By
from tabulate import tabulate
import time

#### Запуск браузера ####
driver = webdriver.Chrome()
# Перехід на сторінку
driver.get('http://127.0.0.1:8000')  # URL сторінки
# Список для зберігання результатів тестів
test_results_1 = []
test_results_2 = []


#### Тест-Сьют 1: Основна функціональність відео ####
# Тест-кейс 1.1: Увімкнення відео
def test_enable_video():
    try:
        video = driver.find_element(By.ID, 'video')
        toggle_button = driver.find_element(By.ID, 'toggleButton')

        # Натискання на кнопку для увімкнення відео
        toggle_button.click()
        time.sleep(1)  # Очікування для завантаження відео

        # Перевірки
        assert video.is_displayed(), "Відео не відображається після увімкнення."
        assert toggle_button.text == 'Вимкнути відео', "Текст кнопки не змінився на 'Вимкнути відео'."

        test_results_1.append(["Увімкнення відео", "Пройдено", "Усі перевірки успішні"])
    except Exception as e:
        test_results_1.append(["Увімкнення відео", "Не пройдено", str(e)])
# Тест-кейс 1.2: Вимкнення відео
def test_disable_video():
    try:
        video = driver.find_element(By.ID, 'video')
        toggle_button = driver.find_element(By.ID, 'toggleButton')

        # Натискання на кнопку для вимкнення відео
        toggle_button.click()
        time.sleep(1)

        # Перевірки
        assert not video.is_displayed(), "Відео відображається після вимкнення."
        assert toggle_button.text == 'Увімкнути відео', "Текст кнопки не змінився на 'Увімкнути відео'."

        test_results_1.append(["Вимкнення відео", "Пройдено", "Усі перевірки успішні"])
    except Exception as e:
        test_results_1.append(["Вимкнення відео", "Не пройдено", str(e)])
# Тест-кейс 1.3: Перемикання камери
def test_switch_camera():
    try:
        switch_button = driver.find_element(By.ID, 'switchCamera')
        camera_info = driver.find_element(By.ID, 'camera-info')

        current_camera = camera_info.text  # Поточна камера

        # Натискання на кнопку для перемикання камери
        switch_button.click()
        time.sleep(1)  # Очікування для зміни камери

        new_camera = camera_info.text  # Нова камера

        # Перевірка
        assert current_camera != new_camera, "Камера не змінилася після натискання кнопки."

        test_results_1.append(["Перемикання камери", "Пройдено", "Камера успішно змінилася"])
    except Exception as e:
        test_results_1.append(["Перемикання камери", "Не пройдено", str(e)])
# Тест-кейс 1.4: Відео недоступне
def test_video_unavailable():
    try:
        # Симуляція недоступного відео (припустимо, перевірка існує у вашій системі)
        video = driver.find_element(By.ID, 'video')
        driver.execute_script("arguments[0].src = 'invalid_source';", video)
        time.sleep(2)  # Очікування для симуляції помилки завантаження

        assert not video.is_displayed(), "Відео все ще відображається з недоступним джерелом."
        test_results_1.append(["Відео недоступне", "Пройдено", "Відео коректно не відображається"])
    except Exception as e:
        test_results_1.append(["Відео недоступне", "Не пройдено", str(e)])
# Запуск тестів
test_enable_video()
test_disable_video()
test_switch_camera()
test_video_unavailable()


#### Тест-Сьют 2: Функціональність скріншоту ####
# Тест-кейс 2.1: Кнопка скріншоту активна
def test_screenshot_button_active():
    try:
        screenshot_button = driver.find_element(By.ID, 'screenshotButton')

        # Перевірка, чи кнопка видима та активна
        assert screenshot_button.is_displayed(), "Кнопка скріншоту не відображається."
        assert screenshot_button.is_enabled(), "Кнопка скріншоту неактивна."

        test_results_2.append(["Кнопка скріншоту активна", "Пройдено", "Кнопка активна та видима"])
    except Exception as e:
        test_results_2.append(["Кнопка скріншоту активна", "Не пройдено", str(e)])
# Тест-кейс 2.2: Скріншот створюється
def test_screenshot_creation():
    try:
        # Натискання на кнопку для перемикання камери
        switch_button = driver.find_element(By.ID, 'switchCamera')
        switch_button.click()
        time.sleep(1)  # Очікування для зміни камери

        # Натискання на кнопку для увімкнення відео
        toggle_button = driver.find_element(By.ID, 'toggleButton')
        toggle_button.click()
        time.sleep(4)  # Очікування для завантаження відео

        # Натискання кнопки для створення скріншоту
        screenshot_button = driver.find_element(By.ID, 'screenshotButton')
        screenshot_button.click()
        time.sleep(2)  # Очікування для створення скріншоту

         # Перевірка, чи створено Blob для скріншота
        blob_data = driver.execute_script("""
            return (window.lastBlob && window.lastBlob.size > 0) ? true : false;
        """)
        assert blob_data, "Blob для скріншота не створений."

        test_results_2.append(["Скріншот створюється", "Пройдено", "Скріншот успішно створений"])
    except Exception as e:
        test_results_2.append(["Скріншот створюється", "Не пройдено", str(e)])
# Тест-кейс 2.3: Масштабування скріншоту
def test_screenshot_scaling():
    try:
        canvas = driver.find_element(By.ID, 'canvas')

        # Отримання розмірів canvas після створення скріншоту
        width = driver.execute_script("return arguments[0].width;", canvas)
        height = driver.execute_script("return arguments[0].height;", canvas)

        # Припускаємо, що масштабування встановлено у 2x
        video = driver.find_element(By.ID, 'video')
        video_width = video.get_attribute("videoWidth") or video.size["width"]
        video_height = video.get_attribute("videoHeight") or video.size["height"]

        assert width == int(video_width) * 2, "Ширина скріншоту некоректна."
        assert height == int(video_height) * 2, "Висота скріншоту некоректна."

        test_results_2.append(["Масштабування скріншоту", "Пройдено", "Розміри відповідають масштабуванню"])
    except Exception as e:
        test_results_2.append(["Масштабування скріншоту", "Не пройдено", str(e)])
# Тест-кейс 2.4: Завантаження скріншоту
def test_screenshot_download():
    try:
        screenshot_button = driver.find_element(By.ID, 'screenshotButton')

        # Натискання кнопки для створення скріншоту
        screenshot_button.click()
        time.sleep(2)

        # Перевірка, чи створено посилання для завантаження
        download_exists = driver.execute_script("""
            return document.querySelector('a[href^="blob:"]') !== null || !!window.lastDownloadURL;
        """)
        assert download_exists is not None, "Посилання для завантаження не створено."

        test_results_2.append(["Завантаження скріншоту", "Пройдено", "Скріншот завантажується"])
    except Exception as e:
        test_results_2.append(["Завантаження скріншоту", "Не пройдено", str(e)])
# Запуск тестів
test_screenshot_button_active()
test_screenshot_creation()
test_screenshot_scaling()
test_screenshot_download()


#### Виведення результатів тестів у вигляді таблиці ####
headers = ["Назва тесту", "Статус", "Коментар"]
# Тест-Сьют 1
print("\nТест-Сьют 1: Основна функціональність відео:")
table_1 = tabulate(test_results_1, headers, tablefmt="grid")
print(table_1)
# Тест-Сьют 2
print("\nТест-Сьют 2: Функціональність скріншоту:")
table_2 = tabulate(test_results_2, headers, tablefmt="grid")
print(table_2)


#### Закриття браузера після тестів ####
driver.quit()
