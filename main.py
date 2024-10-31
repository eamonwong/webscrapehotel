from playwright.sync_api import sync_playwright
import pandas as pd


def main():
    with sync_playwright() as p:
        checkin_date = '2024-12-11'
        checkout_date = '2024-12-12'

        page_url = f'https://www.booking.com/searchresults.en-gb.html?ss=United+States+of+America&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaFCIAQGYAQm4AQfIAQzYAQHoAQGIAgGoAgO4Avj6jbkGwAIB0gIkMmE5Y2RjZmUtY2NmNi00NDU4LWEyYzAtNWRhMzUzZTE5N2Q32AIF4AIB&sid=a1130072273fb22761e4532733c970f4&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=224&dest_type=country&ac_position=1&ac_click_type=b&ac_langcode=xu&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=48665a7c9c6d01bd&ac_meta=GhA0ODY2NWE3YzljNmQwMWJkIAEoATICeHU6BGFtZXJAAEoAUAA%3D&checkin={checkin_date}&checkout={checkout_date}&group_adults=2&no_rooms=1&group_children=0'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'There are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = \
            hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]

            hotels_list.append(hotel_dict)

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False)

        browser.close()


if __name__ == '__main__':
    main()
