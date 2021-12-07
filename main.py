from bs4 import BeautifulSoup
import lxml
import requests
import smtplib

MY_EMAIL = YOUR_EMAIL
PASSWORD = YOUR_PASSWORD
RECIPIENT_EMAIL = RECIPIENT_EMAIL
PRICE_POINT = 100

ACCEPT_LANGUAGE = "en-US,en;q=0.9"
USER_AGENT = YOUR_USER_AGENT
PRODUCT_URL = "https://www.amazon.ca/Instant-Pot-Duo-Multi-Use-Programmable/dp/B01B1VC13K?th=1"

HEADERS = {
    "Accept-Language": ACCEPT_LANGUAGE,
    "User-Agent": USER_AGENT
}

response = requests.get(url=PRODUCT_URL, headers=HEADERS)
amazon_response = response.text

soup = BeautifulSoup(amazon_response, "lxml")

product_name = soup.find(
    name="span", class_="a-size-large product-title-word-break").getText()
product_title = " ".join(product_name.split()[0:2])
product_description = product_name.strip("\n")

product_price = float(
    soup.find(name="span", class_="a-offscreen").getText().strip("$"))

if product_price <= PRICE_POINT:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=RECIPIENT_EMAIL,
            msg=f"Subject:Amazon {product_title} Now Only ${product_price}!\n\n{product_description}\n\nBuy now: {PRODUCT_URL}"
            )
