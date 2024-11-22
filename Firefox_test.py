from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Функция для инициализации драйвера
def init_driver():
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Firefox(options=options)
    return driver


# Функция для поиска на Википедии
def search_wikipedia(driver, query):
    driver.get("https://ru.wikipedia.org/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ожидание загрузки страницы


# Функция для вывода параграфов текущей статьи
def display_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
    for i, p in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:\n{p.text}\n")
        if i % 3 == 2:  # Показывать три параграфа за раз
            choice = input("Продолжить просмотр параграфов? (да/нет): ").strip().lower()
            if choice != "да":
                break


# Функция для перехода по связанным ссылкам
def follow_link(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    for i, link in enumerate(links[:10]):  # Показать только первые 10 ссылок
        print(f"{i + 1}: {link.text}")
    choice = input("Введите номер ссылки для перехода или 'назад' для выхода: ").strip().lower()
    if choice.isdigit() and 1 <= int(choice) <= len(links[:10]):
        selected_link = links[int(choice) - 1]
        selected_link.click()
        time.sleep(2)  # Ожидание загрузки страницы
    else:
        print("Возвращаемся в меню.")


# Основная функция программы
def main():
    driver = init_driver()
    try:
        query = input("Введите запрос для поиска на Википедии: ").strip()
        search_wikipedia(driver, query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")
            choice = input("Ваш выбор: ").strip()

            if choice == "1":
                display_paragraphs(driver)
            elif choice == "2":
                follow_link(driver)
            elif choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
