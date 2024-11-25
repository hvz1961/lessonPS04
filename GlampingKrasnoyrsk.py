import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Функция для парсинга глэмпингов из сайта
def parse_glamping_info():
    # Пример URL для парсинга (замените на реальные URL глэмпингов)
    urls = [
        "https://glampi.ru/catalog/glempings/karelia/"  # Подставьте реальные сайты глэмпингов
        ]

    data = []

    for url in urls:
        print(f"Парсим сайт: {url}")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Ошибка подключения к {url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Пример: Найти информацию о загрузке
            # (измените селекторы в зависимости от структуры сайта)
            glamping_name = soup.find("div", class_="h5.mb-4.mb-sm-8").text.strip()
            days = soup.find_all("div", class_="h5.mb-4.mb-sm-8")

            for day in days:
                day_name = day.find("span", class_="day-name").text.strip()
                occupancy = day.find("span", class_="occupancy").text.strip()

                data.append({
                    "Название глэмпинга": glamping_name,
                    "День недели": day_name,
                    "Загрузка (%)": occupancy
                })
        except Exception as e:
            print(f"Ошибка при парсинге {url}: {e}")

    return data


# Функция для сохранения данных в Excel
def save_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel("glamping_data.xlsx", index=False)
    print("Данные успешно сохранены в 'glamping_data.xlsx'")
#
#
# Основная функция
def main():
    data = parse_glamping_info()
    if data:
        save_to_excel(data)
    else:
        print("Данные не были собраны.")

#
if __name__ == "__main__":
    main()
