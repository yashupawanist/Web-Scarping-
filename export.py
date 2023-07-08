import csv
import json
import pandas as pd

from scraping import scrape_product_listings, scrape_product_details

def scrape_and_export_data():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

    all_products = []

    for page in range(1, 21):  # Scrape 20 pages
        url = base_url.format(page)
        products = scrape_product_listings(url)
        all_products.extend(products)

    for product in all_products:
        url = product['URL']
        product_details = scrape_product_details(url)
        product.update(product_details)

    # Export data to CSV
    keys = all_products[0].keys() if all_products else []
    filename_csv = 'product_data.csv'
    with open(filename_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, keys)
        writer.writeheader()
        writer.writerows(all_products)

    # Export data to JSON
    filename_json = 'product_data.json'
    with open(filename_json, 'w', encoding='utf-8') as file:
        json.dump(all_products, file, ensure_ascii=False, indent=4)

    # Export data to Excel
    df = pd.DataFrame(all_products)
    filename_excel = 'product_data.xlsx'
    df.to_excel(filename_excel, index=False)

    print("Scraped data has been exported to the following formats:")
    print(f"- CSV: {filename_csv}")
    print(f"- JSON: {filename_json}")
    print(f"- Excel: {filename_excel}")

scrape_and_export_data()
