import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page_content(url):
    """
    Fetches the content of the page at the specified URL.
    
    Parameters:
    url (str): The URL of the page to fetch.
    
    Returns:
    str: The HTML content of the page if the request is successful; otherwise, None.
    """
    headers = {
        # User-Agent header to simulate a request from a real web browser
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
    try:
        # Send a GET request to the specified URL with custom headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.text  # Return the HTML content of the page
    except requests.exceptions.HTTPError as err:
        # Print an error message if there is an HTTP error
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        # Print a general error message for other exceptions
        print(f"An error occurred: {err}")

def parse_product_info(page_content):
    """
    Parses product information from the HTML content of the page.
    
    Parameters:
    page_content (str): The HTML content of the page.
    
    Returns:
    list: A list of dictionaries containing product name, price, and rating.
    """
    soup = BeautifulSoup(page_content, 'html.parser')  # Parse the HTML content with BeautifulSoup
    products = []  # List to store product information

    # Select all product elements from the page using CSS selectors
    for product in soup.select('.product-class'):
        # Extract the product name, price, and rating
        name = product.select_one('.product-name').get_text(strip=True)
        price = product.select_one('.product-price').get_text(strip=True)
        rating = product.select_one('.product-rating').get_text(strip=True)
        # Append the product information to the list
        products.append({'name': name, 'price': price, 'rating': rating})
    
    return products  # Return the list of products

def save_to_csv(products, filename):
    """
    Saves the list of products to a CSV file.
    
    Parameters:
    products (list): A list of dictionaries containing product information.
    filename (str): The name of the file to save the data.
    """
    df = pd.DataFrame(products)  # Convert the list of products to a pandas DataFrame
    df.to_csv(filename, index=False)  # Save the DataFrame to a CSV file
    print(f"Saved {len(products)} products to {filename}")  # Print the number of products saved

if __name__ == "__main__":
    url = 'https://example.com/products'  # Replace with the actual URL of the page to scrape
    page_content = get_page_content(url)  # Fetch the page content
    if page_content:  # Check if page content was successfully retrieved
        products = parse_product_info(page_content)  # Parse product information
        save_to_csv(products, 'products.csv')  # Save the product information to a CSV file
