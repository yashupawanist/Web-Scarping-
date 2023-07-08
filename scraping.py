import requests
from bs4 import BeautifulSoup

def scrape_product_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(response.content, 'html.parser')

    product_listings = soup.find_all('div', {'data-component-type': 's-search-result'})

    products = []
    for listing in product_listings:
        product_data = {}

        # Extracting product URL
        product_link = listing.find('a', class_='a-link-normal s-no-outline')['href']
        product_data['URL'] = f"https://www.amazon.in{product_link}"

        # Extracting product name
        product_name = listing.find('span', class_='a-size-medium a-color-base a-text-normal').text
        product_data['Name'] = product_name.strip()

        # Extracting product price
        product_price = listing.find('span', class_='a-offscreen').text
        product_data['Price'] = product_price.strip()

        # Extracting rating
        product_rating = listing.find('span', {'class': 'a-icon-alt'})
        if product_rating:
            product_data['Rating'] = product_rating.text.split()[0]
        else:
            product_data['Rating'] = 'N/A'

        # Extracting number of reviews
        product_reviews = listing.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        if product_reviews:
            product_data['Reviews'] = product_reviews.text
        else:
            product_data['Reviews'] = '0'

        products.append(product_data)

    return products

def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_details = {}

    # Extracting ASIN
    try:
        product_asin = soup.find('th', text='ASIN').find_next_sibling('td').text
    except AttributeError:
        product_asin = 'N/A'
    product_details['ASIN'] = product_asin.strip()

    # Extracting product description
    try:
        product_desc = soup.find('div', {'id': 'productDescription'}).text
    except AttributeError:
        product_desc = 'N/A'
    product_details['Description'] = product_desc.strip()

    # Extracting manufacturer
    product_manufacturer_elem = soup.find('a', {'id': 'bylineInfo'})
    if product_manufacturer_elem is not None:
        product_manufacturer = product_manufacturer_elem.text.strip()
    else:
        product_manufacturer = 'N/A'
    product_details['Manufacturer'] = product_manufacturer

    return product_details
