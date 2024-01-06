import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

BUY_PRICE = 100
PRODUCT_URL = 'https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL = "jeremiaspasolli@gmail.com"

response = requests.get(url=PRODUCT_URL,
                        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                               ' Chrome/120.0.0.0 Safari/537.36',
                                 'Accept-Language': 'en-US,en;q=0.9'})
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
title = soup.find(id="productTitle").get_text().strip()
price = soup.select_one('span .a-price-whole').getText().strip()
cents = soup.select_one('span .a-price-fraction').getText().strip()
total_price = float(price + cents)

if total_price <= BUY_PRICE:
    message = f"{title} is now ${total_price}"

    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        result = connection.login(MAIL, MAIL_PASSWORD)
        connection.sendmail(from_addr=MAIL, to_addrs=MAIL, msg=f"Subject: Amazon Price Alert!\n\n{message}\n"
                                                               f"{PRODUCT_URL}".encode('utf-8'))
