from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


def parse_glampi_ru():
    url = "https://glampspace.ru/region/kareliya/"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    data = []
    try:
        driver.get(url)
        time.sleep(5)  # Ждем, пока страница полностью загрузится

        # Найдите все карточки глэмпингов (при необходимости уточните селектор контейнера карточек)
        glamping_cards = driver.find_elements(By.CSS_SELECTOR, "h1.h2")
        for card in glamping_cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, "div.object-card__title").text.strip()
                location = card.find_element(By.CSS_SELECTOR, "div.div.object-card__taxonomies").text.strip()

                prices = card.find_elements(By.CSS_SELECTOR, "div.object-card__price")
                weekday_price = prices[0].text.strip() if len(prices) > 0 else "Не указано"
                weekend_price = prices[1].text.strip() if len(prices) > 1 else "Не указано"

                data.append({
                    "Название": name,
                    "Локация": location,
                    "Цена (будни)": weekday_price,
                    "Цена (выходные)": weekend_price,
                })
            except Exception as e:
                print(f"Ошибка при обработке карточки: {e}")
    except Exception as e:
        print(f"Ошибка при парсинге сайта: {e}")
    finally:
        driver.quit()

    return data


def save_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel("glampi_data.xlsx", index=False)
    print("Данные успешно сохранены в 'glampi_data.xlsx'")


def main():
    data = parse_glampi_ru()
    if data:
        save_to_excel(data)
    else:
        print("Данные не были собраны.")


if __name__ == "__main__":
    main()
